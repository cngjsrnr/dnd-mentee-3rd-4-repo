import requests
import time
from bs4 import BeautifulSoup
from .models import Post
from .categorization import Categorization


def Crawl():
    # 실시간 파악
    now = time.localtime()
    today = time.strftime('%Y/%m/', now)

    print("뉴스 크롤링 시작")

    # 필요한 URL  23848534 ← 경우 임의 날짜 뉴스 글 지정 후 해당 글 번호 기준으로 크롤링
    joongang1 = "https://news.joins.com/article/"
    # 23863326 #9월 2일 뉴스
    joongang2 = 23863326
    #Post.objects.filter(
    #    press="중앙일보").order_by('-news_num')[0].news_num
    ja3 = joongang2

    mk1 = "https://www.mk.co.kr/news/society/view/"
    mk2 = today
    # 907241 #9월 2일 뉴스
    mk3 = 907241
    #Post.objects.filter(press="매일경제").order_by('-news_num')[0].news_num
    mk4 = mk3

    # 각 카테고리, 제목, 내용 초기화
    category = ""
    title = ""
    contents = ""
    temp1 = 0
    temp2 = 0

    # web_data 변수에 해당 url 정보를 가져온다.
    # bs4에 html.parser로 해당 텍스트만 파싱
    # 크롤링 할 태그를 지정 및 해당 태그에 관련된 텍스트 반복 작업

    # 각 뉴스 기사 크롤링 반복 작업
    # 마지막 페이지인지 확인 어떻게 하나요?
    # 하는법 몰라서 일단 10개씩 긁어오는걸로만듬
    while True:
        if joongang2-ja3 >= 10 and mk3-mk4 >= 10:
            break

        if joongang2-ja3 < 10:
            try:
                joongang = joongang1 + str(joongang2)
                web_data = requests.get(joongang)
                temp1 = 0
            except requests.exceptions.ConnectionError:  # 3번이상 요청오류발생하면 패스
                temp1 += 1
                if temp1 >= 3:
                    joongang2 += 1
                continue

            soup = BeautifulSoup(web_data.text, "html.parser")
            crawling = "body > div.doc > header > div.mh > div > h2 > a"  # 카테고리 추출
            crawling2 = "#article_title"  # 기사 제목 추출
            crawling3 = "#article_body"  # 기사 내용 추출
            for list1 in soup.select(crawling):
                category = list1.get_text()
                #print("카테고리: " + category)

            for list2 in soup.select(crawling2):
                title = list2.get_text()
                #print("기사 제목: " + title)

            for list3 in soup.select(crawling3):
                contents = list3.get_text()
                #print(" 기사 내용: " + contents)

            #print("기사 주소 → " + joongang + "\n\n")
            print("중앙일보")
            cat = Categorization(contents)
            model_instance = Post(title=title, content=contents, category=cat,
                                  newslink=joongang, press="중앙일보", news_num=joongang2)
            model_instance.save()
            print("save 중앙일보 "+str(joongang2-ja3+1))
            joongang2 += 1

        if mk3-mk4 < 10:

            try:
                mk = mk1 + mk2 + str(mk3)
                web_data2 = requests.get(mk)
                temp2 = 0
            except requests.exceptions.ConnectionError:
                temp2 += 1
                if temp2 >= 3:
                    mk3 += 1
                continue

            soup = BeautifulSoup(web_data2.content.decode(
                'euc-kr', 'replace'), "html.parser")
            #soup = BeautifulSoup(web_data2.text, "html.parser", from_encoding='utf-8')
            crawling = "#header > div.gnb_top > ul > li.on > dl > dd.sub_on"  # 카테고리 추출
            crawling2 = "#top_header > div > div > h1"  # 기사 제목 추출
            crawling3 = "#article_body > div"  # 기사 내용 추출
            for list1 in soup.select(crawling):
                category = list1.get_text()
                #print("카테고리: " + category)

            for list2 in soup.select(crawling2):
                title = list2.get_text()
                #print("기사 제목: " + title)

            for list3 in soup.select(crawling3):
                contents = list3.get_text()
                #print("기사 내용: " + contents)

            #print("기사 주소 → " + mk + "\n\n")
            print("매일경제")
            cat = Categorization(contents)
            model_instance = Post(title=title, content=contents, category=cat,
                                  newslink=mk, press="매일경제", news_num=mk3)
            model_instance.save()
            print("save 매일경제 "+str(mk3-mk4+1))
            mk3 += 1
