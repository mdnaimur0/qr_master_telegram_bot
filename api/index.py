from flask import Flask, request
import tgbot
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)


@app.route("/")
def index():
    return "ok"


@app.route("/webhook", methods=["POST"])
def handle_webhook():
    update = tgbot.Update.from_array(request.json)
    tgbot.handle_update(update)
    return "ok", 200