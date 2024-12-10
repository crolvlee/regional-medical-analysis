import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# 결과 저장 디렉토리 설정
data_raw_dir = os.path.join(os.getcwd(), "../data_raw")
if not os.path.exists(data_raw_dir):
    os.makedirs(data_raw_dir)

# 웹 드라이버 설정
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URL 접속
url = 'https://www.hira.or.kr/ra/dtlCndHospSrch/dtlCndHospSrch.do?pgmid=HIRAA050200000000'
driver.get(url)

# '시/도' 리스트
regions = ["110000", "210000", "220000", "230000", "240000", "250000", "260000", "310000", "320000", "330000", "340000", "350000", "360000", "370000", "380000", "390000", "410000"]

# 종별 리스트 (value1 기준)
categories = {
    "01": "상급종합병원",
    "11": "종합병원",
    "21": "병원",
    "31": "의원"
}

# 진료과목 체크박스 기본 인덱스
departments = {
    "내과": 3,
    "소아청소년과": 10,
    "산부인과": 8,
    "신경과": 11
}

# 크롤링 시작
for department_name, base_index in departments.items():
    department_data = []
    
    for region_code in regions:
        # 1. '시/도' 선택
        try:
            region_dropdown = driver.find_element(By.ID, "sidoCd")
            region_dropdown.click()
            region_option = driver.find_element(By.XPATH, f'//*[@id="sidoCd"]/option[@value="{region_code}"]')
            region_option.click()
            time.sleep(1)

            for category_code, category_name in categories.items():
                # 2. '종별' 선택
                try:
                    category_dropdown = driver.find_element(By.ID, "clCds")
                    category_dropdown.click()
                    category_option = driver.find_element(By.XPATH, f'//*[@id="clCds"]/option[@value1="{category_code}"]')
                    category_option.click()
                    time.sleep(1)

                    # 종별 변경 시 alert 처리
                    try:
                        alert = Alert(driver)
                        alert.accept()  # 알림 창 확인
                        time.sleep(2)
                    except:
                        pass
                except Exception as e:
                    print(f"종별 선택 오류 ({category_name}): {e}")
                    continue

                # 3. '진료과목' 클릭
                try:
                    detail_button = driver.find_element(By.XPATH, '//*[@id="subCdList"]/li[1]/label')  # '진료과목' 버튼
                    detail_button.click()
                    time.sleep(1)

                    # 4. 체크박스 선택
                    index = base_index + 1 if category_name == "의원" else base_index
                    checkbox_xpath = f'//*[@id="dtlCdList"]/li[{index}]/label'
                    checkbox = driver.find_element(By.XPATH, checkbox_xpath)
                    
                    if not checkbox.is_selected():
                        checkbox.click()
                    time.sleep(1)
                except Exception as e:
                    print(f"'진료과목' 클릭 오류: {e}")
                    continue
                
                # 5. 검색 버튼 클릭
                try:
                    search_button = driver.find_element(By.XPATH, '//*[@id="hosp-form"]/div[2]/div/a[2]')
                    search_button.click()
                    time.sleep(2)

                    # 페이지네이션 처리
                    while True:
                        try:
                            # 현재 페이지 데이터 수집
                            table_rows = driver.find_elements(By.CSS_SELECTOR, "#listInfoTable tr")
                            for row in table_rows:
                                cols = row.find_elements(By.TAG_NAME, "td")
                                if len(cols) > 1:  # 유효한 데이터만 추가
                                    department_data.append([
                                        cols[1].text.strip(),  # 병원명
                                        cols[2].text.strip(),  # 소재지
                                        region_code,  # 지역코드
                                        category_name  # 종별
                                    ])

                            print(f"현재 페이지에서 {len(table_rows)}개의 데이터를 수집했습니다.")

                            # 현재 활성화된 페이지 확인
                            current_page = driver.find_element(By.CSS_SELECTOR, ".pagination .on a").text.strip()
                            print(f"현재 페이지: {current_page}")
                            
                            # 다음 페이지 XPath 결정
                            if int(current_page) % 10 == 0:  # 10, 20, 30 페이지 등
                                # 10의 배수일 경우
                                next_button_selector = '#pagingPc > a.next'
                            else:
                                # 10의 배수가 아닌 경우
                                next_page_relative_index = int(current_page) % 10 + 1
                                next_button_xpath = f'//*[@id="pagingPc"]/ul/li[{next_page_relative_index}]/a'

                            # 다음 페이지 클릭
                            try:
                                if int(current_page) % 10 == 0:
                                    next_page_button = driver.find_element(By.CSS_SELECTOR, next_button_selector)
                                else:
                                    next_page_button = driver.find_element(By.XPATH, next_button_xpath)
                                next_page_button.click()
                                time.sleep(2)
                            except Exception as e:
                                print(f"다음 페이지 버튼 클릭 오류: {e}")
                                break
                        except Exception as e:
                            print(f"페이지네이션 처리 오류: {e}")
                            break
                except Exception as e:
                    print(f"검색 및 결과 처리 오류: {e}")
                    continue
        except Exception as e:
            print(f"지역 선택 오류: {e}")
            continue
    
    # 데이터를 DataFrame으로 변환
    columns = ["병원명", "소재지", "지역코드", "종별"]
    df = pd.DataFrame(department_data, columns=columns)

    # 파일 저장 경로 설정
    file_path = os.path.join(data_raw_dir, f"hospital_data_{department_name}.xlsx")

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

