from flask import Flask, render_template, request
from telegram import Bot
import asyncio
import os  # 환경 변수 사용을 위해 os 모듈을 가져옵니다.

app = Flask(__name__)
app.debug = True

# 환경 변수에서 토큰과 채팅 ID를 가져옵니다.
TELEGRAM_BOT_TOKEN = '6560335312:AAHo82hdFJr1q_6CKUkms7NkL68kwgMul08'
TELEGRAM_CHAT_ID = '71046013'

# 환경 변수가 설정되어 있지 않으면 기본 값을 사용합니다.
if not TELEGRAM_BOT_TOKEN:
    TELEGRAM_BOT_TOKEN = 'YOUR_DEFAULT_BOT_TOKEN'

if not TELEGRAM_CHAT_ID:
    TELEGRAM_CHAT_ID = 'YOUR_DEFAULT_CHAT_ID'

bot = Bot(token=TELEGRAM_BOT_TOKEN)

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
        # 예외 처리를 통해 오류 메시지를 기록하고 사용자에게 오류를 알릴 수 있습니다.
        error_message = f'오류 발생: {str(e)}'
        return error_message

    return '신고가 접수되었습니다. 감사합니다!'

async def send_telegram_message(message):
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

if __name__ == '__main__':
    try:
        app.run()
    except Exception as e:
        print('An error occurred:', str(e))
