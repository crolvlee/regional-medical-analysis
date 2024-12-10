from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
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
    # 'sltOrgLvl1' 드롭다운 요소 가져오기
    lvl1_dropdown = Select(driver.find_element(By.ID, "sltOrgLvl1"))

    # 'sltOrgLvl1'의 모든 옵션 가져오기 (첫 번째 옵션 제외)
    lvl1_options = lvl1_dropdown.options[1:]

    for lvl1_option in lvl1_options:
        try:
            # 'sltOrgLvl1' 옵션 선택
            lvl1_value = lvl1_option.get_attribute("value")
            lvl1_name = lvl1_option.text.strip()
            lvl1_dropdown = Select(driver.find_element(By.ID, "sltOrgLvl1"))  # 드롭다운 새로 가져오기
            lvl1_dropdown.select_by_value(lvl1_value)
            print(f"sltOrgLvl1 선택: {lvl1_name}")
            time.sleep(1)

            # 'sltOrgLvl2' 드롭다운 요소 가져오기
            lvl2_dropdown = Select(driver.find_element(By.ID, "sltOrgLvl2"))

            # 'sltOrgLvl2'의 모든 옵션 가져오기 (첫 번째 옵션 제외)
            lvl2_options = lvl2_dropdown.options[1:]

            for lvl2_option in lvl2_options:
                try:
                    # 'sltOrgLvl2' 드롭다운을 새로 가져와야 하므로 다시 초기화
                    lvl2_dropdown = Select(driver.find_element(By.ID, "sltOrgLvl2"))
                    lvl2_value = lvl2_option.get_attribute("value")
                    lvl2_name = lvl2_option.text.strip()
                    lvl2_dropdown.select_by_value(lvl2_value)
                    print(f"sltOrgLvl2 선택: {lvl2_name}")
                    time.sleep(1)

                    # 검색 버튼 클릭
                    search_button = driver.find_element(By.CLASS_NAME, "btn_search")
                    search_button.click()
                    time.sleep(3)  # 검색 결과 로딩 대기

                    # 첫 번째 데이터만 추출
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
    "총 인구수", "총_연령구간인구수",
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
