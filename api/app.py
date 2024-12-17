from threading import Thread
from flask import Flask, jsonify
from flask_cors import CORS
from .CalculateMostProfitableCrafts import GetMostProfitableCrafts
from .CalculateMostProfitableCrafts import StartCalculatingMostProfitableCrafts

app = Flask(__name__)
CORS(app)

def RunMostProfitableCraftsInBackground():
    thr = Thread(target=StartCalculatingMostProfitableCrafts)
    thr.start()
    return thr

@app.route('/')
def index():
    return "Hello world!"

@app.route("/topProfit", methods=['GET'])
def get_top_profit():
    return jsonify(GetMostProfitableCrafts())


def __main__():
    RunMostProfitableCraftsInBackground()
    app.run(debug=True, host='0.0.0.0')
__main__()