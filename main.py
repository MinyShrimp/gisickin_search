import sys, os
import threading
from datetime import date

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import uic

import clipboard

from form.post_index     import PostIndexForm
from form.search_ban     import SearchBanForm
from form.search_keyword import SearchKeywordForm

from module.database import DataBase
from module.crawling import Crawling
from module.chrome_selenium import Chrome

class MainForm():
    def __init__(self):
        self.ui = uic.loadUi(os.path.join(os.getcwd(), "res", "ui", "main.ui"))
        self.ui.setWindowIcon( QtGui.QIcon( os.path.join(os.getcwd(), "res", "icon", "icon.ico") ) )

        # set ui callback function
        self.ui.closeEvent = self.closeEvent

        self.ui.btn_start.clicked.connect(self.btn_start_click_event)
        self.ui.btn_answer.clicked.connect(self.btn_answer_click_event)
        self.ui.btn_keyword.clicked.connect(self.btn_keyword_click_event)
        self.ui.btn_clear.clicked.connect(self.btn_clear_click_event)

        self.ui.tb_posts.itemDoubleClicked.connect(self.tb_posts_d_click_event)
        self.ui.tb_answers.itemDoubleClicked.connect(self.tb_answers_d_click_event)

        # init tables
        self.__init_tb_keywords_items()
        self.__init_tb_answers_items()
        self.__init_tb_ban_items()
        self.ui.show()

        # init QDateEdit to today
        self.ui.date.setDate(date.today())

        # set child form
        self.post_index_form     = PostIndexForm()
        self.post_index_form.add_callback_function( self.__init_tb_answers_items )

        self.search_ban_form     = SearchBanForm()
        self.search_ban_form.add_callback_function( self.__init_tb_ban_items )

        self.search_keyword_form = SearchKeywordForm()
        self.search_keyword_form.add_callback_function( self.__init_tb_keywords_items )

        # class values
        self.is_searching = False
        self.search_datas = []

        # daemon thread
        self.web_crawling = None
        self.chrome = None
        self.__start_chrome()
    
    def closeEvent(self, event):
        if self.chrome != None:
            self.chrome.quit()

    ###########################################
    # private functions
    def __init_tb_search_items(self, _datas):
        self.ui.tb_posts.clearContents()
        self.ui.tb_posts.setRowCount(len(_datas))
        for i, v in enumerate(_datas):
            self.ui.tb_posts.setItem( i, 0, QtWidgets.QTableWidgetItem(v[1]) )
    
    def __init_tb_ban_items(self):
        _datas = DataBase.select_ban_all()
        _len_datas = len(_datas)

        self.ui.tb_ban.clearContents()
        self.ui.tb_ban.setRowCount(_len_datas)
        for i, v in enumerate(_datas):
            self.ui.tb_ban.setItem( i, 0, QtWidgets.QTableWidgetItem(v[1]) )

    def __init_tb_keywords_items(self):
        _datas = DataBase.select_keyword_all()
        _len_datas = len(_datas)

        self.ui.tb_keywords.clearContents()
        self.ui.tb_keywords.setRowCount(_len_datas)
        for i, v in enumerate(_datas):
            self.ui.tb_keywords.setItem( i, 0, QtWidgets.QTableWidgetItem(v[1]) )
    
    def __init_tb_answers_items(self):
        _datas = DataBase.select_post_all()
        _len_datas = len(_datas)

        self.ui.tb_answers.clearContents()
        self.ui.tb_answers.setRowCount(_len_datas)        
        for i, v in enumerate(_datas):
            self.ui.tb_answers.setItem( i, 0, QtWidgets.QTableWidgetItem(v[1]) )
            self.ui.tb_answers.setItem( i, 1, QtWidgets.QTableWidgetItem(v[2]) )

    def __start_thread(self):
        _tmp_date = self.ui.date.date()
        self.web_crawling = Crawling( 
            [ _[1] for _ in DataBase.select_keyword_all() ], # keyword
            [ _[1] for _ in DataBase.select_ban_all() ],     # ban
            self.ui.pg_intellectual_start.value(), self.ui.pg_intellectual_end.value(), # 페이지
            date( _tmp_date.year(), _tmp_date.month(), _tmp_date.day() ), # 기간
            self.__init_tb_search_items # callback function
        )
        self.web_crawling.daemon = True
        self.web_crawling.start()
        self.ui.btn_start.setText('검색 종료')

    def __stop_thread(self):
        self.search_datas = self.web_crawling.datas
        self.web_crawling.is_stop = True
        self.ui.btn_start.setText('검색 시작')
        self.web_crawling = None

    def __load_chrome(self):
        self.chrome = Chrome()

    def __start_chrome(self):
        t = threading.Thread(target=self.__load_chrome, args=())
        t.start()

    ###########################################
    # Button Events
    def btn_keyword_click_event(self):
        if self.ui.tabWidget.currentIndex() == 0:
            self.search_keyword_form.show()
        else:
            self.search_ban_form.show()
    
    def btn_answer_click_event(self):
        self.post_index_form.show()
    
    def btn_start_click_event(self):
        self.is_searching = not self.is_searching

        # 시작
        if self.is_searching: 
            self.__start_thread()
        # 종료
        else:
            self.__stop_thread()

    def btn_clear_click_event(self):
        self.ui.tb_posts.clearContents()
        self.ui.tb_posts.setRowCount(0)

    ###########################################
    # Table Item Double Click Events
    def tb_posts_d_click_event(self, item):
        #self.ui.view_web.load( QUrl(_data[item.row()][0]) )
        _data = self.search_datas if self.web_crawling == None else self.web_crawling.datas
        try:
            self.chrome.get( _data[item.row()][0] )
        except:
            self.__start_chrome()

    def tb_answers_d_click_event(self, item):
        _data = DataBase.select_post_all()
        _tmp = _data[item.row()][2]
        _tmp.replace('\n', '\r\n')
        clipboard.copy( _tmp )
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainForm()
    sys.exit( app.exec() )