from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5 import uic

from .base_form import BaseForm
from .post_add  import PostAddForm

from module.database import DataBase

class PostIndexForm(BaseForm):
    def __init__(self):
        BaseForm.__init__(self, "post_index.ui")

        # set ui callback function
        self.ui.btn_add.clicked.connect(self.btn_add_click_event)
        self.ui.btn_fix.clicked.connect(self.btn_fix_click_event)
        self.ui.btn_delete.clicked.connect(self.btn_delete_click_event)
        self.__init_table_items()

        # set child form
        self.post_add_form = PostAddForm()
        self.post_add_form.add_callback_function( self.__init_table_items )

        # class values
        self.datas = []

    ###########################################
    # private functions
    def __add_table_item(self, title, contents):
        rowPosition = self.ui.tb_posts.rowCount()
        self.ui.tb_posts.insertRow( rowPosition )
        self.ui.tb_posts.setItem( rowPosition, 0, QtWidgets.QTableWidgetItem(title) )
        self.ui.tb_posts.setItem( rowPosition, 1, QtWidgets.QTableWidgetItem(contents) )
    
    def __init_table_items(self):
        self.ui.tb_posts.clearContents()
        self.ui.tb_posts.setRowCount(0)
        self.datas = DataBase.select_post_all()
        for d in self.datas:
            self.__add_table_item(d[1], d[2])

    ###########################################
    # overloading function
    def show(self):
        self.ui.setVisible(True)
        self.__init_table_items()
    
    ###########################################
    # Button Events
    def btn_add_click_event(self):
        self.post_add_form.show()

    def btn_fix_click_event(self):
        _index = self.ui.tb_posts.currentRow()
        self.post_add_form.show( self.datas[_index][0], self.datas[_index][1], self.datas[_index][2] )

    def btn_delete_click_event(self):
        _index = self.ui.tb_posts.currentRow()

        DataBase.delete_post( self.datas[_index][0] )
        self.datas.pop(_index)

        self.__init_table_items()