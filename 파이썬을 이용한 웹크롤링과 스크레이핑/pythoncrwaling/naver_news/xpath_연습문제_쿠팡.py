import requests
from lxml import html

# 웹문서 가져오기
url = "https://www.coupang.com/np/search?component=&q=%ED%82%A5%EB%B3%B4%EB%93%9C&channel=user"
headers = {"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}
# html_req: 가져올 문서를 저장할 변수
html_req = requests.get(url, headers=headers)

# html_req의 내용을 html 구조로 해석
tree = html.fromstring(html_req.content)
titles = tree.xpath('//div[@class="descriptions-inner"]/div[@class="name"/text()')

for title in titles:
    print(title)