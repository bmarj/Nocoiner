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
    headers = {
            'authority': 'www.binance.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
  #          'x-trace-id': '3d1a8b33-2d74-45ad-8fad-3203843a21de',
  #          'csrftoken': '22e5f94a7a96a2b450eed547418f7665',
  #          'x-ui-request-trace': '3d1a8b33-2d74-45ad-8fad-3203843a21de',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
            'content-type': 'application/json',
            'lang': 'en',
 #           'fvideo-id': '31e3a07780b9ad61a4e03c7f0ff9cef782fe7d56',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
#            'device-info': 'eyJzY3JlZW5fcmVzb2x1dGlvbiI6IjM4NDAsMTYwMCIsImF2YWlsYWJsZV9zY3JlZW5fcmVzb2x1dGlvbiI6IjM4NDAsMTU3MCIsInN5c3RlbV92ZXJzaW9uIjoiV2luZG93cyAxMCIsImJyYW5kX21vZGVsIjoidW5rbm93biIsInN5c3RlbV9sYW5nIjoiaHItSFIiLCJ0aW1lem9uZSI6IkdNVCsyIiwidGltZXpvbmVPZmZzZXQiOi0xMjAsInVzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvOTQuMC40NjA2LjcxIFNhZmFyaS81MzcuMzYiLCJsaXN0X3BsdWdpbiI6IlBERiBWaWV3ZXIsQ2hyb21lIFBERiBWaWV3ZXIsQ2hyb21pdW0gUERGIFZpZXdlcixNaWNyb3NvZnQgRWRnZSBQREYgVmlld2VyLFdlYktpdCBidWlsdC1pbiBQREYiLCJjYW52YXNfY29kZSI6IjVmOGRkMzI0Iiwid2ViZ2xfdmVuZG9yIjoiR29vZ2xlIEluYy4gKEludGVsKSIsIndlYmdsX3JlbmRlcmVyIjoiQU5HTEUgKEludGVsLCBJbnRlbChSKSBVSEQgR3JhcGhpY3MgNjIwIERpcmVjdDNEMTEgdnNfNV8wIHBzXzVfMCwgRDNEMTEtMjcuMjAuMTAwLjg4NTQpIiwiYXVkaW8iOiIxMjQuMDQzNDc1Mjc1MTYwNzQiLCJwbGF0Zm9ybSI6IldpbjMyIiwid2ViX3RpbWV6b25lIjoiRXVyb3BlL1phZ3JlYiIsImRldmljZV9uYW1lIjoiQ2hyb21lIFY5NC4wLjQ2MDYuNzEgKFdpbmRvd3MpIiwiZmluZ2VycHJpbnQiOiJiZmZiMmI1M2ExOTQ0NzVlZGQ3OWRiZTNkODBiMzc4MiIsImRldmljZV9pZCI6IiIsInJlbGF0ZWRfZGV2aWNlX2lkcyI6IjE2MzMzNDM4OTM4NTNueTdzTU1RV2E1eERHaUJoaXBFIn0=',
#            'bnc-uuid': 'ba1dab35-8dcc-4298-a00b-c3661b914c3b',
            'clienttype': 'web',
            'sec-ch-ua-platform': '"Windows"',
            'accept': '*/*',
            'origin': 'https://www.binance.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
#            'referer': 'https://www.binance.com/en/futures-activity/leaderboard?type=myProfile&encryptedUid=CCF3E0CB0AAD54D9D6B4CEC5E3E741D2',
            'accept-language': 'hr-HR,hr;q=0.9,en;q=0.8',
            #'cookie': 'cid=2NjR7Epn; nft-init-compliance=true; s9r1=A0C22FE10683CE87A507F89888EBF2F8; cr00=696353F394101D4F8D781F8963EE6A93; d1og=web.138803268.B150E33C795E97CA440CF3C83547EBA9; r2o1=web.138803268.F53CDC3BA9760A8ED91C11F842B98348; f30l=web.138803268.63DCCE1FA980F01477BCF657EDF73004; __BINANCE_USER_DEVICE_ID__={"861af6134b041e39cdaacffbb31410c9":{"date":1633343894071,"value":"1633343893853ny7sMMQWa5xDGiBhipE"}}; p20t=web.138803268.26B15ADE17FFF733B959C9840D243098; sajssdk_2015_cross_new_user=1; userPreferredCurrency=USD_USD; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22138803268%22%2C%22first_id%22%3A%2217c4ae40a7a567-023ba53950c5a5-b7a1b38-6144000-17c4ae40a7b6e6%22%2C%22props%22%3A%7B%7D%2C%22%24device_id%22%3A%2217c4ae40a7a567-023ba53950c5a5-b7a1b38-6144000-17c4ae40a7b6e6%22%7D; bnc-uuid=ba1dab35-8dcc-4298-a00b-c3661b914c3b; source=referral; campaign=www.binance.com; lang=en; BNC_FV_KEY=31e3a07780b9ad61a4e03c7f0ff9cef782fe7d56; BNC_FV_KEY_EXPIRE=1633430253490'
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
