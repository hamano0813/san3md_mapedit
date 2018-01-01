#!/usr/bin/env python
#-*- coding:utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
import sys


class DateEdit(QSqlTableModel):
    def __init__(self, *args):
        super(DateEdit, self).__init__(*args)



app = QApplication(sys.argv)
b = QWidget()
a = DateEdit(b)

b.show()

file = QFile(":/QSS/black.qss")
file.open(QFile.ReadOnly)
stylesheet = bytearray(file.readAll()).decode("UTF-8")
app.setStyleSheet(stylesheet)
sys.exit(app.exec_())