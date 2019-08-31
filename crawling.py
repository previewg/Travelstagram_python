# 유튜브 크롤링
from selenium import webdriver as wd
import urllib
from bs4 import BeautifulSoup
import urllib.request as REQ

options = wd.ChromeOptions()	
options.add_argument('headless')	
options.add_argument('disable-gpu')	
driver = wd.Chrome( 'static/chromedriver.exe', options=options)

# 암시적으로 최대 1초간 기다린다
driver.implicitly_wait(1)

def youtube_crawling( country ):

    url = 'https://www.youtube.com/results?search_query='
    keyword = urllib.parse.quote('%s 여행 vlog' %country)
    sorting='&sp=CAASBAgFEAE%253D'
    f_url = url+keyword+sorting

    driver.get( f_url )

    # 암시적으로 최대 2초간 기다린다
    driver.implicitly_wait(2)

    videos = driver.find_elements_by_tag_name('ytd-video-renderer')

    href = []
    img = []
    title = []   

    for v in videos[:9]:
        href.append(v.find_element_by_id('thumbnail').get_attribute('href') )
        img.append(v.find_element_by_id('img').get_attribute('src') )
        title.append(v.find_element_by_id('video-title').text )
    
    yout = { 'ytitle':title, 'yimg':img, 'yhref':href }
    return yout

def tripadviser_crawling(country):
    url_base = 'https://www.tripadvisor.co.kr/Search?geo=1&searchNearby=&pid=3826&redirect=&startTime=1548818336538&uiOrigin=MASTHEAD&q='
    keyword = urllib.parse.quote('%s' %country)
    url_sub='&sid=8058B739B8F09F099E61B762107533C11548818581315&ssrc=g&rf=1'
    turl=url_base+keyword+url_sub

    driver.get(turl)

    # 암시적으로 최대 5초간 기다린다
    driver.implicitly_wait(5)

    tkey = []
    tcount = []
    thref = []

    # 검색어
    for one in driver.find_elements_by_class_name('result-title>span'):
        tkey.append(one.text)
        thref_base = 'https://www.tripadvisor.co.kr/Search?q='
        thref.append(thref_base + urllib.parse.quote('%s' %one.text))
    # 리뷰 수
    for one in driver.find_elements_by_class_name('review-count'):
        tcount.append(one.text)

    # 딕셔너리 형태
    print(tkey[1:5])
    trip = { 'tkey':tkey[1:5], 'tcount':tcount[1:5], 'thref':thref[1:5] }
    return trip

def basic_content( country ):
    url_base ='https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query='
    keyword = urllib.parse.quote('%s' %country)
    response = REQ.urlopen(url_base + keyword)
    soup = BeautifulSoup(response, 'html.parser')
    source = soup.select_one('.nacon_area')
    if not source:
        str1 = str(soup.select_one('.title_wrap'))
        str2 = str(soup.select_one('.overseas_tab'))
        str3 = str(soup.select_one('.overseas_city'))
        source = str1+str2+str3
    return source