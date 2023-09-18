from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 보안을 위한 시크릿 키
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myapp.db'  # SQLite 데이터베이스 설정
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    available = db.Column(db.Boolean, default=True)
    reservation_id = db.Column(db.Integer, nullable=True)
    reservation_name = db.Column(db.String(100), nullable=True)
    reservation_info = db.Column(db.String(255), nullable=True)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, nullable=False)
    time_slot = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def home():
    cars = Car.query.all()
    return render_template('index.html', cars=cars)

@app.route('/admin')
def admin():
    cars = Car.query.all()
    return render_template('admin.html', cars=cars)

@app.route('/admin/update/<int:car_id>', methods=['POST'])
def update_car(car_id):
    new_car_id = str(request.form['new_car_id'])

    # 차량 정보 업데이트
    car = Car.query.get_or_404(car_id)
    car.name = request.form['new_car_name']
    car.id = new_car_id  # 차량 번호를 문자열로 업데이트
    db.session.commit()

    flash(f'차량 정보가 업데이트되었습니다. (ID: {new_car_id})', 'success')
    return redirect(url_for('admin'))

@app.route('/cancel_reservation/<int:reservation_id>')
def cancel_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    car = Car.query.get_or_404(reservation.car_id)

    # 차량 상태 변경 및 예약 정보 제거
    car.available = True
    car.reservation_id = None
    car.reservation_name = None
    db.session.delete(reservation)
    db.session.commit()

    flash('예약이 취소되었습니다.', 'success')
    return redirect(url_for('home'))

@app.route('/reserve/<int:car_id>/<time_slot>', methods=['POST'])
def reserve(car_id, time_slot):
    car = Car.query.get_or_404(car_id)

    if car.available:
        reservation_name = request.form.get('reservation_name', '')  # 예약자명 추출

        if reservation_name:
            car.available = False
            car.reservation_id = len(Reservation.query.all()) + 1  # 예약 ID 생성
            car.reservation_name = reservation_name

            reservation = Reservation(car_id=car.id, time_slot=time_slot)
            db.session.add(reservation)
            db.session.commit()

            flash(f'{reservation_name} 님의 예약이 완료되었습니다.', 'success')
        else:
            flash('예약자명을 입력하세요.', 'danger')
    else:
        flash('이미 예약된 차량입니다.', 'danger')

    return redirect(url_for('home'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
