# 시스템 기능을 사용하기 위한 모듈
import sys
import time
import requests
from lxml import html
import selenium.webdriver as webdriver

driver = webdriver.Chrome('C://chromedriver/chromedriver.exe')
url_start = 'https://news.naver.com'


# sys.argv[0]: 자신의 파일경로 정보, sys.argv[1]: 입력받은 값
if len(sys.argv) == 2: # 길이가 2라는 것은 기본적으로 있는 파일경로 정보 + 입력 값이라는 것
    keywords = list(sys.argv[1].split(','))     # 입력받은 값이 존재하면 갑을 ,로 분리시킨다.
else:
    keywords = ['NH은행','NH증권']

def fmake_file(keyword):
    # 파일 이름에 현재 년월일시분초를 추가하여 중복 방지
    output_file_name = 'naver_news_' + keyword + "_" + time.strftime("%y%m%d_%H%M%S") + '.txt'
    output_file = open(output_file_name, "w", encoding="utf-8")
    output_file.write("{}\t{}\t{}\t{}\n".format('페이지', '키워드', '제목', 'URL'))
    output_file.close()
    return output_file_name
def fwrite_news(i, keyword, news_title_clean, news_url, output_file_name):
    print([i, keyword, news_title_clean, news_url])
    output_file = open(output_file_name, "a", encoding="utf-8")
    output_file.write("{}\t{}\t{}\t{}\n".format(i, keyword, news_title_clean, news_url))
    output_file.close()
    return

def fcrawl_news(keyword, i, output_file_name):
    page_num = (i - 1) * 10 + 1
    url = 'https://search.naver.com/search.naver' \
        '?where=news&sm=tab_pge' \
        '&query=' + keyword + '&sort=1&photo=0&field=0&pd=3' \
        '&ds=2021.01.01&de=2021.04.30&mynews=0&office_type=0' \
        '&office_section_code=0&news_office_checked=' \
        '&nso=so:dd,p:from20210101to20210430,a:all&start=' + str(page_num)
    print(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'}
    html_req = requests.get(url, headers=headers)
    tree = html.fromstring(html_req.content)
    bodies = tree.xpath('//ul[@class="list_news"]/li')
    results = []
    for body in bodies:
        news_title = body.xpath('.//a[@class="news_tit"]/@title')[0]
        try:
            news_url = body.xpath('.//a[@class="info"]/@href')[0]
        except:
            news_url = ''
        news_title_clean = news_title.replace("\n", "").replace("\t", "").replace("\r", "").strip()
        results.append([i, keyword, news_title_clean, news_url])
        fwrite_news(i, keyword, news_title_clean, news_url, output_file_name)
    return results


def fmain():
    for keyword in keywords:
        output_file_name = fmake_file(keyword)
        for i in range(1,4):
            print(i)
            results = fcrawl_news(keyword, i, output_file_name)
            print(results)
            time.sleep(6)
fmain()
