import requests
from bs4 import BeautifulSoup
from datetime import date
from pprint import pprint

from .module.database import DataBase

def GisickInCrawling(_keyword, _page):
    keyword = _keyword.replace(' ', '+')
    start_date, end_date = date.today().strftime("%Y.%m.%d."), date.today().strftime("%Y.%m.%d.")

    html = requests.get("https://kin.naver.com/search/list.nhn?sort=date&section=kin&query={}&page={}&period={}%7C{}".format(keyword, _page, start_date, end_date))
    bs   = BeautifulSoup(html.text, "html.parser").select('.basic1 > li > dl > dt > a')

    return [ [ _.get('href'), _.text ] for _ in bs ]

if __name__ == "__main__":
    GisickInCrawling('컴퓨터 조립', 1)
    DataBase.insert_search(  )