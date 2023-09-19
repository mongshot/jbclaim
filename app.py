from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# 데이터베이스 모델 정의
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

# 루트 경로
@app.route('/')
def home():
    cars = Car.query.filter_by(available=True).all()
    return render_template('index.html', cars=cars)

# 관리자 페이지
@app.route('/admin')
def admin():
    cars = Car.query.all()
    return render_template('admin.html', cars=cars)

# 차량 정보 업데이트
@app.route('/admin/update/<int:car_id>', methods=['POST'])
def update_car(car_id):
    car = Car.query.get_or_404(car_id)

    # 차량 번호를 숫자로 업데이트
    car.id = int(request.form['new_car_id'])
    car.name = request.form['new_car_name']
    db.session.commit()

    flash(f'차량 정보가 업데이트되었습니다. (ID: {car.id})', 'success')
    return redirect(url_for('admin'))

# 예약 취소
@app.route('/cancel_reservation/<int:reservation_id>')
def cancel_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    car = reservation.car
    car.available = True
    db.session.delete(reservation)
    db.session.commit()

    flash('예약이 취소되었습니다.', 'success')
    return redirect(url_for('home'))

# 차량 예약
@app.route('/reserve/<int:car_id>/<time_slot>', methods=['POST'])
def reserve(car_id, time_slot):
    car = Car.query.get_or_404(car_id)

    if car.available:
        reservation_name = request.form.get('reservation_name', '')

        if reservation_name:
            car.available = False
            car.reservation_id = len(Reservation.query.all()) + 1
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

# 차량 등록
@app.route('/register_car', methods=['GET', 'POST'])
def register_car():
    if request.method == 'POST':
        car_name = request.form['car_name']
        if car_name:
            car = Car(name=car_name, available=True)
            db.session.add(car)
            db.session.commit()
            flash(f'{car_name} 차량이 등록되었습니다.', 'success')
            return redirect(url_for('admin'))
        else:
            flash('차량 이름을 입력하세요.', 'danger')
    return render_template('register_car.html')

if __name__ == '__main__':
    app.run(debug=True)
