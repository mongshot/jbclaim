from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 보안을 위한 시크릿 키

# 간단한 차량 데이터베이스
cars = [
    {'id': 1, 'name': 'Car 1', 'available': True},
    {'id': 2, 'name': 'Car 2', 'available': True},
    {'id': 3, 'name': 'Car 3', 'available': True},
    {'id': 4, 'name': 'Car 4', 'available': True},
    {'id': 5, 'name': 'Car 5', 'available': True},
    {'id': 6, 'name': 'Car 6', 'available': True},
    {'id': 7, 'name': 'Car 7', 'available': True}
]

# 간단한 예약 데이터베이스
reservations = []

@app.route('/')
def home():
    return render_template('index.html', cars=cars)

@app.route('/cancel/<int:reservation_id>')
def cancel_reservation(reservation_id):
    reservation = next((r for r in reservations if r.get('id') == reservation_id), None)
    if reservation:
        car_id = reservation['car_id']
        car = next((c for c in cars if c['id'] == car_id), None)
        if car:
            # 로그 추가: 예약 정보 확인
            print(f"Cancelling reservation ID {reservation_id} for car ID {car_id}")
            # 로그 추가: 차량 상태 변경
            print(f"Setting car ID {car_id} to available")
            car['available'] = True
            car['reservation_id'] = None
            reservations.remove(reservation)
            flash('예약이 취소되었습니다.', 'success')
        else:
            flash('차량을 찾을 수 없습니다.', 'danger')
    else:
        flash('예약을 찾을 수 없습니다.', 'danger')
    return redirect(url_for('home'))



@app.route('/reserve/<int:car_id>/<time_slot>')
def reserve(car_id, time_slot):
    car = next((c for c in cars if c['id'] == car_id), None)
    if car:
        if car['available']:
            car['available'] = False
            reservations.append({'car_id': car_id, 'time_slot': time_slot, 'timestamp': datetime.now()})
            flash('예약이 완료되었습니다.', 'success')
        else:
            flash('이미 예약된 차량입니다.', 'danger')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
