from datetime import date
import time, re

import requests
from bs4 import BeautifulSoup

class CrawlingQNA():
    def __init__(self, _index, _cb_function):
        self.datas, self.is_stop = [], False
        self.cb_function, self.index = _cb_function, _index
        self.LINK_LIST = [
            "https://kin.naver.com/qna/list.nhn",               # 질문
            "https://kin.naver.com/qna/kinupList.nhn",          # qna
            "https://kin.naver.com/qna/kinupList.nhn?dirId=13", # 쥬니버네이버
            "https://kin.naver.com/qna/kinupList.nhn?dirId=20"  # 고민
        ]
        self.link = self.LINK_LIST[self.index]
    
    ###############################################
    # private functions
    # qna 크롤링
    def __qna_index(self):
        html = requests.get("{}".format( self.link ))
        bs   = BeautifulSoup(html.text, "html.parser").select('#au_board_list > tr > td.title > a')
        return [ [ "https://kin.naver.com{}".format(_.get('href')), _.text ] for _ in bs ]
    
    ###############################################
    def get_lists(self):
        _result = []
        for _ in self.__qna_index( ):
            _result.append( _ )
            
        if len(self.datas) == 0:
            self.datas = _result
            self.cb_function( _result )
        else:
            if self.datas[0][1] != _result[0][1]:
                self.datas = _result
                self.cb_function( _result )
        
        return _result