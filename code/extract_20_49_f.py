# pip install openpyxl

import pandas as pd
import os

# 경로 설정
base_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 코드가 위치한 디렉토리
input_file = os.path.join(base_dir, "../data_raw/population.csv")
output_file = os.path.join(base_dir, "../data_clean/population_20_49_f.xlsx")

# 데이터 읽기
data = pd.read_csv(input_file)  # CSV 파일 읽기

# 2열(행정기관), 29열(여 인구수), 33열(20~29세), 34열(30~39세), 35열(40~49세) 추출
data_cleaned = data.iloc[:, [1, 28, 32, 33, 34]].copy()

# 열 이름 변경
data_cleaned.columns = ["행정기관", "여 인구수", "20~29세", "30~39세", "40~49세"]

# 쉼표 제거 및 숫자로 변환
data_cleaned["여 인구수"] = data_cleaned["여 인구수"].str.replace(",", "").astype(int)
data_cleaned["20~29세"] = data_cleaned["20~29세"].str.replace(",", "").astype(int)
data_cleaned["30~39세"] = data_cleaned["30~39세"].str.replace(",", "").astype(int)
data_cleaned["40~49세"] = data_cleaned["40~49세"].str.replace(",", "").astype(int)

# 0~9세와 10~19세 합산하여 '0~19세' 열 생성
data_cleaned["20~49세"] = data_cleaned["20~29세"] + data_cleaned["30~39세"] + data_cleaned["40~49세"]

# 데이터프레임 생성
result = pd.DataFrame({
    "행정기관": data_cleaned["행정기관"],
    "여 인구수": data_cleaned["여 인구수"],
    "20~29세": data_cleaned["20~29세"],
    "30~39세": data_cleaned["30~39세"],
    "40~49세": data_cleaned["40~49세"],
    "20~49세": data_cleaned["20~49세"]
})

# 결과 저장
result.to_excel(output_file, index=False)

print(f"인구 요약 파일이 생성되었습니다: {output_file}")
