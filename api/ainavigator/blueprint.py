from flask import request, Blueprint, jsonify, current_app
import openai

bp = Blueprint('ainavigator', __name__,
               template_folder='templates',
               static_folder='static', static_url_path='/ainavigator/static')

@bp.route("/forinrobot", methods=['POST'])
def robot():
    openai.api_key = current_app.config['OPENAI_API_KEY']
    openai.api_base = current_app.config['OPENAI_BASE_ADDRESS']
    engine = current_app.config.get('OPENAI_DEFAULT_ENGINE', "gpt-j-6b")

    # # List Engines (Models)
    # engines = openai.Engine.list()
    # # Print all engines IDs
    # for engine in engines.data:
    #     print(engine.id)

    user_prompt = request.form.to_dict()['input_query']
    if not user_prompt:
        return jsonify({"status": "error", "result": ""}), 400

    prompt = f"""Website has different views, dependin on their purpose in cryptocarency trading analytics app.
Each view enables activities related to its description.
Here is a complete list of views available:

-Category: analytics and visualizations. Contains all visualisations and analysis.
URL: "/profitloss"
Usecase: Estimated profit and loss for all traders, trader profiability, trader quality, trader visualization
URL: "/transactions"
Usecase: Transaction sizes by position size and price, volume of trades, big players, small players, transaction visualization
URL: "/tradedvalue"
Usecase: Value traded per coins (securities), who traded in what quantity, which crypto currency has most traded value
URL: "/tradeactivity"
Usecase: Number of trades per coin, which crypto currency has most trades

-Category: estimated trades and positions
URL: "/positions"
Usecase: Known positions that traders hold at this moment, list of positions, trader portfolio, owned crypto currencies
URL: "/trades"
Usecase: View of esitimated trades, crypto buyin and selling, transactions made by trader

-Category: traders in the system
URL: "/traders"
Usecase: List of trader profiles, players

Q: If i want to see profit
URL: /profitloss
Q: show me who is profitable
URL: /profitloss
Q: show me value of IBM stock
URL: /
Q: show me most traded coins
URL: /tradedvalue
Q: show me what trader has in his potfolio
URL: /positions
Q: {user_prompt}
URL:"""


#     prompt = f"""Website has different views, dependin on their purpose in cryptocarency trading analytics app.
# Each view enables activities related to its description. Url is composed of view address and query parameters that define specifics of how to view the data.
# Here is a complete list of views available:

# Query parameters: 
# oa = order ascending
# od = order descending
# l10 = 10 results
# l25 = 25 results
# l50 = 50 results
# l100 = 100 results
# Suffix:
# 0=symbol
# 1=position entry price
# 2=amount
# 3=position size
# 4=time
# 5=trader
# 6=active

# Query pareter separator is ":".

# -Category: analytics and visualizations. Contains all visualisations and analysis.
# URL: /profitloss
# Usecase: Estimated profit and loss for all traders, trader profiability, trader quality, trader visualization
# URL: /transactions
# Usecase: Transaction sizes by position size and price, volume of trades, big players, small players, transaction visualization
# URL: /tradedvalue
# Usecase: Value traded per coins (securities), who traded in what quantity, which crypto currency has most traded value
# URL: /tradeactivity
# Usecase: Number of trades per coin, which crypto currency has most trades

# -Category: estimated trades and positions
# URL: /positions
# Usecase: Known positions that traders hold at this moment, list of positions, trader portfolio, owned crypto currencies
# URL: /trades
# Usecase: View of esitimated trades, crypto buyin and selling, transactions made by trader

# -Category: traders in the system
# URL: /traders
# Usecase: List of trader profiles, players

# Q: If i want to see profit
# URL: /profitloss
# Q: show me who is profitable
# URL: /profitloss
# Q: show me value of IBM stock
# URL: /
# Q: show me most traded coins
# URL: /tradedvalue
# Q: show me what trader has in his potfolio
# URL: /positions
# Q:  coin trader buy/sells analytics, 25 results
# URL: /positions#datatable=l25
# Q:  coin trader buy/sells analytics, ordered descending by symbol
# URL: /positions#datatable=od0
# Q:  coin trader buy/sells analytics, ordered ascending by symbol
# URL: /positions#datatable=oa0
# Q:  coin trader buy/sells analytics, ordered ascending by amount
# URL: /positions#datatable=oa2
# Q:  profits, 50 rows by amount
# URL: /profitloss#datatable=l50:oa2
# Q: {user_prompt}
# URL:"""

    # Create a completion, return results streaming as they are generated.
    # Run with `python3 -u` to ensure unbuffered output.
    completion = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        max_tokens=5,
        temperature=0.05,
        stop=["\n", " "],
        stream=False)

    suggested_url = completion.choices[0].text.strip()
    print("Suggestion: " + suggested_url)
    return jsonify({"status": "ok",
                    "result": suggested_url})
