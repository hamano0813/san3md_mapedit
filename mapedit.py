# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QFile
from program.main_window import MainWindow
import sys

app = QApplication(sys.argv)
file = QFile(':/QSS/black.qss')
file.open(QFile.ReadOnly)
stylesheet = bytearray(file.readAll()).decode('UTF-8')
app.setStyleSheet(stylesheet)
window = MainWindow()
sys.exit(app.exec_())
