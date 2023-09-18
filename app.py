from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from telegram import Bot
import asyncio
import os

app = Flask(__name__)
app.debug = True
Bootstrap(app)

# 환경 변수에서 토큰과 채팅 ID를 가져옵니다.

TELEGRAM_BOT_TOKEN = os.environ.get('6560335312:AAHo82hdFJr1q_6CKUkms7NkL68kwgMul08')  # 환경 변수에서 봇 토큰 가져오기
TELEGRAM_CHAT_ID = os.environ.get('71046013')  # 환경 변수에서 채팅 ID 가져오기

# 환경 변수가 설정되어 있지 않으면 기본 값을 사용합니다.
if not TELEGRAM_BOT_TOKEN:
    TELEGRAM_BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'  # 본인의 봇 토큰으로 대체

if not TELEGRAM_CHAT_ID:
    TELEGRAM_CHAT_ID = 'YOUR_CHAT_ID_HERE'  # 본인의 채팅 ID로 대체

bot = Bot(token=TELEGRAM_BOT_TOKEN)  # 봇 객체 초기화

async def send_telegram_message(message):
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

@app.route('/')
def home():
    return render_template('report.html')

@app.route('/submit', methods=['POST'])
def submit():
    reporter = request.form['reporterName']
    location = request.form['reportLocation']
    complaint = request.form['complaint']

    message = f'신고인: {reporter}\n신고위치: {location}\n신고사항: {complaint}'

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(send_telegram_message(message))
    except Exception as e:
        error_message = f'오류 발생: {str(e)}'
        return render_template('error.html', error_message=error_message)

    return render_template('success.html')

if __name__ == '__main__':
    try:
        app.run()
    except Exception as e:
        print('An error occurred:', str(e))
