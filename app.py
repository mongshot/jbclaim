from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 보안을 위한 시크릿 키
app.config['TEMPLATES_AUTO_RELOAD'] = True

# 간단한 차량 데이터베이스
cars = [
    {'id': 4836, 'name': '넥소', 'available': True, 'reservation_id': None},
    {'id': 7385, 'name': '카니발', 'available': True, 'reservation_id': None},
    {'id': 8636, 'name': '카니발', 'available': True, 'reservation_id': None},
    {'id': 2055, 'name': '아반떼', 'available': True, 'reservation_id': None},
    {'id': 6739, 'name': '아반떼', 'available': True, 'reservation_id': None},
    {'id': 3694, 'name': '아반떼', 'available': True, 'reservation_id': None},
    {'id': 6599, 'name': '투싼', 'available': True, 'reservation_id': None}
]

# 간단한 예약 데이터베이스
reservations = []

@app.route('/')
def home():
    return render_template('index.html', cars=cars, reservations=reservations)

@app.route('/admin')
def admin():
    return render_template('admin.html', cars=cars)

@app.route('/admin/update/<car_id>', methods=['POST'])
def update_car(car_id):
    new_car_id = str(request.form['new_car_id'])

    # 차량 정보 업데이트
    for car in cars:
        if car['id'] == int(car_id):
            car['name'] = request.form['new_car_name']
            car['id'] = new_car_id  # 차량 번호를 문자열로 업데이트

    flash(f'차량 정보가 업데이트되었습니다. (ID: {new_car_id})', 'success')
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
            reservation_name = request.form.get('reservation_name', '')  # 예약자명 추출
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
