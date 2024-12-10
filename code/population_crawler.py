import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# 웹 드라이버 설정
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# URL 접속
url = "https://jumin.mois.go.kr/ageStatMonth.do"
driver.get(url)
time.sleep(2)  # 페이지 로드 대기

# 테이블 저장용 리스트
data = []

try:
    # WebDriverWait를 사용하여 요소 대기
    wait = WebDriverWait(driver, 10)

    # 첫 번째 드롭다운 처리
    lvl1_dropdown = wait.until(EC.presence_of_element_located((By.ID, "sltOrgLvl1")))
    lvl1_select = Select(lvl1_dropdown)
    
    # 첫 번째 드롭다운 옵션들 가져오기 (첫 번째 옵션 제외)
    lvl1_options = lvl1_select.options[1:]
    
    for lvl1_option_index in range(len(lvl1_options)):
        try:
            # 매번 요소를 다시 찾음
            lvl1_dropdown = wait.until(EC.presence_of_element_located((By.ID, "sltOrgLvl1")))
            lvl1_select = Select(lvl1_dropdown)
            
            # 인덱스로 옵션 선택
            lvl1_select.select_by_index(lvl1_option_index + 1)
            
            # 옵션 값과 이름 추출
            lvl1_value = lvl1_select.first_selected_option.get_attribute("value")
            lvl1_name = lvl1_select.first_selected_option.text.strip()
            
            print(f"sltOrgLvl1 선택: {lvl1_name}")
            time.sleep(1)

            # 두 번째 드롭다운 처리
            lvl2_dropdown = wait.until(EC.presence_of_element_located((By.ID, "sltOrgLvl2")))
            lvl2_select = Select(lvl2_dropdown)
            
            # 두 번째 드롭다운 옵션들 가져오기 (첫 번째 옵션 제외)
            lvl2_options = lvl2_select.options[1:]
            
            for lvl2_option_index in range(len(lvl2_options)):
                try:
                    # 매번 요소를 다시 찾음
                    lvl2_dropdown = wait.until(EC.presence_of_element_located((By.ID, "sltOrgLvl2")))
                    lvl2_select = Select(lvl2_dropdown)
                    
                    # 인덱스로 옵션 선택
                    lvl2_select.select_by_index(lvl2_option_index + 1)
                    
                    # 옵션 값과 이름 추출
                    lvl2_value = lvl2_select.first_selected_option.get_attribute("value")
                    lvl2_name = lvl2_select.first_selected_option.text.strip()
                    
                    print(f"sltOrgLvl2 선택: {lvl2_name}")
                    time.sleep(1)

                    # 검색 버튼 클릭
                    search_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn_search")))
                    search_button.click()
                    
                    # 테이블 로딩 대기
                    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="contextTable"]/tbody/tr')))
                    time.sleep(2)

                    # 첫 번째 데이터 추출
                    rows = driver.find_elements(By.XPATH, '//*[@id="contextTable"]/tbody/tr')
                    if len(rows) > 0:
                        first_row = rows[0].find_elements(By.TAG_NAME, "td")[1:]  # 첫 번째 셀 제외
                        row_data = [lvl1_name, lvl2_name] + [cell.text.strip() for cell in first_row]
                        data.append(row_data)
                        print(f"데이터 저장: {row_data}")
                    else:
                        print("테이블 데이터가 없습니다.")
                except Exception as e:
                    print(f"'sltOrgLvl2' 처리 중 오류: {e}")
        except Exception as e:
            print(f"'sltOrgLvl1' 처리 중 오류: {e}")
except Exception as e:
    print(f"오류 발생: {e}")
finally:
    # 브라우저 종료
    driver.quit()

# 열 정의
columns = [
    "행정기관(대)", "행정기관(소)", "행정기관",
    "총_인구수", "총_연령구간인구수",
    "총_0~9세", "총_10~19세", "총_20~29세", "총_30~39세", "총_40~49세", "총_50~59세",
    "총_60~69세", "총_70~79세", "총_80~89세", "총_90~99세", "총_100세 이상",
    "남_인구수", "남_연령구간인구수",
    "남_0~9세", "남_10~19세", "남_20~29세", "남_30~39세", "남_40~49세", "남_50~59세",
    "남_60~69세", "남_70~79세", "남_80~89세", "남_90~99세", "남_100세 이상",
    "여_인구수", "여_연령구간인구수",
    "여_0~9세", "여_10~19세", "여_20~29세", "여_30~39세", "여_40~49세", "여_50~59세",
    "여_60~69세", "여_70~79세", "여_80~89세", "여_90~99세", "여_100세 이상"
]

# 데이터를 pandas DataFrame으로 변환
try:
    df = pd.DataFrame(data, columns=columns)
    # 테이블 출력
    print(df)
except ValueError as e:
    print(f"DataFrame 생성 오류: {e}")
    print(f"저장된 데이터: {data}")
    

# 결과 저장 디렉토리 설정
data_dir = os.path.join(os.getcwd(), "../data_raw")
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

file_path = os.path.join(data_dir, "population_sggu.xlsx")

# 엑셀 파일 저장
try:
    if os.path.exists(file_path):
        print(f"경고: {file_path} 파일이 이미 존재합니다. 기존 파일을 덮어씁니다.")
    df.to_excel(file_path, index=False)
    print(f"'{file_path}'에 데이터를 저장했습니다.")
except Exception as e:
    print(f"엑셀 저장 중 오류가 발생했습니다: {e}")

# 브라우저 종료
driver.quit()

print("크롤링이 완료되었습니다! 데이터를 지정된 파일에 저장했습니다.")





