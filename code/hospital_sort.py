# pip install openpyxl
import pandas as pd
import os

# 경로 설정
base_dir = os.path.dirname(os.path.abspath(__file__))
input_folder = os.path.join(base_dir, "../data_raw")
output_folder = os.path.join(base_dir, "../data_raw")

# 처리할 파일 이름들
departments = ["내과", "소아청소년과", "산부인과", "신경과"]

# 출력 폴더 생성 (없을 경우)
os.makedirs(output_folder, exist_ok=True)

# 반복 작업 처리
for dept in departments:
    input_file = os.path.join(input_folder, f"hospital_data_{dept}.xlsx")
    output_file = os.path.join(output_folder, f"hospital_data_{dept}_sort.xlsx")
    
    # 데이터 읽기
    hospital_data = pd.read_excel(input_file)
    
    # 행정기관 이름 분리
    hospital_data["행정기관(대)"] = hospital_data["소재지"].str.split().str[0]
    hospital_data["행정기관(소)"] = hospital_data["소재지"].str.split().str[1]
    
    # 행정기관 기준 정렬
    hospital_data_sorted = hospital_data.sort_values(by=["행정기관(대)", "행정기관(소)"]).reset_index(drop=True)
    
    # 결과 저장
    hospital_data_sorted.to_excel(output_file, index=False)
    print(f"{dept} 병원 정렬 파일이 생성되었습니다: {output_file}")
