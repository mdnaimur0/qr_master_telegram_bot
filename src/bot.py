from pytgbot import Bot
from models import User
from pytgbot.api_types.receivable.updates import Update, Message
from pytgbot.api_types.sendable.files import InputFileFromDisk
import os, strings, qrcode_util, time, db

bot = Bot(os.getenv("BOT_TOKEN"))

IS_SERVICE_AVAILABLE = True


def get_updates(offset):
    return bot.get_updates(poll_timeout=10 * 60, error_as_empty=True, offset=offset)


def handle_update(update: Update):
    if update.message is not None:
        message: Message = update.message

        chat_id, _ = get_id(message)
        user = db.get_user(chat_id)
        if user is None:
            db.add_user(get_user_from_message(message))

        if message.text is not None:
            if message.text.startswith("/"):
                handle_command(message)
            else:
                handle_text_message(message)
        else:
            handle_nontext_message(message)


def handle_text_message(message: Message):
    chat_id, msg_id = get_id(message)
    _ = set_typing(chat_id)

    if IS_SERVICE_AVAILABLE == False:
        bot.send_message(
            chat_id=chat_id,
            text="Service is currently unavailable.I will let you know when it's available.Thanks for your patience.",
        )
        return

    file_name = os.path.join("temp", str(int(time.time())) + ".png")
    status, msg = qrcode_util.generate_qr_code(message.text, file_name)

    if status:
        bot.send_photo(
            chat_id=chat_id,
            photo=InputFileFromDisk(path=file_name, mime="image/png"),
            caption="Here is your QR Code!",
            reply_to_message_id=msg_id,
        )
        os.remove(file_name)
    else:
        bot.send_message(
            chat_id=chat_id,
            text=msg,
            reply_to_message_id=msg_id,
        )


def handle_command(message: Message):
    chat_id, msg_id = get_id(message)
    text = message.text

    user = db.get_user(chat_id)
    if user is None:
        db.add_user(get_user_from_message(message))

    if text.startswith("/start"):
        text, parse_mode = strings.get_new_user_start_command_reply()
        bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode)

    elif text.startswith("/help"):
        text, parse_mode = strings.get_help_command_reply()
        bot.send_message(text=text, chat_id=chat_id, parse_mode=parse_mode)

    elif text.startswith("/qr"):
        text = text.replace("/qr", "").strip()
        if text == "":
            bot.send_message(
                chat_id=chat_id,
                text="Please provide some text to generate QR Code!",
                reply_to_message_id=msg_id,
            )
            return
        message.text = text
        handle_text_message(message)

    else:
        bot.send_message(
            chat_id=chat_id, text="Invalid command!", reply_to_message_id=msg_id
        )


def get_user_from_message(message: Message) -> User:
    chat_id, _ = get_id(message)
    name = get_user_name(message)
    username = message.from_peer.username
    return User(None, str(chat_id), name, username)


def handle_nontext_message(message: Message):
    chat_id, msg_id = get_id(message)

    if message.photo is not None:
        file_id = message.photo[0].file_id
        file = bot.get_file(file_id)
        url = file.get_download_url(os.getenv("BOT_TOKEN"))
        _ = set_typing(chat_id)
        text = qrcode_util.extract_text_from_qr_code_url(url)
        bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_to_message_id=msg_id,
        )
    else:
        bot.send_message(
            chat_id=chat_id,
            text="I can't understand this message format!",
            reply_to_message_id=msg_id,
        )


def get_message(update: Update) -> Message:
    if update.message is not None:
        return update.message
    elif update.callback_query is not None:
        return update.callback_query.message
    return None


def get_id(message: Message):
    if message is None:
        return -1, -1
    return message.chat.id, message.message_id


def get_user_name(message: Message):
    fname = message.from_peer.first_name
    lname = message.from_peer.last_name
    name = fname + (" " + lname if lname is not None else "")
    return name


def set_typing(chat_id):
    return bot.send_chat_action(chat_id=chat_id, action="typing")
