import sys, os

from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import uic

from form.post_index     import PostIndexForm
from form.search_keyword import SearchKeywordForm

from module.database import DataBase

class MainForm():
    def __init__(self):
        self.ui = uic.loadUi(os.path.join(os.getcwd(), "res", "ui", "main.ui"))

        # set ui callback function
        self.ui.btn_start.clicked.connect(self.btn_start_click_event)
        self.ui.btn_answer.clicked.connect(self.btn_answer_click_event)
        self.ui.btn_keyword.clicked.connect(self.btn_keyword_click_event)

        # init
        self.__init_tb_keywords_items()
        self.__init_tb_answers_items()
        self.ui.show()

        # set child form
        self.post_index_form     = PostIndexForm()
        self.post_index_form.add_callback_function( self.__init_tb_answers_items )

        self.search_keyword_form = SearchKeywordForm()
        self.search_keyword_form.add_callback_function( self.__init_tb_keywords_items )

        # class values
        self.is_searching = False

    ###########################################
    # private functions
    def __init_tb_keywords_items(self):
        self.ui.tb_keywords.clearContents()
        self.ui.tb_keywords.setRowCount(0)
        datas = DataBase.select_keyword_all()
        for d in datas:
            rowPosition = self.ui.tb_keywords.rowCount()
            self.ui.tb_keywords.insertRow( rowPosition )
            self.ui.tb_keywords.setItem( rowPosition, 0, QtWidgets.QTableWidgetItem(d[1]) )
    
    def __init_tb_answers_items(self):
        self.ui.tb_answers.clearContents()
        self.ui.tb_answers.setRowCount(0)
        datas = DataBase.select_post_all()
        for d in datas:
            rowPosition = self.ui.tb_answers.rowCount()
            self.ui.tb_answers.insertRow( rowPosition )
            self.ui.tb_answers.setItem( rowPosition, 0, QtWidgets.QTableWidgetItem(d[1]) )
            self.ui.tb_answers.setItem( rowPosition, 1, QtWidgets.QTableWidgetItem(d[2]) )

    ###########################################
    # Button Events
    def btn_keyword_click_event(self):
        self.search_keyword_form.show()
    
    def btn_answer_click_event(self):
        self.post_index_form.show()
    
    def btn_start_click_event(self):
        self.is_searching = not self.is_searching
        self.ui.btn_start.setText('검색 종료' if self.is_searching else '검색 시작')
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainForm()
    sys.exit( app.exec() )