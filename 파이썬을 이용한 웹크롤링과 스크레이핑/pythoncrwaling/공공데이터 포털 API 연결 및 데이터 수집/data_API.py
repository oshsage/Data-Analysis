import requests
import time
from xml.etree import ElementTree           # xml문서를 해석할 수 있는 모듈
from datetime import date                   # 기준월을 바꾸기 위한 모듈
from dateutil.relativedelta import relativedelta    # 월을 증가, 감소시키기 위해 날짜를 계산할 수 있는 모듈 사용

input_file_name = "region_code5.csv"
secret_key = '21dpBw3ONi0aSCZjgM5zk46nOk4Zbc%2BLBkwC0khxO0wDd2Typ91qLps6faPaU88za7vPpfTawOqx9K8RjnDw5w%3D%3D'
date_start = date(2020, 6, 1)
date_end = date(2020, 5, 1)

output_file_name = "trade_apt_api_" + time.strftime("%y%m%d_%H%M%S") + ".txt"
output_file = open(output_file_name, 'w', encoding='utf-8')
output_file.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format('기준연월', '지역명', '지역코드', '법정동', '아파트', '거래금액', '년', '월', '일', '건축년도', '전용면적', '층'))
output_file.close()

def fget_list():
    input_file = open(input_file_name, 'r', encoding='euc-kr')      # 파일 열고
    input_text = input_file.read()                                  # 읽어오고
    lines = input_text.splitlines()                                 # 행단위로 자르고
    print(lines)
    lists = []
    for line in lines:                                              # 하나씩 뽑아
        line = line.replace('"', '')                                # " 를 ' 로
        elms = line.strip().split(",")                              # , 단위로 자르고
        region_name = elms[0]                                       # 첫번째 원소는 이름
        region_code = elms[1]                                       # 두번재 원소는 코드
        if region_code[:2] == "11":                                 # 코드 앞의 두자리는 지역(11은 서울)
            lists.append([region_name, region_code])                # lists에 이름이랑 코드 추가
    return lists


def fget_html(region_name, region_code, this_ym):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
    page_url = "http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?LAWD_CD="+str(region_code)+"&DEAL_YMD="+str(this_ym)+"&serviceKey="+str(secret_key)
    print(page_url)
    response = requests.get(page_url, headers = headers)
    tree = ElementTree.fromstring(response.content)
    elements = tree.iter(tag="item")

    for element in elements:
        price = element.find("거래금액").text
        const_year = element.find("건축년도").text
        year = element.find("년").text
        month = element.find("월").text
        day = element.find("일").text
        dong = element.find("법정동").text
        apt_name = element.find("아파트").text
        square = element.find("전용면적").text
        stair = element.find("층").text
        elm_list = [this_ym, region_name, region_code, dong, apt_name, price, year, month,day, const_year, square, stair]
        print(elm_list)
        output_file = open(output_file_name, "a", encoding='utf-8')
        output_file.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(this_ym, region_name, region_code, dong, apt_name, price, year,month, day, const_year, square, stair))
        output_file.close()
    return

def fmain():
    date_this = date_start
    lists = fget_list()

    while date_this >= date_end:
        print(date_this)
        this_year = str(date_this.year)
        this_month = str(date_this.month)

        if len(this_month) == 1:
            this_month = "0" + str(this_month)
        this_ym = this_year + this_month

        print(this_ym)
        for list in lists:
            region_name = list[0]
            region_code = list[1]
            print(region_name, region_code)
            fget_html(region_name, region_code, this_ym)

        date_this = date_this - relativedelta(months=1)
    return

fmain()
