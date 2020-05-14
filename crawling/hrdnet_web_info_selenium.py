# 모듈 가져오기 (터미널에서 설치)
# pip install requests
# pip install bs4
# pip install pymysql

import requests
from bs4 import BeautifulSoup
import time
import pymysql
from tqdm import tqdm
from selenium import webdriver as wd

# 프로그램 실행시간 확인
start_time = time.time()

# 크롬드라이버 - 창 띄우지 않고 크롤링 할 수 있는 옵션 활성화
options = wd.ChromeOptions()
# options.add_argument('headless')
driver = wd.Chrome(executable_path='chromedriver.exe')

# 초기화
course_num = 0
target_num = 0

# 훈련과정 선택
print("=========== 훈련과정 선택 ===========\n"
      "=        1. 구직자 훈련과정         =\n"
      "=        2. 근로자 훈련과정         =\n"
      "=        3. 기업 훈련과정           =\n"
      "=        4. 원격 훈련과정           =\n"
      "=====================================")

course_num = int(input("숫자를 입력하세요: "))

if course_num == 1:
    # db명 지정
    # 구직자
    db_name = "seeker_db"
elif course_num == 2:
    # db명 지정
    # 근로자
    db_name = "worker_db"
elif course_num == 3:
    # db명 지정
    # 기업
    db_name = "corp_db"
elif course_num == 4:
    # db명 지정
    # 기업
    db_name = "web_db"

# db 접속
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db=db_name, charset='utf8')
cur = conn.cursor()

# 훈련대상 선택(1, 2, 3)
if course_num < 4:
    # url 불러오기용 table명
    load_table_name = "url_table"
    # 저장할 데이터용 table명
    save_table_name = "data_table"

# 훈련대상 선택(4-원격 훈련과정일 경우에만)
elif course_num == 4:
    print("=========== 훈련대상 선택 ===========\n"
          "=              1. 구직자            =\n"
          "=              2. 근로자            =\n"
          "=              3. 기업              =\n"
          "=====================================")

    target_num = int(input("숫자를 입력하세요: "))

    if target_num == 1:
        # 구직자
        # url 불러오기용 table명
        load_table_name = "seeker_url_table"
        # 저장할 데이터용 table명
        save_table_name = "seeker_data_table"

    elif target_num == 2:
        # 근로자
        # url 불러오기용 table명
        load_table_name = "worker_url_table"
        # 저장할 데이터용 table명
        save_table_name = "worker_data_table"

    elif target_num == 3:
        # 기업
        # url 불러오기용 table명
        load_table_name = "corp_url_table"
        # 저장할 데이터용 table명
        save_table_name = "corp_data_table"

# 1 훈련과정명 == courseName
# 2 훈련기관명 == organName
# 3 훈련기관 주소 == organAddress
# # 4 훈련실시 주소 == enforceAddress
# 5 담당자 성명 == managerName
# 6 담당자 연락처 == managerTel
# 7 홈페이지 == webSite
# 8 담당자 이메일 == managerEmail
# 9 주관부처 == department
# 10 훈련유형 == courseType
# 11 NCS 직무분류 == ncsClass
# 12 수강생 평균만족도 == satisLevel
# 13 훈련기간 == courseTerm
# # 14 훈련기관 직종별 취업률 == employRate
# 15 훈련시간 == courseTime
# 16 수강생 평균연령대 == ageGroup
# 17 훈련비 == courseCost
# 18 관련자격증 == license
# # 19 취업처 임금평균 == avgPay
# # 20 ncs수준 == ncsLevel

# 1. 구직자(seeker_db\data_table) -> 20개(4, 14, 19, 20)
# 2. 근로자(worker_db\data_table) -> 18개(4, 20)
# 2-1. 외국어과정 -> 16개
# 2-2. 인터넷과정 -> 16개
# 3. 기업(corp_db\data_table) -> 16개
# 4. 원격(web_db)
# 4-1. 구직자(\seeker_data_table) -> 18개(14, 19)
# 4-2. 근로자(\worker_data_table)  -> 16개
# 4-3. 기업(\corp_data_table)  -> 16개

# if 3, 4-2, 4-3 (if (tagret_num == 2 or 3) or (course_num == 3))
# elif 1 (if course_num == 1)
# elif 2 (if course_num == 2)
# elif 4-1 (if target_num == 1)

all_data_arr = []

# 저장용 테이블 초기화
sql = "truncate `" + save_table_name + "`;"
cur.execute(sql)

# 사이트 접속

sql = "SELECT url FROM " + load_table_name
cur.execute(sql)
all_url = cur.fetchall()

for cut_url in tqdm(all_url, desc="Progress of the cut URL", mininterval=10):
    divide_data_arr = []
    cut_url = str(cut_url).lstrip("('")
    cut_url = str(cut_url).rstrip("',)")

    # 사이트 접속
    r = driver.get(cut_url)
    time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # html > 전체 table
    tables = soup.find_all("table")

    # infoArea Data 가져오기
    # 1. 구직자, 2. 근로자
    if course_num == 1 or 2:
        for i, table in enumerate(tables[0:1]):
            # 첫번째 table 안의 tr 태그 전부 찾아서 저장
            trs = table.find_all("tr")
            for tr in trs:
                # tr 태그 안에서 td 태그 전부 찾아서 저장
                tds = tr.find_all("td")
                for td in tds:
                    # td 태그 안의 text 내용 양쪽의 공백을 지워줌
                    td = td.text.strip()
                    # 첫번째 td 태그 -> 공백이므로 무시
                    if i == 0:
                        exit
                    # 두번째 td 태그 -> '모집중, 모집마감' 글씨 제거
                    elif i == 1:
                        divide_data_arr.append(td[0: -4].replace("\n", ""))
                    # 네번째 td 태그 -> '지도보기' 글씨 제거
                    elif i == 3:
                        divide_data_arr.append(td[0: -5])
                    # 다섯번째 td 태그 -> '지도보기' 글씨 제거
                    elif i == 4:
                        divide_data_arr.append(td[0: -5])
                    # 그 외의 경우 일반적으로 저장
                    else:
                        divide_data_arr.append(td)
                    i += 1

        for j, table in enumerate(tables[1:2]):
            # 두번째 table 안의 tr 태그 전부 찾아서 저장
            trs = table.find_all("tr")
            for tr in trs[0:1]:
                # 첫번째 tr 태그 안에서 td 태그 전부 찾아서 저장
                tds = tr.find_all("td")
                for td in tds:
                    # td 태그 안의 text 내용 양쪽의 공백을 지워줌
                    td = td.text.strip()
                    divide_data_arr.append(td)
                    j += 1

        for k, table in enumerate(tables[1:2]):
            # 두번째 table 안의 tr 태그 전부 찾아서 저장
            trs = table.find_all("tr")
            for tr in trs[1:2]:
                # 두번째 tr 태그 안에서 li 태그 전부 찾아서 저장
                lis = tr.find_all("li")
                for li in lis:
                    # li 태그 안의 text 내용 양쪽의 공백을 지워줌
                    innertext = li.text.strip()
                    # li 태그 안의 text 내용 중 "	" 전부 삭제
                    innertext = innertext.replace("	", "")
                    # li 태그 안의 text 내용 중 "\n" 전부 삭제
                    innertext = innertext.replace("\n", "")
                    # li 태그 안의 text 내용을 ":" 를 기준으로 나눠줌
                    innertext = innertext.split(":")
                    # 나눠준 내용 중 뒷부분(필요한 data) 앞쪽의 공백을 지워줌
                    innertext = innertext[1].lstrip()
                    # ncs 직무분류 코드 번호만 추출
                    if k == 0:
                        if "(" in innertext:
                            # li 태그 안의 text 내용을 "(" 를 기준으로 나눠줌
                            innertext = innertext.split("(")
                            # 나눠준 내용 중 뒷부분(필요한 data) 뒤쪽의 괄호을 지워줌
                            innertext = innertext[1].rstrip(")")
                    divide_data_arr.append(innertext)
                    k += 1

        all_data_arr.append(divide_data_arr)

    # 3. 기업, 4. 웹
    elif course_num == 3 or 4:
        # infoArea Data 가져오기
        for i, table in enumerate(tables[0:1]):
            # 첫번째 table 안의 tr 태그 전부 찾아서 저장
            trs = table.find_all("tr")
            for tr in trs:
                # tr 태그 안에서 td 태그 전부 찾아서 저장
                tds = tr.find_all("td")
                for td in tds:
                    # td 태그 안의 text 내용 양쪽의 공백을 지워줌
                    td = td.text.strip()
                    # 첫번째 td 태그 -> 공백이므로 무시
                    if i == 0:
                        exit
                    # 두번째 td 태그 -> '모집중, 모집마감' 글씨 제거
                    elif i == 1:
                        divide_data_arr.append(td[0: -4].replace("\n", ""))
                    # 네번째 td 태그 -> '지도보기' 글씨 제거
                    elif i == 3:
                        divide_data_arr.append(td[0: -5])
                    # 그 외의 경우 일반적으로 저장
                    else:
                        divide_data_arr.append(td)
                    i += 1

        for j, table in enumerate(tables[1:2]):
            # 두번째 table 안의 tr 태그 전부 찾아서 저장
            trs = table.find_all("tr")
            for tr in trs[0:1]:
                # 첫번째 tr 태그 안에서 td 태그 전부 찾아서 저장
                tds = tr.find_all("td")
                for td in tds:
                    # td 태그 안의 text 내용 양쪽의 공백을 지워줌
                    td = td.text.strip()
                    divide_data_arr.append(td)
                    j += 1

        for k, table in enumerate(tables[1:2]):
            # 두번째 table 안의 tr 태그 전부 찾아서 저장
            trs = table.find_all("tr")
            for tr in trs[1:2]:
                # 두번째 tr 태그 안에서 li 태그 전부 찾아서 저장
                lis = tr.find_all("li")
                for li in lis:
                    # li 태그 안의 text 내용 양쪽의 공백을 지워줌
                    innertext = li.text.strip()
                    # li 태그 안의 text 내용 중 "	" 전부 삭제
                    innertext = innertext.replace("	", "")
                    # li 태그 안의 text 내용 중 "\n" 전부 삭제
                    innertext = innertext.replace("\n", "")
                    # li 태그 안의 text 내용을 ":" 를 기준으로 나눠줌
                    innertext = innertext.split(":")
                    # 나눠준 내용 중 뒷부분(필요한 data) 앞쪽의 공백을 지워줌
                    innertext = innertext[1].lstrip()
                    # ncs 직무분류 코드 번호만 추출
                    if k == 0:
                        if "(" in innertext:
                            # li 태그 안의 text 내용을 "(" 를 기준으로 나눠줌
                            innertext = innertext.split("(")
                            # 나눠준 내용 중 뒷부분(필요한 data) 뒤쪽의 괄호을 지워줌
                            innertext = innertext[1].rstrip(")")
                    divide_data_arr.append(innertext)
                    k += 1

        all_data_arr.append(divide_data_arr)

    for data in all_data_arr:
        try:
            datatext = str()
            for i in data:
                datatext += '"' + i + '",'

            if target_num == 2 or target_num == 3 or course_num == 3:
                if len(data) != 16:
                    continue
                sql = "insert into " + save_table_name + " (courseName, organName, organAddress, managerName, managerTel, webSite, managerEmail, department, " \
                                                         "courseType, ncsClass, satisLevel, courseTerm, courseTime, ageGroup, courseCost, license)" \
                                                         " values (" + datatext.rstrip(",") + ");"
            elif course_num == 1:
                if len(data) != 20:
                    continue
                sql = "insert into " + save_table_name + " (courseName, organName, organAddress, enforceAddress, managerName, managerTel, webSite, managerEmail, department, " \
                                                         "courseType, ncsClass, satisLevel, courseTerm, employRate, courseTime, ageGroup, courseCost, license, avgPay, ncsLevel)" \
                                                         " values (" + datatext.rstrip(",") + ");"
            elif course_num == 2:
                if len(data) != 16 and len(data) != 18:
                    continue

                if len(data) == 16:
                    sql = "insert into " + save_table_name + " (courseName, organName, organAddress, managerName, managerTel, webSite, managerEmail, department, " \
                                                             "courseType, ncsClass, satisLevel, courseTerm, courseTime, ageGroup, courseCost, license)" \
                                                             " values (" + datatext.rstrip(",") + ");"
                elif len(data) == 18:
                    sql = "insert into " + save_table_name + " (courseName, organName, organAddress, enforceAddress, managerName, managerTel, webSite, managerEmail, department, " \
                                                             "courseType, ncsClass, satisLevel, courseTerm, courseTime, ageGroup, courseCost, license, ncsLevel)" \
                                                             " values (" + datatext.rstrip(",") + ");"
            elif target_num == 1:
                if len(data) != 18:
                    continue
                sql = "insert into " + save_table_name + " (courseName, organName, organAddress, managerName, managerTel, webSite, managerEmail, department, " \
                                                         "courseType, ncsClass, satisLevel, courseTerm, employRate, courseTime, ageGroup, courseCost, license, avgPay)" \
                                                         " values (" + datatext.rstrip(",") + ");"
            cur.execute(sql)
            conn.commit()

        except Exception as e1:
            print('오류', e1, cut_url, datatext)

    all_data_arr = []

# sql = "select * into outfile 'Desktop/" + save_table_name + datetime.now() + ".csv' fields terminated by ',' enclosed by '"' LINES TERMINATED BY '\n' from " + save_table_name + ";"
#         cur.execute(sql)
#         conn.commit()

print(load_table_name, save_table_name, course_num, target_num)

end_time = time.time()
print("저장된 데이터 : " + str(len(all_url)))
print("WorkingTime: {} sec".format(end_time - start_time))

cur.close()
driver.close()
conn.close()
driver.quit()