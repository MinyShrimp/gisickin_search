import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5 import uic

class BaseForm():
    def __init__(self, filepath):
        self.ui = uic.loadUi(os.path.join(os.getcwd(), "res", "ui", filepath))
        self.ui.setVisible(False)

        # set ui callback function
        self.ui.btn_close.clicked.connect(self.btn_close_click_event)

        # class values
        self.cb_functions = []
        self.ui.hideEvent = self.hide_event
    
    def show(self):
        self.ui.setVisible(True)
    
    def hide(self):
        self.ui.setVisible(False)

    def hide_event(self, event):
        for _ in self.cb_functions:
            _()
    
    def add_callback_function(self, cbf):
        self.cb_functions.append( cbf )

    def btn_close_click_event(self):
        self.hide()