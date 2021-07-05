import requests
from lxml import html
import time

keyword = '킥보드'

# 파일 정의
input_file_name = 'naver_news_킥보드_210624_171510.txt'

output_file_main_name = 'naver_news_main_' + keyword + '_' + time.strftime("%y%m%d_%H%M%S") + '.txt'
output_file_main = open(output_file_main_name, "w", encoding="utf-8")
# 열머리글 입력
output_file_main.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format('번호', '키워드', '매체', '날짜', '제목', 'URL', '본문'))
output_file_main.close()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}

def fget_list():
    input_file = open(input_file_name, "r", encoding="utf-8")
    input_text = input_file.read()
    lines = input_text.splitlines()
    lists=[]
    for line in lines[:]:
        elms = line.strip().split("\t")
        news_title = elms[2]
        try:
            url = elms[3]
        except:
            url = ''
        lists.append([news_title, url])
    # 열머리글을 제외한 데이터 반환
    return lists[1:]

def fwrite_news_main(count, news_media, news_date, news_title, news_url, news_article):
    print([count, keyword, news_media, news_date, news_title, news_url, news_article])
    output_file_main = open(output_file_main_name, "a", encoding="utf-8")
    output_file_main.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(count, keyword, news_media, news_date, news_title,news_url,news_article))
    return

def fcrawl_news_main(count, news_title, news_url):
    html_req = requests.get(news_url, headers=headers)
    tree = html.fromstring(html_req.content)

    try:
        news_media = tree.xpath('//div[@class="press_logo"]/a/img/@title')[0]
    except:
        news_media = ''
    try:
        news_date = tree.xpath('//div[@class="sponsor"]/span[@class="t11"]/text()')[0]
    except:
        news_date = ''
    try:
        news_article = tree.xpath('//div[@id="articleBodyContents"]/descendant-or-self::text()[not(ancestor::script)]')
    except:
        news_article = ''

    news_article = " ".join(news_article).replace("\n", " ").replace("\t", " ").replace("\r", "").strip()
    fwrite_news_main(count, news_media, news_date, news_title, news_url, news_article)

    return


def fmain():
    lists = fget_list()
    count = 1
    for list in lists[:]:
        print(list)
        news_title = list[0]
        news_url = list[1]
        if len(news_url) == 0:
            continue
        fcrawl_news_main(count, news_title, news_url)
        time.sleep(6)
        count += 1

fmain()