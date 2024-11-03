from flask import request, Blueprint, jsonify, current_app
from flask_login import current_user
from datetime import datetime
from urllib.parse import urlparse
from openai import OpenAI
from api.utils.rate_limiter import limiter
from . import safety_classifier


bp = Blueprint('ainavigator', __name__,
               template_folder='templates',
               static_folder='static', static_url_path='/ainavigator/static')

# this sets rate limmit for entire blueprint, including static files
# limiter.limit("1/minute")(bp)

@bp.route('/forinrobot', methods=['POST', 'GET'])
@limiter.limit('20/minute')
def robot():
    client = OpenAI(api_key=current_app.config['OPENAI_API_KEY'])
    engine = current_app.config.get('OPENAI_DEFAULT_ENGINE', 'gpt-3.5-turbo')
    temperature = current_app.config.get('OPENAI_DEFAULT_TEMPERATURE', '0')

    # # List Engines (Models)
    # engines = openai.Engine.list()
    # # Print all engines IDs
    # for engine in engines.data:
    #     print(engine.id)

    user_prompt = request.form.to_dict()['input_query']
    user_prompt = user_prompt.strip().replace('\n', ' ').replace('\r', '')

    if not user_prompt:
        return jsonify({'status': 'error', 'result': ''}), 400

    if len(user_prompt) > 500:
        return jsonify({'status': 'error',
                        'result': 'Prompt too long, more than 500 characters.'}), 400

    # pre-request content filtering
    content_safety_class = safety_classifier.classify(user_prompt)
    if content_safety_class == '2':
        return jsonify({'status': 'error', 'result': 'Can\'t do that'}), 400

    print('Prompt: ' + user_prompt)

    user_identifier = str(getattr(current_user, 'id', 0))
    # Create a completion, return results streaming as they are generated.
    # Run with `python3 -u` to ensure unbuffered output.
    completion = client.chat.completions.create(
        model=engine,
        messages=[
{'role': 'system',
 'content': """We will classify INPUT intent to range of known values and organize them in class parts:
[BASE]
[COLUMN]
[DIRECTION]
[LIMIT]
[FILTER].

Purpose it to provide navigation parameters to be used in navigation to BASE page, operations on grid, filtering by content displayed in grid and < > operators for numeric values.

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
[TICKER] = acceptable value"""
},
{'role': 'user',
 'content': """show trade list for ADA"""
},
{'role': 'assistant',
 'content': 
"""[BASE]: trades
[FILTER]: ADAUSDT"""
},
{'role': 'user',
 'content': """coin trader buy/sells analytics, ordered descending by symbol"""
},
{'role': 'assistant',
 'content': """[BASE]: positions
[COLUMN]: symbol
[DIRECTION]: od"""
},
{'role': 'user',
 'content': """coin trader buy/sells analytics, ordered ascending by symbol"""
},
{'role': 'assistant',
 'content': """[BASE]: positions
[COLUMN]: symbol
[DIRECTION]: od"""
},
{'role': 'user',
 'content': """profit visualization, 25 results, sorted by direction from lower to higher"""
},
{'role': 'assistant',
 'content': """[BASE]: profitloss
[COLUMN]: direction
[DIRECTION]: oa
[LIMIT]: l25"""
},
{'role': 'user',
 'content': """list trades, fifty rows sort by direction field made by Clickherenow"""
},
{'role': 'assistant',
 'content': """[BASE]: trades
[COLUMN]: direction
[LIMIT]: l50
[FILTER]: Clickherenow"""
},
{'role': 'user',
 'content': user_prompt
},
            ],
        max_tokens=100,
        temperature=temperature,
        stop=['INPUT:'],
        user=user_identifier,
        stream=False)

    suggested_response = completion.choices[0].message.content.strip().replace(' ', '')

    # recommended content filtering
    content_safety_class = safety_classifier.classify(suggested_response)
    if content_safety_class == '2':
        return jsonify({'status': 'error', 'result': 'Can\'t do that'}), 400

    parts = {ct.split(']:')[0].lstrip('['): ct.split(']:')[1]
             for ct in suggested_response.split('\n')}

    if request.referrer:
        current_url = url_parse(request.referrer)
        current_base = current_url.path.lstrip('/')

    if not parts.get('BASE', current_base):
        return jsonify({'status': 'error', 'result': 'Try to explain better'}), 400

    url = '/' + parts.get('BASE', current_base)

    hashpart = ''
    # if we have other parts that base url path
    if len(parts) > (1 if parts.get('BASE') else 0):
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
