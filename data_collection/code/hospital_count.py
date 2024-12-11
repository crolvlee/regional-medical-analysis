# 필요한 모듈 불러오기
import pandas as pd
import os

# 경로 설정
base_dir = os.path.dirname(os.path.abspath(__file__))
input_folder = os.path.join(base_dir, "../data_raw")
output_folder = os.path.join(base_dir, "../data_clean")

# 처리할 파일 이름 리스트
departments = ["내과", "소아청소년과", "산부인과", "신경과"]

# 출력 폴더 생성 (없을 경우)
os.makedirs(output_folder, exist_ok=True)

# 반복 작업
for dept in departments:
    input_file = os.path.join(input_folder, f"hospital_data_{dept}_sort.xlsx")
    output_file = os.path.join(output_folder, f"hospital_counts_{dept}.xlsx")
    
    # 데이터 읽기
    hospital_data = pd.read_excel(input_file)
    
    # "행정구역" 열 생성
    hospital_data["행정구역"] = hospital_data["행정기관(대)"] + " " + hospital_data["행정기관(소)"]

    # 행정구역별 병원 수 계산
    hospital_counts = hospital_data.groupby(["행정구역", "행정기관(대)", "행정기관(소)"]).size().reset_index(name="병원 수")

    # 결과 저장
    hospital_counts.to_excel(output_file, index=False)
    print(f"{dept} 병원 수 데이터가 생성되었습니다: {output_file}")

