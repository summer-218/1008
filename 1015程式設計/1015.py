from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 設定你的 Line Bot 的 Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = 'jDZrhrfWoMnBOxo5voRhKfKSDhyUp6bTsgORwPl/duMpaWpyfIkXWw8f/cX0Lu89JIsQ2Jka4RpctK8jSeeMF8qstzepMBU9TRKTeA4sVCR2XAAkAhbzScrEgWxxs488CeDRVkd2LHJcCchyTu5HGAdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = 'b67b622c8c25443c1282d8b6b1556ff5'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
webhook_handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # 獲取 Line 平台傳來的簽名
    signature = request.headers['X-Line-Signature']

    # 獲取請求的內容
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 驗證簽名並處理請求
    try:
        webhook_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@webhook_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 回應相同的訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text + " 你也好！")
    )

if __name__ == "__main__":
    app.run(port=5000)