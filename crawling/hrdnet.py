# HRD-net 사이트 훈련정보 가져오기
# 로그인 시 PC 웹 사이트에서 처리가 어려울 경우 -> 모바일 로그인으로 진입
# 모듈 가져오기 (터미널에서 설치)
# pip install selenium
# pip install bs4
# pip install pymysql

from selenium import webdriver as wd
#from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
# 명시적 대기를 위해
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from DbMgr import DBHelper as Db
import time
#from Tour import TourInfo

# 사전에 필요한 정보를 로드 => 디비 혹은 쉘, 배치 파일에서 인자로 받아서 세팅
#db       = Db()
main_url = 'http://hrd.go.kr'
keyword  = 'http://hrd.go.kr/hrdp/ti/ptiao/PTIAO0100L.do'
# 상품정보를 담는 리스트 (TourInfo 리스트)
#tour_list = []

# 드라이버 로드
driver = wd.Chrome(executable_path='chromedriver.exe')

# 차후 -> 옵션 부여하여 (프록시, 에이전트 조작, 이미지를 배제)
# 크롤링을 오래 돌리면 => 임시파일들이 쌓인다!! -> 탬프 파일 삭제

# 사이트 접속 (get)
driver.get(main_url)
driver.get(keyword)

# 잠시 대기 => 페이지가 로드되고 나서 즉각적으로 데이터를 획득하는 행위는
# 명시적 대기 => 특정 요소가 로케이트(발견될 때까지) 대기
try:
    element = WebDriverWait(driver, 10).until(
        # 지정한 한개 요소가 올라오면 웨이트 종료
       EC.presence_of_element_located((By.CLASS_NAME, "content_wrap"))
   )
except Exception as e:
    print('오류 발생', e)

# 암묵적 대기 => DOM이 다 로드될 때까지 대기하고 먼저 로드되면 바로 진행
# 요소를 찾을 특정 시간 동안 DOM 풀링을 지시, 예를 들어 10초 이내라도 발견되면 바로 진행
driver.implicitly_wait( 10 )
# 절대적 대기 => time.sleep(10) -> 클라우드 페어(디도스 방어 솔루션)

# 게시판에서 데이터를 가져올 때
# 데이터가 많으면 세션(혹시 로그인을 해서 접근되는 사이트일 경우) 관리
# 특정 단위별로 로그아웃 로그인 계속 시도

# 특정 게시물이 사라질 경우 => 팝업 발생 (없는 글이라고 나옴) => 팝업 처리 검토

# 게시판을 스캔 시 => 임계점을 모름!!
# 게시판을 스캔해서 => 메타 정보 획득 => loop를 돌려서 일괄적으로 방문 접근 처리

# searchModule.SetCategoryList(1, '') 스크립트 실행
# 16은 임시값, 게시물을 넘어갔을 때 현상을 확인자

for page in range(1, 3): # 753):
    try:
        # 자바스크립트 구동하기
        driver.execute_script("fn_search(%s);return false; " % page)
        time.sleep(2)
        print("[%s] 페이지" % page)
        # 여러 사이트에서 정보를 수집할 경우 공통정보 정의 단계 필요
        # 훈련과정, 훈련유형, 훈련기관, 훈련정보, 인증기간
        tour = driver.find_elements_by_css_selector('.tb_list>li')
        #tb_lists = driver.find_elements_by_css_selector('.tb_list>li')
        # 상품 하나 하나 접근
        for li in tour:
            print( '링크주소', li.find_element_by_css_selector('.cont a').get_attribute('onclick') )\t
            print( '링크주소', li.find_element_by_css_selector('.cont a').get_attribute('onclick') )\t
            print( '훈련과정', li.find_element_by_css_selector('.cont a').text )\t
            print( '훈련유형', li.find_element_by_css_selector('.cont .system img').get_attribute('title') )\t
            print( '훈련기관', li.find_element_by_css_selector('.cont .academy a').text )\t
            print( '기관주소', li.find_element_by_css_selector('.cont .academy dd').text )\t
            for info in li.find_elements_by_css_selector('.cont .info li'):
                print ( info.text )\t
            print( '인증기간', li.find_element_by_css_selector('.cont .certifi img').get_attribute('alt') )

            # 데이터 모음
            # 데이터가 부족하거나 없을 수도 있으므로 직접 인덱스로 표현은 위험성이 있음
            #obj = TourInfo(
            #        li.find_element_by_css_selector('.cont a').get_attribute('onclick'),
            #        li.find_element_by_css_selector('.cont a').text,
            #        li.find_element_by_css_selector('.cont .system img').get_attribute('title'),
            #        li.find_element_by_css_selector('.cont .academy a').text,
            #        li.find_element_by_css_selector('.cont .academy dd').text,
            #        li.find_elements_by_css_selector('.cont .info li')[0].text,
            #        li.find_element_by_css_selector('.cont .certifi img').get_attribute('alt')
            # )
            #tour_list.append( obj )
    except Exception as e1:
        print('오류', e1)

# print (tour_list, len(tour_list) )
# print (tour_list, len(tour_list) )

#    print( tour_list, len(tour_list) )

    # 수집한 정보 개수를 루프 => 페이지 방문 => 콘텐츠 획득(상품상세정보)
#
#    for tour in tour_list:
        # conts => ContsInfo
#        print( type(tour) )
        # 링크 데이터에서 실데이터 획득
        # 분해
#        arr = tour.link.split(',')
#        if arr:
            # 대체
#           link = arr[0].replace('javascript:fn_viewTracseInfo(',' ')
            # 슬라이싱 => 앞에 ', 뒤에 ' 제거
            #detail_url = link[1:-1]
            # 상세 페이지 이동 : URL 값이 완성된 형태인지 확인 (http://~~)
            #driver.get( detail_url )
            #time.sleep(2)

        # pip install bs4
        # 현재 페이지를 BeautifulSoup 의 DOM 으로 구성
        #soup = bs( driver.page_source, 'html.parser' )
        # 현재 상세 정보 페이지에서 스케줄 정보 획득
        #data = soup.select('.tip-cover')
        #print( type(data), len(data) )
        # 데이터 sum
        #content_final = ''
        #for c in data[0].contents:
        #    content_final += str(c)

        # html 콘첸츠 데이터 전처리 (디비에 입력 가능토록)
        #import re

        #content_final = re.sub("'", '"', content_final)
        #content_final = re.sub(re.compile(r'\r\n|\r|\n|\n\r+'), '', content_final)

        #print(content_final)
        # 디비 입력 => pip install pymysql
        #db.db_insertCrawlingData(
#            tour.link,
#            tour.title
#        )

# 자제 =>

# 종료
driver.close()
driver.quit()
import sys
sys.exit()

