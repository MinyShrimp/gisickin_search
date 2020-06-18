from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5 import uic

from .base_form import BaseForm
from module.database import DataBase

class SearchKeywordForm(BaseForm):
    def __init__(self):
        BaseForm.__init__(self, 'search_keyword.ui')

        # set ui callback function
        self.ui.btn_add.clicked.connect(self.btn_add_click_event)
        self.ui.btn_fix.clicked.connect(self.btn_fix_click_event)
        self.ui.btn_delete.clicked.connect(self.btn_delete_click_event)
        self.ui.tb_keywords.itemClicked.connect(self.tb_keywords_click_event)

        # init
        self.__init_table_items()
        self.ui.input_text.clear()

        # class values
        self.datas = []
    
    ###########################################
    # private functions
    def __add_table_item(self, text):
        rowPosition = self.ui.tb_keywords.rowCount()
        self.ui.tb_keywords.insertRow( rowPosition )
        self.ui.tb_keywords.setItem( rowPosition, 0, QtWidgets.QTableWidgetItem(text) )
    
    def __init_table_items(self):
        self.ui.tb_keywords.clearContents()
        self.ui.tb_keywords.setRowCount(0)
        self.datas = DataBase.select_keyword_all()
        for d in self.datas:
            self.__add_table_item(d[1])
    
    ###########################################
    # overloading function
    def show(self):
        self.ui.setVisible(True)
        self.__init_table_items()
    
    ###########################################
    # Table Events
    def tb_keywords_click_event(self):
        self.ui.input_text.setText( self.ui.tb_keywords.currentItem().text() )

    ###########################################
    # Button Events
    def btn_add_click_event(self):
        _text = self.ui.input_text.text()

        DataBase.insert_keyword( _text )

        self.ui.input_text.clear()
        self.__init_table_items()

    def btn_fix_click_event(self):
        _index, _text = self.ui.tb_keywords.currentRow(), self.ui.input_text.text()

        DataBase.update_keyword( self.datas[_index][0], _text )

        self.ui.input_text.clear()
        self.__init_table_items()

    def btn_delete_click_event(self):
        _index = self.ui.tb_keywords.currentRow()

        DataBase.delete_keyword( self.datas[_index][0] )
        self.datas.pop(_index)

        self.ui.input_text.clear()
        self.__init_table_items()