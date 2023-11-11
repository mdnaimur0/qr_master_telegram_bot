from flask import Flask, request
import bot
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)


@app.route("/")
def index():
    return "ok", 200


@app.route("/webhook", methods=["POST"])
def handle_webhook():
    update = bot.Update.from_array(request.json)
    bot.handle_update(update)
    return "ok", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0")
