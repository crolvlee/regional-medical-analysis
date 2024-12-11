# pip install openpyxl

import pandas as pd
import os

# 경로 설정
base_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 코드가 위치한 디렉토리
input_file = os.path.join(base_dir, "../data_raw/population_sggu.xlsx")
output_file = os.path.join(base_dir, "../data_clean/population_20_49_f.xlsx")

# 데이터 읽기
data = pd.read_excel(input_file)  # Excel 파일 읽기

# 열 이름 확인 및 선택
data_cleaned = data.iloc[:, [0, 1, 3, 33, 34, 35]].copy()

# 열 이름 변경
data_cleaned.columns = ["행정구역(대)", "행정구역(소)", "총 인구수", "여 20~29세", "여 30~39세", "여 40~49세"]

# 쉼표 제거 및 숫자로 변환
data_cleaned["총 인구수"] = data_cleaned["총 인구수"].str.replace(",", "").astype(int)
data_cleaned["여 20~29세"] = data_cleaned["여 20~29세"].str.replace(",", "").astype(int)
data_cleaned["여 30~39세"] = data_cleaned["여 30~39세"].str.replace(",", "").astype(int)
data_cleaned["여 40~49세"] = data_cleaned["여 40~49세"].str.replace(",", "").astype(int)

# 20~49세 합산 열 생성
data_cleaned["여 20~49세"] = data_cleaned["여 20~29세"] + data_cleaned["여 30~39세"] + data_cleaned["여 40~49세"]

# 행정구역 데이터 추가
data_cleaned["행정구역"] = data_cleaned["행정구역(대)"] + " " + data_cleaned["행정구역(소)"]

# 데이터프레임 생성 (필요한 열 선택)
result = data_cleaned[["행정구역", "행정구역(대)", "행정구역(소)", "총 인구수", "여 20~29세", "여 30~39세", "여 40~49세", "여 20~49세"]]

# 결과 저장
result.to_excel(output_file, index=False)

print(f"인구 요약 파일이 생성되었습니다: {output_file}")
