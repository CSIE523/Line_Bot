import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage


from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["user", "start", "expense", "climate", "news", "thingandcost","storedata", "printtotal", "clear",
            "north", "west", "south", "Taipei", "NewTaipei", "Taoyuan", "Taichung", "Tainan", "Kaohsiung"
           ],
    transitions=[
        {
            "trigger": "advance", "source": "user",
            "dest": "start", "conditions": "is_going_to_start",
        },
        # first
        {
            "trigger": "advance", "source": "start",
            "dest": "expense", "conditions": "is_going_to_expense",
        },
        {
            "trigger": "advance", "source": "start",
            "dest": "climate", "conditions": "is_going_to_climate",
        },
        {
            "trigger": "advance", "source": "start",
            "dest": "news", "conditions": "is_going_to_news",
        },

        # second expense
        {
            "trigger": "advance", "source": "expense",
            "dest": "thingandcost", "conditions": "is_going_to_thingandcost",
        },
        {
            "trigger": "advance", "source": "expense",
            "dest": "printtotal", "conditions": "is_going_to_printtotal",
        },
        {
            "trigger": "advance", "source": "expense",
            "dest": "clear", "conditions": "is_going_to_clear",
        },
        # third expense
        {
            "trigger": "advance", "source": "thingandcost",
            "dest": "storedata", "conditions": "is_going_to_storedata",
        },
        # second climate
        {
            "trigger": "advance", "source": "climate",
            "dest": "north", "conditions": "is_going_to_north",
        },
        {
            "trigger": "advance", "source": "climate",
            "dest": "west", "conditions": "is_going_to_west",
        },
        {
            "trigger": "advance", "source": "climate",
            "dest": "south", "conditions": "is_going_to_south",
        },

        # third climate
        {
            "trigger": "advance", "source": "north",
            "dest": "Taipei", "conditions": "is_going_to_Taipei",
        },
        {
            "trigger": "advance", "source": "north",
            "dest": "NewTaipei", "conditions": "is_going_to_NewTaipei",
        },
        {
            "trigger": "advance", "source": "north",
            "dest": "Taoyuan", "conditions": "is_going_to_Taoyuan",
        },
        {
            "trigger": "advance", "source": "west",
            "dest": "Taichung", "conditions": "is_going_to_Taichung",
        },
        {
            "trigger": "advance", "source": "south",
            "dest": "Tainan", "conditions": "is_going_to_Tainan",
        },
        {
            "trigger": "advance", "source": "south",
            "dest": "Kaohsiung", "conditions": "is_going_to_Kaohsiung",
        },

        # final
        {
            "trigger": "go_back",
            "source": ["storedata", "printtotal", "clear", "Taipei", "NewTaipei", "Taoyuan", "Taichung", "Tainan", "Kaohsiung", "news"],
            "dest": "user"
        },
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue

        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)

        if response == False:
            send_text_message(event.reply_token, "格式錯誤，請重新輸入!(如果是一開始，請輸入""你好""來開始服務)")

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "格式錯誤，請重新輸入")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
