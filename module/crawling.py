from datetime import date
import threading, time, re, os

import requests
from bs4 import BeautifulSoup
from PyQt5.QtMultimedia import QSound

from crawling_qna import CrawlingQNA

class Crawling(threading.Thread):
    def __init__(self, _keywords, _bans, _sound_function, _cb_functions):
        threading.Thread.__init__(self)

        self.qnas = [ CrawlingQNA( _, _cb_functions[_+1] ) for _ in range(4) ]
        self.datas, self.cb_function = [], _cb_functions[0]
        self.sound_function = _sound_function
        self.keywords, self.bans = _keywords, _bans
        self.is_stop = False

    ###############################################
    # private functions
    def __is_str_ban(self, _str):
        for _b in self.bans:
            p = re.compile( _b )
            if p.search( _str ) is not None:
                return True
        return False
    
    def __is_str_keyword(self, _str):
        for _b in self.keywords:
            p = re.compile( _b )
            if p.search( _str ) is not None:
                return True
        return False

    ###############################################
    # 일정시간마다 체크해서 업데이트 되면(저장된 파일 목록과 다르면)
    def run(self):
        while True:
            if self.is_stop:
                self.datas = []
                for f in self.qnas:
                    f.datas = []
                return None

            #_result = [ f.get_lists() for f in qnas ]
            _result = []
            for i, f in enumerate(self.qnas):
                for _ in f.get_lists():
                    if self.__is_str_ban( _[1] ) or ( _[1] in [ __[1] for __ in self.datas] ):
                        continue
                    if self.__is_str_keyword( _[1] ):
                        _result.append(_)

            if len(_result) != 0:
                for _ in _result:
                    self.datas.append( _ )
                self.cb_function( self.datas )
                self.sound_function()