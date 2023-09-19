import pandas as pd

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

if __name__ == "__main__":
    csv_file = "vehicles.csv"
    vehicle_data = load_data(csv_file)

    while True:
        print("1. 차량 추가")
        print("2. 종료")
        choice = input("선택: ")

        if choice == "1":
            vehicle_id = int(input("차량 ID: "))
            make = input("제조사: ")
            model = input("모델: ")
            year = int(input("연식: "))
            available = input("사용 가능 여부 (Yes/No): ")

            vehicle_data = add_vehicle(vehicle_data, vehicle_id, make, model, year, available)
            save_data(vehicle_data, csv_file)
            print("차량이 추가되었습니다.")
        elif choice == "2":
            break
