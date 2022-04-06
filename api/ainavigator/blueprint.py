from flask import request, Blueprint, jsonify, current_app
from datetime import datetime
import openai

bp = Blueprint('ainavigator', __name__,
               template_folder='templates',
               static_folder='static', static_url_path='/ainavigator/static')

@bp.route('/forinrobot', methods=['POST', 'GET'])
def robot():
    openai.api_key = current_app.config['OPENAI_API_KEY']
    openai.api_base = current_app.config['OPENAI_BASE_ADDRESS']
    engine = current_app.config.get('OPENAI_DEFAULT_ENGINE', 'gpt-j-6b')
    temperature = current_app.config.get('OPENAI_DEFAULT_TEMPERATURE', '0')

    # # List Engines (Models)
    # engines = openai.Engine.list()
    # # Print all engines IDs
    # for engine in engines.data:
    #     print(engine.id)

    user_prompt = request.form.to_dict()['input_query']
    if not user_prompt:
        return jsonify({'status': 'error', 'result': ''}), 400

    prompt = f"""We will extract known values and organize them in classes. 

Format is
[CLASS]: [accepted values]
and below is description of values that we are extracting.

[DIRECTION]: [oa, od]
oa = order ascending (default value if ordering is specified)
od = order descending

[LIMIT]: [l10, l25, l50, l100]
l10 = 10 results by default
l25 = 25 results
l50 = 50 results
l100 = 100 results

[COLUMN]: [symbol, change_entry_price, change_size, amount_change, entry_price, amount, position_size, created_timestamp, direction]
symbol = cryptocurrency exchange recognized name
change_entry_price = price at which cryptocurrency is traded i current trade
change_size = dollar value of current trade
amount_change = amount of crypto traded
entry_price = position average price for a trader and cryptocurrency
amount = position amount in cryptocurrency
position_size = position size in dollars
created_timestamp = time of recorded trade
direction = buy or sell direction of a trade

[BASE]: [profitloss, transactions, tradedvalue, tradeactivity, positions, trades, traders]
profitloss = Estimated profit and loss for all traders, trader profiability, trader quality, trader visualization
transactions = Transaction sizes by position size and price, volume of trades, big players, small players, transaction visualization
tradedvalue = Value traded per coins (securities), who traded in what quantity, which crypto currency has most traded value
tradeactivity = Number of trades per coin, which crypto currency has most trades
positions = Known positions that traders hold at this moment, list of positions, trader portfolio, owned crypto
trades = View of esitimated trades, crypto buyin and selling, transactions made by trader
traders = List of trader profiles, players

[TICKER]: [BTCUSDT, ADAUSDT, ETHUSDT, EOSUSDT, BNBUSDT, 1000SHIBUSDT, SOLUSDT, LUNAUSDT]

[FILTER]: [>0, >100, >1000, >10000, >100000, ClickHereNow]
>0 = positive, non-negative
>100 = moderete size
>1000 = respectable size
>10000 = large
>100000 = huge
ClickHereNow = trader name
TradingHorse = trader name
[TICKER] = acceptable value

INPUT: show trade list for ADA
[BASE]: trades
[FILTER]: ADAUSDT
INPUT: coin trader buy/sells analytics, ordered descending by symbol
[BASE]: positions
[COLUMN]: symbol
[DIRECTION]: od
INPUT:  coin trader buy/sells analytics, ordered ascending by symbol
[BASE]: positions
[COLUMN]: symbol
[DIRECTION]: od
INPUT:  profit visualization, 25 results, sorted by direction from lower to higher
[BASE]: profitloss
[COLUMN]: direction
[DIRECTION]: oa
[LIMIT]: l25
INPUT: list trades, fifty rows sort by direc field made by Clickherenow
[BASE]: trades
[COLUMN]: direction
[LIMIT]: l50
[FILTER]: Clickherenow
INPUT: {user_prompt}
["""

    print('Promt: ' + user_prompt)

    # Create a completion, return results streaming as they are generated.
    # Run with `python3 -u` to ensure unbuffered output.
    completion = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        max_tokens=50,
        temperature=temperature,
        stop=['INPUT:'],
        stream=False)

    suggested_response = completion.choices[0].text.rstrip('INPUT:').strip().replace(' ', '')
    parts = {ct.split(']:')[0]: ct.split(']:')[1]
             for ct in suggested_response.replace('\n', '').split('[')}

    if not parts.get('BASE'):
        return jsonify({'status': 'error', 'result': 'Try to explain better'}), 400

    url = '/' + parts['BASE']

    hashpart = ''
    if len(parts) > 1:
        hashpart = '#datatable='

    if parts.get('LIMIT'):
        hashpart += '' + parts.get('LIMIT') + ':'
    if parts.get('COLUMN'):
        hashpart += '' + parts.get('DIRECTION', 'oa') + parts.get('COLUMN') + ':'
    if parts.get('FILTER') or parts.get('TICKER'):
        hashpart += 'f' + (parts.get('FILTER', '') + ' ' + parts.get('TICKER', '')).strip() + ':'

    suggested_url = url + hashpart.rstrip(':')
    print('Suggestion: ' + suggested_url + ' ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return jsonify({'status': 'success',
                    'result': suggested_url})
