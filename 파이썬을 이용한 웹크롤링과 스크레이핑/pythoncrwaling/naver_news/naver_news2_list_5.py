import requests
from lxml import html
import time

keywords = ['킥보드', '자전거']

# 파일 만들기
output_file_name = 'naver_news_list.txt'                                            # 파일명
output_file = open(output_file_name, "w", encoding="utf-8")                         # 파일 만들기
output_file.write("{}\t{}\t{}\t{}\n".format('페이지', '키워드', '제목', 'URL'))        # 파일에 카테고리 쓰기
output_file.close()                                                                 # 파일 닫기

# 파일에 새로운 내용 추가
def fwrite_news(i, keyword, news_title_clean, news_url):
    print([i, keyword, news_title_clean, news_url])
    # 파일열기
    output_file = open(output_file_name, "a", encoding="utf-8")
    # 파일에 데이터 쓰기
    output_file.write("{}\t{}\t{}\t{}\n".format(i,keyword, news_title_clean,news_url))
    # 파일 닫기
    output_file.close()
    return

# 웹 크롤링
def fcrwal_news(keyword, i):
    page_num = (i - 1) * 10 + 1
    url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query='+keyword+'&sort=1&photo=0&field=0&pd=3&ds=2021.04.01&de=2021.04.30&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:from20210401to20210430,a:all&start='+str(page_num)
    print(url)
    headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
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
        news_title_clean = news_title.replace("\n", "").replace("\t","").replace("\r","").strip()
        results.append(results)

        # 파일에 데이터 저장
        fwrite_news(i, keyword, news_title_clean, news_url)
    return results

# 키워드마다 1~3 페이지 기사 출력
def fmain():
    for keyword in keywords:
        for i in range(1, 4):
            print(i)
            results = fcrwal_news(keyword, i)
            print(results)
            time.sleep(6)
fmain()