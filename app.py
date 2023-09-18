from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 보안을 위한 시크릿 키

# 간단한 차량 데이터베이스
cars = [
    {'id': 1, 'name': 'Car 1', 'available': True, 'reservation_id': None},
    {'id': 2, 'name': 'Car 2', 'available': True, 'reservation_id': None},
    {'id': 3, 'name': 'Car 3', 'available': True, 'reservation_id': None},
    {'id': 4, 'name': 'Car 4', 'available': True, 'reservation_id': None},
    {'id': 5, 'name': 'Car 5', 'available': True, 'reservation_id': None},
    {'id': 6, 'name': 'Car 6', 'available': True, 'reservation_id': None},
    {'id': 7, 'name': 'Car 7', 'available': True, 'reservation_id': None}
]

# 간단한 예약 데이터베이스
reservations = []

@app.route('/')
def home():
    return render_template('index.html', cars=cars, reservations=reservations)
@app.route('/admin')
def admin():
    return render_template('admin.html', cars=cars)
@app.route('/admin/update/<int:car_id>', methods=['POST'])
def update_car(car_id):
    new_car_id = request.form['new_car_id']
    new_car_name = request.form['new_car_name']

    # 입력된 차량 번호가 형식에 맞는지 확인
    if not re.match(r'^\d{3}[가-힣]\d{4}$', new_car_id):
        flash('올바른 차량 번호 형식을 입력하세요 (예: 123가1234).', 'danger')
    else:
        # 해당 차량을 찾아서 수정
        for car in cars:
            if car['id'] == car_id:
                car['id'] = new_car_id
                car['name'] = new_car_name

        flash('차량 정보가 수정되었습니다.', 'success')
    return redirect(url_for('admin'))

@app.route('/cancel/<int:reservation_id>')
def cancel_reservation(reservation_id):
    reservation = next((r for r in reservations if r.get('id') == reservation_id), None)
    if reservation:
        car_id = reservation['car_id']
        car = next((c for c in cars if c['id'] == car_id), None)
        if car:
            # 차량 상태 변경 및 예약 정보 제거
            car['available'] = True
            car['reservation_id'] = None
            reservations.remove(reservation)
            flash('예약이 취소되었습니다.', 'success')
        else:
            flash('차량을 찾을 수 없습니다.', 'danger')
    else:
        flash('예약을 찾을 수 없습니다.', 'danger')
    return redirect(url_for('home'))

@app.route('/reserve/<int:car_id>/<time_slot>', methods=['POST'])
def reserve(car_id, time_slot):
    car = next((c for c in cars if c['id'] == car_id), None)
    if car:
        if car['available']:
            reservation_name = request.form.get('reservation_name')  # 입력 필드에서 예약자명 추출
            if reservation_name:
                car['available'] = False
                car['reservation_id'] = len(reservations) + 1  # 예약 ID 생성
                car['reservation_name'] = reservation_name  # 예약자명 저장
                reservations.append({'id': len(reservations) + 1, 'car_id': car_id, 'time_slot': time_slot, 'timestamp': datetime.now()})
                flash(f'{reservation_name} 님의 예약이 완료되었습니다.', 'success')
            else:
                flash('예약자명을 입력하세요.', 'danger')
        else:
            flash('이미 예약된 차량입니다.', 'danger')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
