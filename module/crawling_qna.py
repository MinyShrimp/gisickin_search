from datetime import date
import time, re

import requests, re, time
from bs4 import BeautifulSoup

class CrawlingQNA():
    def __init__(self, _index, _cb_function):
        self.datas = []
        self.cb_function, self.index = _cb_function, _index
        self.LINK_LIST = [
            "https://kin.naver.com/qna/list.nhn?view=card",               # 질문
            "https://kin.naver.com/qna/kinupList.nhn",                    # qna
            "https://kin.naver.com/qna/list.nhn?view=card&dirId=13",      # 쥬니버네이버
            "https://kin.naver.com/qna/kinupList.nhn?view=card&dirId=20"  # 고민
        ]
        self.link = self.LINK_LIST[self.index]
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    
    ###############################################
    # private functions
    def __get_ng(self, _str):
        p = re.compile( '내공\d+' )
        _tmp = p.match( _str )
        if _tmp != None:
            return _tmp.group()
        return None

    # qna 크롤링
    def __qna_index(self):
        html = requests.get("{}".format( self.link ), headers=self.header)
        bs   = BeautifulSoup(html.text, "html.parser").select('#au_board_list > tr > td.title > a')
        return [ [ "https://kin.naver.com{}".format(_.get('href')), _.text, _.text ] for _ in bs ]
    
    def __card_index(self):
        html = requests.get("{}".format( self.link ), headers=self.header)
        bs = BeautifulSoup(html.text, "html.parser").select('ul.quest_area > li > div.lst_q')

        _result = []
        for _ in bs:
            _herf  = "https://kin.naver.com{}".format(_.select('strong.tit > a')[0].get('href')) 

            _title = _.select('strong.tit > a')[0].text
            _tmp   = self.__get_ng(_title)
            if _tmp != None:
                _title = _title.replace(_tmp, '', 1)

            try:
                _contents = _.select('p.cont > a')[0].text
                _contents = _contents.replace('\t', '').replace('\n', '').replace('                                ', '')
            except IndexError:
                _contents = ''
            _result.append( [ _herf, _title, _contents ] )

        return _result
    
    ###############################################
    def get_lists(self):
        if self.index == 1:
            _result = self.__qna_index( )
        else:
            _result = self.__card_index( )
            
        if len(self.datas) == 0:
            self.datas = _result
            self.cb_function( _result )
        else:
            try:
                if self.datas[0][1] != _result[0][1]:
                    self.datas = _result
                    self.cb_function( _result )
            except:
                print(self.index, self.link, len(self.datas), len(_result))
        
        return _result

if __name__ == "__main__":
    a = CrawlingQNA(2, lambda x: x)
    print( a.get_lists() )