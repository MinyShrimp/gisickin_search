from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5 import uic

from .base_form import BaseForm
from module.database import DataBase

class PostAddForm(BaseForm):
    def __init__(self):
        BaseForm.__init__(self, "post_add.ui")

        # set ui callback function
        self.ui.btn_ok.clicked.connect( self.btn_ok_click_event )

        # class values
        self.isFix, self.id = False, -1

    ###########################################
    # private functions
    def __text_clear(self):
        self.ui.input_title.clear()
        self.ui.input_contents.clear()
    
    ###########################################
    # overloading function
    def show(self, id=-1, title='', contents=''):
        self.ui.setVisible(True)
        self.__text_clear()
        self.ui.input_title.setText( title )
        self.ui.input_contents.setPlainText( contents )

        self.id    = id
        self.isFix = ( id != -1 )
    
    ###########################################
    # Button Events
    def btn_ok_click_event(self):
        _title, _contents = self.ui.input_title.text(), self.ui.input_contents.toPlainText()

        if self.isFix:
            DataBase.update_post( self.id, _title, _contents )
        else:
            DataBase.insert_post( _title, _contents )
        self.hide()