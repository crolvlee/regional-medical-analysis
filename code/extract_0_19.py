# pip install openpyxl

import pandas as pd
import os

# 경로 설정
base_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 코드가 위치한 디렉토리
input_file = os.path.join(base_dir, "../data_raw/population.csv")
output_file = os.path.join(base_dir, "../data_clean/population_0_19.xlsx")

# 데이터 읽기
data = pd.read_csv(input_file)  # CSV 파일 읽기

# 2열(행정기관), 3열(총 인구수), 5열(0~9세), 6열(10~19세) 추출
data_cleaned = data.iloc[:, [1, 2, 4, 5]].copy()

# 열 이름 변경
data_cleaned.columns = ["행정기관", "총 인구수", "0~9세", "10~19세"]

# 쉼표 제거 및 숫자로 변환
data_cleaned["총 인구수"] = data_cleaned["총 인구수"].str.replace(",", "").astype(int)
data_cleaned["0~9세"] = data_cleaned["0~9세"].str.replace(",", "").astype(int)
data_cleaned["10~19세"] = data_cleaned["10~19세"].str.replace(",", "").astype(int)

# 0~9세와 10~19세 합산하여 '0~19세' 열 생성
data_cleaned["0~19세"] = data_cleaned["0~9세"] + data_cleaned["10~19세"]

# 데이터프레임 생성
result = pd.DataFrame({
    "행정기관": data_cleaned["행정기관"],
    "총 인구수": data_cleaned["총 인구수"],
    "0~9세": data_cleaned["0~9세"],
    "10~19세": data_cleaned["10~19세"],
    "0~19세": data_cleaned["0~19세"]
})

# 결과 저장
result.to_excel(output_file, index=False)

print(f"인구 요약 파일이 생성되었습니다: {output_file}")
