# pip install openpyxl
import pandas as pd
import os

# 경로 설정
base_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 코드가 위치한 디렉토리
input_file = os.path.join(base_dir, "../data_raw/population_sggu.xlsx")
output_file = os.path.join(base_dir, "../data_clean/population_60_up.xlsx")

# 데이터 읽기
data = pd.read_excel(input_file)  # Excel 파일 읽기

# 열 이름 확인 및 선택
data_cleaned = data.iloc[:, [0, 1, 3, 11, 12, 13, 14, 15]].copy()

# 열 이름 변경
data_cleaned.columns = ["행정기관(대)", "행정기관(소)", "총 인구수", "60~69세", "70~79세", "80~89세", "90~99세", "100세 이상"]

def convert_to_int(column):
    try:
        return column.str.replace(",", "").astype(int)
    except AttributeError:  # 쉼표가 없는 경우
        return column.astype(int)

# 적용
data_cleaned["총 인구수"] = convert_to_int(data_cleaned["총 인구수"])
data_cleaned["60~69세"] = convert_to_int(data_cleaned["60~69세"])
data_cleaned["70~79세"] = convert_to_int(data_cleaned["70~79세"])
data_cleaned["80~89세"] = convert_to_int(data_cleaned["80~89세"])
data_cleaned["90~99세"] = convert_to_int(data_cleaned["90~99세"])
data_cleaned["100세 이상"] = convert_to_int(data_cleaned["100세 이상"])


# 60세 이상 인구 합산하여 '60세 이상' 열 생성
data_cleaned["60세 이상"] = (
    data_cleaned["60~69세"] +
    data_cleaned["70~79세"] +
    data_cleaned["80~89세"] +
    data_cleaned["90~99세"] +
    data_cleaned["100세 이상"]
)

# 필요한 열만 선택하여 새 데이터프레임 생성
result = data_cleaned[["행정기관(대)", "행정기관(소)", "총 인구수", "60~69세", "70~79세", "80~89세", "90~99세", "100세 이상", "60세 이상"]]

# 결과 저장
result.to_excel(output_file, index=False)
print(f"60세 이상 인구 요약 파일이 생성되었습니다: {output_file}")