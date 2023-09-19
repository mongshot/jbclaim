from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# CSV 파일에서 데이터 읽기
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"File {file_path} not found. Creating an empty DataFrame.")
        return pd.DataFrame(columns=['vehicle_id', 'make', 'model', 'year', 'available'])

# 차량 데이터 추가
def add_vehicle(data, vehicle_id, make, model, year, available):
    new_row = {'vehicle_id': vehicle_id, 'make': make, 'model': model, 'year': year, 'available': available}
    data = data.append(new_row, ignore_index=True)
    return data

# 차량 데이터 저장
def save_data(data, file_path):
    data.to_csv(file_path, index=False)

# 차량 예약
@app.route('/reserve', methods=['POST'])
def reserve():
    vehicle_id = int(request.form['vehicle_id'])

    # 차량 데이터를 불러오고 예약 상태를 변경합니다.
    csv_file = "vehicles.csv"
    vehicle_data = load_data(csv_file)
    
    # 예약 가능한 차량인지 확인합니다.
    row = vehicle_data.loc[vehicle_data['vehicle_id'] == vehicle_id].iloc[0]
    if row['available'] == 'Yes':
        vehicle_data.loc[vehicle_data['vehicle_id'] == vehicle_id, 'available'] = 'No'
        save_data(vehicle_data, csv_file)
        return redirect(url_for('index'))
    else:
        return "이 차량은 이미 예약되었습니다."

# 웹 페이지 렌더링
@app.route('/')
def index():
    csv_file = "vehicles.csv"
    vehicle_data = load_data(csv_file)
    return render_template('index.html', vehicle_data=vehicle_data)

# 차량 데이터 추가
@app.route('/add_vehicle', methods=['POST'])
def add_vehicle_route():
    vehicle_id = int(request.form['vehicle_id'])
    make = request.form['make']
    model = request.form['model']
    year = int(request.form['year'])
    available = request.form['available']

    csv_file = "vehicles.csv"
    vehicle_data = load_data(csv_file)
    vehicle_data = add_vehicle(vehicle_data, vehicle_id, make, model, year, available)
    save_data(vehicle_data, csv_file)

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
