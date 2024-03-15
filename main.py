from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

# LINE 聊天機器人的基本資料
# config = configparser.ConfigParser()
# config.read('config.ini')

# Channel Access Token
line_bot_api = LineBotApi('lVMUiuEAymtA+dgjoUwauGFazYhX2rECvymHZoo6ETV3zSLKcvgB/Njc7WqdG8s9mnUa7EHi6UAK8G2XcG9xh6ZtDvGbZBboM+Qv+680Ak18DDakZpfoYbOzeP5CY5sF9mPw0v8bs1iP+OGF6bxucgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('d84c840557e2620b4a5a2b1160bfd725')


# 接收 LINE 的資訊
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
        abort(400)
    return 'OK'

# 學你說話
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token,message)

import os
if __name__ == "__main__":
    app.run()