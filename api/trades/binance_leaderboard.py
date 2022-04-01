from datetime import datetime
from flask import current_app, Blueprint, session, jsonify, url_for, request, render_template, flash
from flask_sqlalchemy import orm
from marshmallow import EXCLUDE
import requests
import json
# from marshmallow.exceptions import ValidationError

from api.datatables import DataTables
from api.user_management import login_required, authorize
from api.utils.common import (generic_edit, generic_form_edit, generic_form_delete)
from api.models import Trade, KnownPosition, Leader, db
from .business import (get_leaders, query_trades, query_active_positions,
                       get_positions_except, deactivate_positions,
                       get_positions, save_position, save_trade)

def process_leaders_data():
    for leader in get_leaders():
        if leader.is_active:
            process_leader(leader)


def process_leader(leader: Leader):
    headers = {'authority': 'www.binance.com',
               'pragma': 'no-cache',
               'cache-control': 'no-cache',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
               'content-type': 'application/json',
               'lang': 'en',
               'sec-ch-ua-mobile': '?0',
               'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
               'clienttype': 'web',
               'sec-ch-ua-platform': '"Windows"',
               'accept': '*/*',
               'origin': 'https://www.binance.com',
               'sec-fetch-site': 'same-origin',
               'sec-fetch-mode': 'cors',
               'sec-fetch-dest': 'empty',
               'accept-language': 'hr-HR,hr;q=0.9,en;q=0.8',
               }
    res = requests.post(
        url='https://www.binance.com/bapi/futures/v1/public/future/leaderboard/getOtherPosition',
        headers=headers,
        data=f'{{"encryptedUid":"{leader.encrypted_uid}","tradeType":"PERPETUAL"}}'
    )

    if res.status_code != 200:
        print('Error fetching positions')
        # TODO: log and raise error
        return

    positions = res.json()['data']['otherPositionRetList']

    if positions is None:
        print(f"Positions not found: {leader.name}")
        return

    position_summary = {p['symbol']: p['amount'] for p in positions}

    # first time use, move to app init
    if not hasattr(current_app, 'position_summaries'):
        current_app.position_summaries = {}
    # TODO: use real cache
    cached_summary = current_app.position_summaries
    # return if no changes in trader positions
    if position_summary == cached_summary.get(leader.encrypted_uid):
        return

    trades = []
    user_position_symbols = [p['symbol'] for p in positions]
    closed_positions = get_positions_except(user_position_symbols, leader.id)
    for pos in closed_positions:
        change = process_closed_position(pos)
        trades.append(change)
    deactivate_positions([p.symbol for p in closed_positions], leader.id)
    db.session.commit()

    known_positions = get_positions(user_position_symbols, leader.id)
    for pos in positions:
        active_pos = KnownPosition()
        active_pos.symbol = pos['symbol']
        active_pos.amount = pos['amount']
        active_pos.entry_price = pos['entryPrice']
        active_pos.position_size = pos['amount'] * pos['markPrice']
        ut = pos['updateTime']
        active_pos.update_time = datetime(ut[0], ut[1], ut[2], ut[3], ut[4], ut[5])
        active_pos.leader_id = leader.id
        active_pos.is_active = True
        change = process_open_position(active_pos, known_positions)
        if change:
            save_position(active_pos)
            trades.append(change)

    for trade in trades:
        save_trade(trade)

    db.session.commit()
    # put trades in cache
    current_app.position_summaries[leader.encrypted_uid] = position_summary


def process_closed_position(history_position: KnownPosition) -> Trade:
    # deep copy position object
    position_change = Trade()
    position_change.symbol = history_position.symbol
    position_change.amount = 0.00  # history_position.amount
    position_change.entry_price = history_position.entry_price
    position_change.position_size = 0.00  # history_position.position_size
    position_change.update_time = history_position.update_time
    position_change.leader_id = history_position.leader_id

    # closed trade
    position_change.amount_change = history_position.amount * -1
    # mark price is last known price
    position_change.change_entry_price = history_position.entry_price  # history_position.mark_price
    position_change.position_size = 0.00  # history_position.position_size
    position_change.change_size = position_change.amount_change * position_change.change_entry_price

    if position_change.amount_change > 0.00:
        position_change.direction = "buy-close"
    elif position_change.amount_change < 0.00:
        position_change.direction = "sell-close"

    # orderHistory.push(position_change)
    return position_change


def process_open_position(pos: KnownPosition, known_positions) -> Trade:
    # deep copy position object
    position_change = Trade()
    position_change.symbol = pos.symbol
    position_change.amount = pos.amount
    position_change.entry_price = pos.entry_price
    position_change.position_size = pos.position_size
    position_change.update_time = pos.update_time
    position_change.leader_id = pos.leader_id

    # position changed
    existing_trades = list(filter(lambda p: p.symbol == pos.symbol, known_positions))
    if existing_trades:
        existing_trade = existing_trades[0]
        # trade with that symbol already active
        # Compare with new state
        position_change.amount_change = pos.amount - existing_trade.amount

        # calculate entry price
        am1 = existing_trade.amount
        am2 = position_change.amount_change
        pr1 = existing_trade.entry_price
        pr_average = pos.entry_price
        if am2 != 0.00:
            position_change.change_entry_price = (pr_average*(am1+am2) - am1*pr1)/am2
    else:
        # new trade
        position_change.amount_change = pos.amount
        position_change.change_entry_price = pos.entry_price

    # if exposure changed
    if position_change.amount_change != 0.00:
        if position_change.amount_change > 0.00:
            position_change.direction = "buy"
        else:
            position_change.direction = "sell"
        position_change.change_size = position_change.amount_change * position_change.change_entry_price
        return position_change
        #orderHistory.push(position_change)
        #known_positions[pos.symbol] = pos
