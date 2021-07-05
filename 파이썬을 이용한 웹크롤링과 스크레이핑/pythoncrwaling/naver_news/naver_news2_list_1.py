import requests
from lxml import html
url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query=킥보드&sort=1&photo=0&field=0&pd=3' \
'&ds=2021.01.01&de=2021.04.30&mynews=0&office_type=0&office_section_code=0&news_office_checked=' \
'&nso=so:dd,p:from20210101to20210430,a:all&start=1'
print(url)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'}
html_req = requests.get(url, headers=headers)
tree = html.fromstring(html_req.content)
bodies = tree.xpath('//ul[@class="list_news"]/li')
print(len(bodies))
print(bodies)
results = []
for body in bodies:
    # [0]을 붙이는 이유: 속성(@)을 대상으로 값을 불러오면 리스트를 불러오기 때문. 깔끔하게 문자열 값을 가져오고 싶다면 [0]로 원소를 선택하는 방향으로 가야함.
    news_title = body.xpath('.//a[@class="news_tit"]/@title')[0]
    print(news_title)
    news_broad = body.xpath('.//a[@class="info press"]/text()')
    news_time = body.xpath('.//span[@class="info"]/text()')
    try:
        news_url = body.xpath('.//a[@class="info"]/@href')[0]
    except:
        news_url = ''
    news_title_clean = news_title.replace("\n", "").replace("\t", "").replace("\r", "").strip()
    results.append([news_title_clean, news_url,news_broad,news_time])
print(results)


