from flask import Flask, request
from dotenv import load_dotenv
from pytgbot.api_types.receivable.updates import Update
from tgbot import handle_update


load_dotenv()
app = Flask(__name__)


@app.route("/")
def index():
    return "ok"


@app.route("/webhook", methods=["POST"])
def handle_webhook():
    update = Update.from_array(request.json)
    handle_update(update)
    return "ok", 200
