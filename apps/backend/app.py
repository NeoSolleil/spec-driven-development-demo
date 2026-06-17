"""あいさつAPIサーバー（Flask）"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from greeting import GreetingService

app = Flask(__name__)
CORS(app)  # FE(別ポート)からの呼び出しを許可
service = GreetingService()

@app.route("/greet", methods=["POST"])
def greet():
    number = request.json.get("number")
    message = service.greet(number)
    return jsonify({"message": message})

@app.route("/history", methods=["GET"])
def history():
    return jsonify({"history": service.history()})

if __name__ == "__main__":
    app.run(port=5001)
