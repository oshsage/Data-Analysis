import requests
from lxml import html

# 웹문서 가져오기
url = "http://www.paxnet.co.kr/tbbs/list?tbbsType=L&id=005930"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}
# html_req: 가져올 문서를 저장할 변수
html_req = requests.get(url, headers=headers)


tree = html.fromstring(html_req.content)
titles = tree.xpath('//div[@class="title"]/p/a/text()')
print(titles)
#
results = []
for title in titles:
    print(title)
    title_clean = title.replace("\n"," ").replace("\t", " ").replace("\r", " ").strip()
    results.append(title_clean)
print(len(results))
print(results)

# <a class="best-title" href="javascript:bbsWrtView(150357585271117);">◆ 삼성전자(우): 강력 매수 신호 발생: 5달간 조정 마무리 --&gt;매수 적기        </a>