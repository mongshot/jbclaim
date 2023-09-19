from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import datetime

app = Flask(__name__)

# CSV 파일에서 차량 및 예약 데이터 읽기
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"File {file_path} not found. Creating an empty DataFrame.")
        return pd.DataFrame(columns=['vehicle_id', 'make', 'model', 'year', 'available'])

def load_reservations(file_path):
    try:
        data = pd.read_csv(file_path)
        data['start_time'] = pd.to_datetime(data['start_time'])
        data['end_time'] = pd.to_datetime(data['end_time'])
        return data
    except FileNotFoundError:
        print(f"File {file_path} not found. Creating an empty DataFrame.")
        return pd.DataFrame(columns=['reservation_id', 'vehicle_id', 'user_id', 'start_time', 'end_time'])

# 차량 및 예약 데이터 저장
def save_data(data, file_path):
    data.to_csv(file_path, index=False)

# 예약 기능
@app.route('/reserve', methods=['POST'])
def reserve():
    vehicle_id = int(request.form['vehicle_id'])
    user_id = request.form['user_id']
    start_time = datetime.datetime.strptime(request.form['start_time'], '%Y-%m-%d %H:%M')
    end_time = datetime.datetime.strptime(request.form['end_time'], '%Y-%m-%d %H:%M')

    reservations = load_reservations('reservations.csv')

    # 예약이 가능한지 확인
    for index, row in reservations.iterrows():
        if row['vehicle_id'] == vehicle_id:
            if not (end_time <= row['start_time'] or start_time >= row['end_time']):
                return "이미 예약된 시간입니다."

    reservation_id = len(reservations) + 1
    new_reservation = {
        'reservation_id': reservation_id,
        'vehicle_id': vehicle_id,
        'user_id': user_id,
        'start_time': start_time,
        'end_time': end_time
    }

    reservations = reservations.append(new_reservation, ignore_index=True)
    save_data(reservations, 'reservations.csv')
    return "예약이 완료되었습니다."

# 예약 목록 표시
@app.route('/reservations')
def show_reservations():
    reservations = load_reservations('reservations.csv')
    return render_template('reservations.html', reservations=reservations)


if __name__ == "__main__":
    app.run(debug=True)
