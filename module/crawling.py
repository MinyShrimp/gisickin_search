import requests
from bs4 import BeautifulSoup
from datetime import date
from pprint import pprint

from .database import DataBase

class Crawling():
    def __init__(self):
        pass

# 지식인 크롤링
# 최근 1 ~ 3 페이지
def GisickInCrawling(_keyword, _page):
    keyword = _keyword.replace(' ', '+')
    start_date, end_date = date.today().strftime("%Y.%m.%d."), date.today().strftime("%Y.%m.%d.")

    html = requests.get("https://kin.naver.com/search/list.nhn?sort=date&section=kin&query={}&page={}&period={}%7C{}".format(keyword, _page, start_date, end_date))
    bs   = BeautifulSoup(html.text, "html.parser").select('.basic1 > li > dl > dt > a')

    return [ [ _.get('href'), _.text ] for _ in bs ]

# 일정시간마다 체크해서 업데이트 되면(저장된 파일 목록과 다르면)
# 그 부분만 insert
def checker():
    GisickInCrawling('컴퓨터 조립', 1)

if __name__ == "__main__":
    checker()
    # DataBase.insert_search(  )