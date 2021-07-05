import requests
from lxml import html

keyword = '킥보드'
page_num = 1
url = 'https://search.naver.com/search.naver' \
      '?where=news&sm=tab_pge' \
      '&query='+keyword+'&sort=1&photo=0&field=0&pd=3' \
                        '&ds=2021.04.01&de=2021.04.30&mynews=0' \
                        '&office_type=0&office_section_code=0&news_office_checked=' \
                        '&nso=so:dd,p:from20210401to20210430,a:all&start=' + str(page_num)
print(url)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
html_req= requests.get(url, headers=headers)


tree = html.fromstring(html_req.content)
bodies = tree.xpath('//ul[@class="list_news"]/li')

results = []

for body in bodies:
    news_title = body.xpath('.//a[@class="news_tit"]/@title')[0]
    try:
        news_url = body.xpath('.//a[@class="info"]/@href')[0]
    except:
        news_url = ''
    results.append([news_title, news_url])
print(results)