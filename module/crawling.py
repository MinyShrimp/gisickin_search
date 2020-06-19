from datetime import date
from pprint import pprint
import threading, time

import requests
from bs4 import BeautifulSoup

class Crawling(threading.Thread):
    def __init__(self, _keywords, _s_page, _e_page, _date, _cb_function):
        threading.Thread.__init__(self)

        self.datas, self.is_stop = [], False
        self.start_page, self.end_page = _s_page, _e_page
        self.date, self.cb_function = _date.strftime("%Y.%m.%d."), _cb_function
        self.__set_keywords( _keywords )

    ###############################################
    # private functions
    def __set_keywords(self, _keywords):
        self.keywords = [ _.replace(' ', '+') for _ in _keywords ]

    # 지식인 크롤링
    def __intellectual_index(self, _keyword, _page):
        html = requests.get("https://kin.naver.com/search/list.nhn?sort=date&section=kin&query={}&page={}&period={}%7C{}".format(_keyword, _page, self.date, self.date))
        bs   = BeautifulSoup(html.text, "html.parser").select('.basic1 > li > dl > dt > a')
        return [ [ _.get('href'), _.text ] for _ in bs ]

    ###############################################
    # 일정시간마다 체크해서 업데이트 되면(저장된 파일 목록과 다르면)
    def run(self):
        while True:
            if self.is_stop:
                self.datas = []
                return None

            _result = []
            for key in self.keywords:
                for page in range(self.start_page, self.end_page+1):
                    for _ in self.__intellectual_index( key, page ):
                        if not (_[1] in [ __[1] for __ in _result]):
                            _result.append( _ )
            
            if len(self.datas) == 0:
                self.datas = _result
                self.cb_function( _result )
            else:
                if self.datas[0][1] != _result[0][1]:
                    self.datas = _result
                    self.cb_function( _result )
            time.sleep(5)