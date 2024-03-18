# encoding: utf-8
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

import pymysql
from datetime import date, timedelta

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
    # 連線到資料庫
    connection = pymysql.connect(
        host='localhost',
        user='user',
        password='password',
        db='new_media',
        cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        # 建立游標
        cursor = connection.cursor()
        event_text = event.message.text
        text = ""
        text_array = []
        # 判斷訊息類型
        # 2024-03-18 post inside
        if (event_text.find("post") != -1):
            query = event_text.split(' ')[0]
            source = event_text.split(' ')[2]
            if( query == 'week' ):
                time = str(date.today() - timedelta(weeks=1))
                sql = '''SELECT * FROM new_media.media_posts WHERE source = '{}' AND date >= '{}' '''.format(source, time)
                cursor.execute(sql)
                posts = cursor.fetchall()
                for post in posts:
                    text += "{},相關tag:{},來源:{},日期:{}\n\n".format(
                        post['title'].strip(),
                        post['tags'],
                        post['source'],
                        post['date'])
                    # 判斷回應訊息長度
                    if (len(text) > 1000):
                        text_array.append(TextSendMessage(text=text))
                        text = ""
                    elif (post == posts[-1]):
                        text_array.append(TextSendMessage(text=text))
                        text = ""
            else:
                sql = '''SELECT * FROM new_media.media_posts WHERE source = '{}' AND date = '{}' '''.format(source, query)
                cursor.execute(sql)
                posts = cursor.fetchall()
                for post in posts:
                    text += "{},相關tag:{},來源:{},日期:{}\n\n".format(
                        post['title'].strip(),
                        post['tags'],
                        post['source'],
                        post['date'])
                    # 判斷回應訊息長度
                    if (len(text) > 1000):
                        text_array.append(TextSendMessage(text=text))
                        text = ""
                    elif (post == posts[-1]):
                        text_array.append(TextSendMessage(text=text))
                        text = ""
        else:
            text_array.append(TextSendMessage(text='看謀啦～'))

    # message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token,text_array)

    connection.close()

import os
if __name__ == "__main__":
    app.run()