# HRD-net 사이트 훈련정보 가져오기
# 로그인 시 PC 웹 사이트에서 처리가 어려울 경우 -> 모바일 로그인으로 진입
# 모듈 가져오기 (터미널에서 설치)
# pip install selenium
# pip install bs4
# pip install pymysql
# pip install tqdm

from selenium import webdriver as wd
import time
import pymysql
import datetime
from tqdm import tqdm


# 프로그램 실행시간 확인
start_time = time.time()

# 초기화
sqlcounter = 0

# 크롬드라이버 - 창 띄우지 않고 크롤링 할 수 있는 옵션 활성화
options = wd.ChromeOptions()
#options.add_argument('headless')
driver = wd.Chrome(executable_path='chromedriver.exe')
# , chrome_options=options
# 훈련과정 선택
print("=========== 훈련과정 선택 ===========\n"
      "=        1. 구직자 훈련과정         =\n"
      "=        2. 근로자 훈련과정         =\n"
      "=        3. 기업 훈련과정           =\n"
      "=        4. 원격 훈련과정           =\n"
      "=====================================")

# 훈련과정 선택은 필수적이므로 while문을 통해
# 잘못된 숫자를 입력하더라도 다시 입력받을 수 있도록 한다.
while True:
    course_num = int(input("숫자를 입력하세요: "))
    if 1 <= course_num <= 4:
        break
    elif course_num > 4 or course_num < 1:
        print("잘못된 숫자를 입력하셨습니다!")
        continue

if course_num == 1:
    # 구직자 훈련과정 url
    course_url = "http://hrd.go.kr/hrdp/ti/ptiao/PTIAO0100L.do"
    # db명 지정
    db_name = "seeker_db"
elif course_num == 2:
    # 근로자 훈련과정 url
    course_url = "http://hrd.go.kr/hrdp/ti/ptibo/PTIBO0100L.do"
    # db명 지정
    db_name = "worker_db"
elif course_num == 3:
    # 기업 훈련과정 url
    course_url = "http://hrd.go.kr/hrdp/ti/ptico/PTICO0100L.do"
    # db명 지정
    db_name = "corp_db"

elif course_num == 4:
    # 원격 훈련과정 url
    course_url = "http://hrd.go.kr/hrdp/ti/ptimo/PTIMO0100L.do"
    # db명 지정
    db_name = "web_db"


# db 접속
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db=db_name, charset='utf8')
cur = conn.cursor()

# 사이트 접속
driver.get(course_url)

# 훈련대상 선택
# 구직자 훈련과정 (###### 임시 ######)
if course_num == 1:
    table_name = "url_table"
# 훈련대상 선택
# 근로자 훈련과정
elif course_num == 2:
    table_name = "url_table"
    # 훈련유형 선택
    print("=========== 훈련유형 선택 =======================\n"
          "=         1. 전체                               =\n"
          "=         2. 근로자카드                         =\n"
          "=         3. 영세사업장훈련(폴리텍대학)         =\n"
          "==================================================")

    # 훈련유형 선택은 필수적이지 않으므로 try 문을 통해
    # 잘못된 값을 입력받으면 기본값으로 처리해준다.
    try:
        type_num = int(input("숫자를 입력하세요: "))
        if type_num > 3 or type_num < 1:
            raise Exception("잘못된 숫자를 입력하셨습니다!")
    except Exception as e:
        print("오류 발생 : ", e)
        print("기본값 범위 내에서 검색합니다.")
        type_num = 1

    # 훈련유형 선택
    if type_num == 1:
        # 전체
        driver.find_element_by_xpath('//*[@id="crseTracseSe1"]').click()
    elif type_num == 2:
        # 근로자카드
        driver.find_element_by_xpath('//*[@id="crseTracseSe2"]').click()
    elif type_num == 3:
        # 영세사업장훈련
        driver.find_element_by_xpath('//*[@id="crseTracseSe3"]').click()

    # 훈련구분 선택
    print("=========== 훈련구분 선택 ===========\n"
          "=            1. 전체                =\n"
          "=            2. 일반과정            =\n"
          "=            3. 외국어과정          =\n"
          "=            4. 인터넷과정          =\n"
          "=====================================")

    # 훈련유형 선택은 필수적이지 않으므로 try 문을 통해
    # 잘못된 값을 입력받으면 기본값으로 처리해준다.
    try:
        item_num = int(input("숫자를 입력하세요: "))
        if item_num > 4 or item_num < 1:
            raise Exception("잘못된 숫자를 입력하셨습니다!")
    except Exception as e:
        print("오류 발생 : ", e)
        print("기본값 범위 내에서 검색합니다.")
        item_num = 1

    # 훈련구분 선택
    if item_num == 1:
        # 전체
        driver.find_element_by_xpath('//*[@id="traingMthCd1"]').click()
    elif item_num == 2:
        # 일반과정
        driver.find_element_by_xpath('//*[@id="traingMthCd2"]').click()
    elif item_num == 3:
        # 외국어과정
        driver.find_element_by_xpath('//*[@id="traingMthCd3"]').click()
    elif item_num == 4:
        # 인터넷과정
        driver.find_element_by_xpath('//*[@id="traingMthCd4"]').click()

    # 훈련대상 검색
    #driver.find_element_by_class_name('btn1').click()

# 훈련대상 선택
# 기업 훈련과정
elif course_num == 3:
    table_name = "url_table"
    # 훈련유형 선택
    print("=========== 훈련유형 선택 ===========\n"
          "=             1. 전체               =\n"
          "=             2. 사업주지원         =\n"
          "=             3. 컨소시엄           =\n"
          "=====================================")

    # 훈련유형 선택은 필수적이지 않으므로 try 문을 통해
    # 잘못된 값을 입력받으면 기본값으로 처리해준다.
    try:
        type_num = int(input("숫자를 입력하세요: "))
        if type_num > 3 or type_num < 1:
            raise Exception("잘못된 숫자를 입력하셨습니다!")
    except Exception as e:
        print("오류 발생 : ", e)
        print("기본값 범위 내에서 검색합니다.")
        type_num = 1

    # 훈련유형 선택
    if type_num == 1:
        # 전체
        driver.find_element_by_xpath('//*[@id="crseTracseSe1"]').click()
    elif type_num == 2:
        # 사업주지원
        driver.find_element_by_xpath('//*[@id="crseTracseSe2"]').click()
    elif type_num == 3:
        # 컨소시엄
        driver.find_element_by_xpath('//*[@id="crseTracseSe3"]').click()

    # 훈련구분 선택
    # 사업주지원
    if type_num == 2:
        print("=========== 훈련구분 선택 ===========\n"
              "=          1. 전체                  =\n"
              "=          2. 집체(집합)과정        =\n"
              "=          3. 인터넷과정            =\n"
              "=          4. 우편과정              =\n"
              "=          5. 혼합과정              =\n"
              "=          6. 스마트과정            =\n"
              "=====================================")

        # 훈련유형 선택은 필수적이지 않으므로 try 문을 통해
        # 잘못된 값을 입력받으면 기본값으로 처리해준다.
        try:
            item_num = int(input("숫자를 입력하세요: "))
            if item_num > 6 or item_num < 1:
                raise Exception("잘못된 숫자를 입력하셨습니다!")
        except Exception as e:
            print("오류 발생 : ", e)
            print("기본값 범위 내에서 검색합니다.")
            item_num = 1

        # 훈련구분 선택
        if item_num == 1:
            # 전체
            driver.find_element_by_xpath('//*[@id="traingMthCd1"]').click()
        elif item_num == 2:
            # 집체(집합)과정
            driver.find_element_by_xpath('//*[@id="traingMthCd2"]').click()
        elif item_num == 3:
            # 인터넷과정
            driver.find_element_by_xpath('//*[@id="traingMthCd3"]').click()
        elif item_num == 4:
            # 우편과정
            driver.find_element_by_xpath('//*[@id="traingMthCd4"]').click()
        elif item_num == 5:
            # 혼합과정
            driver.find_element_by_xpath('//*[@id="traingMthCd5"]').click()
        elif item_num == 6:
            # 스마트과정
            driver.find_element_by_xpath('//*[@id="traingMthCd6"]').click()

    # 훈련구분 선택
    # 컨소시엄
    elif type_num == 3:
        print("=========== 훈련구분 선택 ===========\n"
              "=          1. 전체                  =\n"
              "=          2. 집체(집합)과정        =\n"
              "=          3. 인터넷과정            =\n"
              "=====================================")

        # 훈련유형 선택은 필수적이지 않으므로 try 문을 통해
        # 잘못된 값을 입력받으면 기본값으로 처리해준다.
        try:
            item_num = int(input("숫자를 입력하세요: "))
            if item_num > 3 or item_num < 1:
                raise Exception("잘못된 숫자를 입력하셨습니다!")
        except Exception as e:
            print("오류 발생 : ", e)
            print("기본값 범위 내에서 검색합니다.")
            item_num = 1

        # 훈련구분 선택
        if item_num == 1:
            # 전체
            driver.find_element_by_xpath('//*[@id="traingMthCd1"]').click()
        elif item_num == 2:
            # 집체(집합)과정
            driver.find_element_by_xpath('//*[@id="traingMthCd2"]').click()
        elif item_num == 3:
            # 인터넷과정
            driver.find_element_by_xpath('//*[@id="traingMthCd3"]').click()

    # 훈련대상 검색
    #driver.find_element_by_class_name('btn1').click()


# 훈련대상 선택
# 원격(인터넷, 우편) 훈련과정
elif course_num == 4:
    print("=========== 훈련대상 선택 ===========\n"
          "=              1. 구직자            =\n"
          "=              2. 근로자            =\n"
          "=              3. 기업              =\n"
          "=====================================")

    # 훈련대상 선택은 필수적이지 않으므로 try 문을 통해
    # 잘못된 값을 입력받으면 기본값으로 처리해준다.
    try:
        target_num = int(input("숫자를 입력하세요: "))
        if target_num > 3 or target_num < 1:
            raise Exception("잘못된 숫자를 입력하셨습니다!")
    except Exception as e:
        print("오류 발생 : ", e)
        print("기본값 범위 내에서 검색합니다.")
        target_num = 1

    # 훈련대상 선택
    if target_num == 1:
        # 구직자
        table_name = "seeker_url_table"
        driver.find_element_by_xpath('//*[@id="gubun1"]').click()
    elif target_num == 2:
        # 근로자
        table_name = "worker_url_table"
        driver.find_element_by_xpath('//*[@id="gubun2"]').click()
    elif target_num == 3:
        # 기업
        table_name = "corp_url_table"
        driver.find_element_by_xpath('//*[@id="gubun3"]').click()
        # 훈련유형 선택(3-기업 훈련대상일 경우에만)
        print("=========== 훈련유형 선택 ===========\n"
              "=            1. 전체                =\n"
              "=            2. 사업주지원          =\n"
              "=            3. 컨소시엄            =\n"
              "=            4. 중소기업            =\n"
              "=====================================")

        # 훈련유형 선택은 필수적이지 않으므로 try 문을 통해
        # 잘못된 값을 입력받으면 기본값으로 처리해준다.
        try:
            type_num = int(input("숫자를 입력하세요: "))
            if type_num > 4 or type_num < 1:
                raise Exception("잘못된 숫자를 입력하셨습니다!")
        except Exception as e:
            print("오류 발생 : ", e)
            print("기본값 범위 내에서 검색합니다.")
            type_num = 1

        # 훈련유형 선택
        if type_num == 1:
            # 전체
            driver.find_element_by_xpath('//*[@id="crseTracseSe1"]').click()
        elif type_num == 2:
            # 사업주지원
            driver.find_element_by_xpath('//*[@id="crseTracseSe2"]').click()
        elif type_num == 3:
            # 컨소시엄
            driver.find_element_by_xpath('//*[@id="crseTracseSe3"]').click()
        elif type_num == 4:
            # 중소기업
            driver.find_element_by_xpath('//*[@id="crseTracseSe4"]').click()

        # 훈련구분 선택(1, 2의 경우에만)
        if type_num == 1 or 2:
            print("=========== 훈련구분 선택 ===========\n"
                  "=              1. 전체              =\n"
                  "=              2. 인터넷            =\n"
                  "=              3. 우편              =\n"
                  "=              4. 스마트            =\n"
                  "=====================================")

            # 훈련구분 선택은 필수적이지 않으므로 try 문을 통해
            # 잘못된 값을 입력받으면 기본값으로 처리해준다.
            try:
                item_num = int(input("숫자를 입력하세요: "))
                if item_num > 4 or item_num < 1:
                    raise Exception("잘못된 숫자를 입력하셨습니다!")
            except Exception as e:
                print("오류 발생 : ", e)
                print("기본값 범위 내에서 검색합니다.")
                item_num = 1

            # 훈련구분 선택
            if item_num == 1:
                # 전체
                driver.find_element_by_xpath('//*[@id="traingMthCd1"]').click()
            elif item_num == 2:
                # 인터넷
                driver.find_element_by_xpath('//*[@id="traingMthCd2"]').click()
            elif item_num == 3:
                # 우편
                driver.find_element_by_xpath('//*[@id="traingMthCd3"]').click()
            elif item_num == 4:
                # 스마트
                driver.find_element_by_xpath('//*[@id="traingMthCd4"]').click()

    # 훈련대상 검색
    driver.find_element_by_class_name('btn1').click()

    # NCS 직무분류 선택
#### 임시! 대분류만 선택 ####
print("=========== NCS 직무 선택 ===========\n"
      "=     (임시 대분류 선택) 1 ~ 24     =\n"
      "=   맨 앞의 0은 빼고 입력해주세요   =\n"
      "=====================================")
try:
    ncs_num = int(input("숫자를 입력하세요: ")) + 1
    if ncs_num > 24 or ncs_num < 1:
        raise Exception("잘못된 숫자를 입력하셨습니다!")
except Exception as e:
    print("오류 발생 : ", e)
    # 잘못된 숫자를 입력할 경우 기본 값으로 설정
    ncs_num = 1

driver.find_element_by_xpath('//*[@id="upperNcsCd"]/option[' + str(ncs_num) + ']').click()
print("NCS 대분류 0" + str(ncs_num) + " 번 범위로 검색합니다.")

# 개강일자 선택
print("================= 개강일자 선택 =================\n"
      "=      1. 기본값(현재 날짜 ~ 3개월 뒤)          =\n"
      "=      2. 당해년도(올해 1월 1일 ~ 3개월 뒤)     =\n"
      "=      3. 1주일(현재 날짜 ~ 1주일 뒤)           =\n"
      "=      4. 1개월(현재 날짜 ~ 1개월 뒤)           =\n"
      "=      5. 직접 입력 예) YYYYMMDD 20191004       =\n"
      "=================================================")

# 개강일자 선택은 필수적이지 않으므로 try 문을 통해
# 잘못된 값을 입력받으면 기본값으로 처리해준다.
try:
    date_num = int(input("숫자를 입력하세요: "))
    if date_num > 5 or date_num < 1:
        raise Exception("잘못된 숫자를 입력하셨습니다!")
except Exception as e:
    print("오류 발생 : ", e)
    # 잘못된 숫자를 입력할 경우 기본 값으로 설정
    date_num = 1

if date_num == 1:
    # 기본값
    # startDate, endDate를 가진 노드의 value 속성값을 가져온다
    print("기본값 범위 내에서 검색합니다.")

elif date_num == 2:
    # 당해년도
    now = datetime.datetime.now()
    # 당해년도 1월 1일의 값을 변수에 저장하여 준다
    thisyearDate = str(now.year) + "0101"
    startDate = driver.find_element_by_xpath('//*[@id="startDate"]')
    # startDate의 기본값을 지워주고, 당해년도 1월 1일의 값을 넣어준다
    startDate.clear()
    startDate.send_keys(thisyearDate)
    startDate.submit()
    print("당해년도 범위 내에서 검색합니다.")

elif date_num == 3:
    # 1주일
    # 현재 날짜 ~ 1주일로 검색범위를 설정하는 버튼을 클릭한다.
    driver.find_element_by_xpath('//*[@id="btnWeek"]').click()
    print("일주일 범위 내에서 검색합니다.")

elif date_num == 4:
    # 1개월
    # 현재 날짜 ~ 1개월로 검색범위를 설정하는 버튼을 클릭한다.
    driver.find_element_by_xpath('//*[@id="btnMonth"]').click()
    print("1개월 범위 내에서 검색합니다.")

elif date_num == 5:
    # 직접 입력
    get_now_startDate = driver.find_element_by_xpath('//*[@id="startDate"]')
    get_now_endDate = driver.find_element_by_xpath('//*[@id="endDate"]')
    get_startDate = int(input("시작 일자를 입력하세요: "))
    get_endDate = int(input("완료 일자를 입력하세요: "))
    print("입력받은 범위에서 검색합니다.")
    startDate = driver.find_element_by_xpath('//*[@id="startDate"]')
    # startDate의 기본값을 지워주고, 입력받은 시작 일자 값을 넣어준다
    startDate.clear()
    startDate.send_keys(get_startDate)
    startDate.submit()
    endDate = driver.find_element_by_xpath('//*[@id="endDate"]')
    # endDate의 기본값을 지워주고, 입력받은 완료 일자 값을 넣어준다
    endDate.clear()
    endDate.send_keys(get_endDate)
    endDate.submit()

# startDate, endDate를 가진 노드의 value 속성값을 가져온다
startDate = driver.find_element_by_xpath('//*[@id="startDate"]').get_attribute('value')
endDate = driver.find_element_by_xpath('//*[@id="endDate"]').get_attribute('value')
# 현재 검색하려는 날짜 값을 출력한다
print("개강일자 : " + startDate + " ~ " + endDate)
# 개강일자 검색 버튼 클릭
driver.find_element_by_class_name('btn1').click()

# 탐색할 훈련정보 건 수
max_element = driver.find_element_by_css_selector('#searchForm1 > div.sort_wrap.mt70 > p > span').text
max_element = int(max_element.replace(',', ''))
print("총 훈련정보 : " + str(max_element) + "건")

# 탐색할 훈련정보 건 수에 대한 페이지 수
# 올림 수행 알고리즘-> 페이지 수에 9를 더한 뒤 10으로 나눈다
max_pages = int((max_element + 9) / 10)
print("총 페이지 수 : " + str(max_pages) + "페이지")

# 1000개 단위 반복문용 올림 알고리즘
if max_pages >= 100:
    round_up = int((max_pages + 900) / 1000)
elif max_pages < 100:
    round_up = 1

# 암묵적 대기 => DOM이 다 로드될 때까지 대기하고 먼저 로드되면 바로 진행
# 요소를 찾을 특정 시간 동안 DOM 풀링을 지시, 예를 들어 10초 이내라도 발견되면 바로 진행
driver.implicitly_wait(10)

# 원본 js 주소 저장하는 배열
original_js_arr = []
# 바로 접속 가능한 주소 저장하는 배열
# 첫번째 db에 넣어줄 배열
direct_js_arr = []

# 테이블 초기화(테이블 내 데이터 삭제)
sql = "truncate " + table_name + ";"
cur.execute(sql)

# url 가져오기
# def get_url():
for i in (range(1, round_up + 1)):
    # 1000단위 실행을 위해
    if i == 1:
        end = i + 1000
    if i is not 1:
        end = i * 1000
        if i == round_up:
            end = max_pages + 1
        i = ((i-1) * 1000) + 1
    if max_pages < 100:
        end = max_pages + 1

    for page in tqdm(range(i, end + 1), desc="Progress of save URL into DB", mininterval=1):
        try:
            # 자바스크립트 구동하기
            driver.execute_script("fn_search(%s);return false; " % page)
            time.sleep(2)
            CourseItems = driver.find_elements_by_css_selector('.tb_list>li')
            # 접속 배열 초기화
            direct_js_arr = []

            # searchForm1 > ul > li:nth-child(1) > div.cont > p.name > a
            for j, li in enumerate(CourseItems):
                # js 주소 받아오기
                original_js_arr.insert(j, li.find_element_by_css_selector('.cont a').get_attribute('onclick'))

                # 앞, 뒤 필요없는 주소 부분 / ', ' 제거
                original_js_arr[j] = original_js_arr[j].lstrip("javascript:fn_viewTracseInfo('")
                original_js_arr[j] = original_js_arr[j].rstrip("')")
                original_js_arr[j] = original_js_arr[j].split("','")

                # 바로 접속 가능한 주소로 문자열 생성
                direct_js_arr.insert(j, "http://hrd.go.kr/hrdp/co/pcobo/PCOBO0100P.do?tracseId=" + original_js_arr[j][0] +
                                     "&tracseTme=" + original_js_arr[j][1] + "&crseTracseSe=" + original_js_arr[j][2] +
                                     "&trainstCstmrId=" + original_js_arr[j][3])
            # db에 저장
            for url in direct_js_arr:
                # 저장되는 direct url print
                # print(" direct url: " + url)
                # sql문 = db에 url 저장
                sql = "insert into " + table_name + "(url) values (" + '"' + url + '"' + ");"
                cur.execute(sql)
                conn.commit()
                sqlcounter += 1
        except Exception as e1:
            print('오류', e1)
            driver.refresh();

end_time = time.time()
print("저장된 데이터 : " + str(sqlcounter))
print("실행시간 : {} 초".format(end_time-start_time))

# 종료
cur.close()
driver.close()
conn.close()
driver.quit()
