import requests
import time
from bs4 import BeautifulSoup

#실시간 파악
now = time.localtime()
today = time.strftime('%Y/%m/', now)

print("뉴스 크롤링 시작")

#필요한 URL  23848534 ← 경우 임의 날짜 뉴스 글 지정 후 해당 글 번호 기준으로 크롤링
joongang1 = "https://news.joins.com/article/"
joongang2 = 23848534

mk1 = "https://www.mk.co.kr/news/society/view/"
mk2 = today
mk3 = 841062

#chosun1 = "https://news.chosun.com/site/data/html_dir/"
#chosun2 = today
#chosun3 = 2020081701853
#chosun4 = ".html"

#각 카테고리, 제목, 내용 초기화
category = ""
title = ""
contents = ""


#web_data 변수에 해당 url 정보를 가져온다.
#bs4에 html.parser로 해당 텍스트만 파싱
#크롤링 할 태그를 지정 및 해당 태그에 관련된 텍스트 반복 작업

#각 뉴스 기사 크롤링 반복 작업
while True:
    joongang = joongang1 + str(joongang2)
    web_data = requests.get(joongang)
    joongang2 += 1

    soup = BeautifulSoup(web_data.text, "html.parser")
    crawling = "body > div.doc > header > div.mh > div > h2 > a" #카테고리 추출
    crawling2 = "#article_title" # 기사 제목 추출
    crawling3 = "#article_body" # 기사 내용 추출
    for list1 in soup.select(crawling):
        category = list1.get_text()
        print("카테고리: " + category)

    for list2 in soup.select(crawling2):
        title = list2.get_text()
        print("기사 제목: " + title)

    for list3 in soup.select(crawling3):
        contents = list3.get_text()
        print(" 기사 내용: " + contents)

    print("기사 주소 → " + joongang + "\n\n")

    mk = mk1 + mk2 + str(mk3)
    web_data2 = requests.get(mk)
    mk3 += 1

    soup = BeautifulSoup(web_data2.content.decode('euc-kr', 'replace'), "html.parser")
    #soup = BeautifulSoup(web_data2.text, "html.parser", from_encoding='utf-8')
    crawling = "#header > div.gnb_top > ul > li.on > dl > dd.sub_on" #카테고리 추출
    crawling2 = "#top_header > div > div > h1" # 기사 제목 추출
    crawling3 = "#article_body > div" # 기사 내용 추출
    for list1 in soup.select(crawling):
        category = list1.get_text()
        print("카테고리: " + category)

    for list2 in soup.select(crawling2):
        title = list2.get_text()
        print("기사 제목: " + title)

    for list3 in soup.select(crawling3):
        contents = list3.get_text()
        print("기사 내용: " + contents)

    print("기사 주소 → " + mk + "\n\n")

    #chosun = chosun1 + chosun2 + str(chosun3) + chosun4
    #web_data2 = requests.get(chosun)
    #chosun3 += 1

    #soup = BeautifulSoup(web_data2.text, "html.parser")
    #crawling4 = "#csh_art_cat_id" #카테고리 추출
    #crawling5 = "#news_title_text_id" # 기사 제목 추출
    #crawling6 = "#news_body_id" # 기사 내용 추출
    #for list1 in soup.select(crawling4):
    #    category = list1.get_text()
    #    print(category)
     
    #for list2 in soup.select(crawling5):
    #    title = list2.get_text()
    #    print(title)

    #for list3 in soup.select(crawling6):
    #    contents = list3.get_text()
    #    print(contents)
