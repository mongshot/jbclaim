from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap  # Bootstrap 추가
from telegram import Bot
import asyncio
import os

app = Flask(__name__)
app.debug = True
Bootstrap(app)  # Bootstrap 초기화

# 나머지 코드는 그대로 유지됩니다.

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
        return render_template('error.html', error_message=error_message)  # 오류 템플릿으로 리다이렉트

    return render_template('success.html')  # 성공 템플릿으로 리다이렉트

# 나머지 코드는 그대로 유지됩니다.

if __name__ == '__main__':
    try:
        app.run()
    except Exception as e:
        print('An error occurred:', str(e))
