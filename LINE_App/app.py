from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction
)

from decouple import config

app = Flask(__name__)

line_bot_api = LineBotApi(config('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(config('CHANNEL_SECRET'))


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == '@Fund':
        text_message = TextSendMessage(text='Select a fund category', quick_reply=QuickReply(items=[
            QuickReplyButton(action=MessageAction(label="TW", text="@Fund-tw")),
            QuickReplyButton(action=MessageAction(label="US", text="@Fund-us")),
        ]))

        line_bot_api.reply_message(
            event.reply_token,
            text_message)
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
