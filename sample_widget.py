# !/usr/bin/env python
# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QDrag, QFont
from PyQt5.QtCore import Qt, QMimeData
from parameter import T_NAME_LIST, S_NAME_LIST
import math


class DataLabel(QLabel):
    def __init__(self, *args):
        super(DataLabel, self).__init__(*args)
        self.setAcceptDrops(True)
        self.mappedData = None

    def setData(self, data):
        self.mappedData = data

    def mousePressEvent(self, QEvent):
        if QEvent.button() == Qt.LeftButton:
            mime_data = QMimeData()
            mime_data.setText(self.mappedData)
            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.exec_(Qt.CopyAction)

    def dragEnterEvent(self, QEvent):
        if QEvent.mimeData().hasFormat("text/plain"):
            QEvent.accept()
        else:
            QEvent.ignore()

    def dragMoveEvent(self, QEvent):
        if QEvent.mimeData().hasFormat("text/plain"):
            QEvent.accept()
        else:
            QEvent.ignore()


class LandformsSample(QWidget):
    def __init__(self, landforms_blocks, landforms_quantity, cell_size, *args):
        super(LandformsSample, self).__init__(*args)
        self.setAcceptDrops(True)
        self.setWindowFlags(Qt.SubWindow | Qt.WindowStaysOnTopHint)
        self.landformsBlocks = landforms_blocks
        self.landfromsQuantity = landforms_quantity
        self.cellSize = cell_size
        self.setFixedSize((self.cellSize + 1) * 16, (self.cellSize + 1) * (math.ceil(self.landfromsQuantity / 16)))
        self.setWindowTitle("地貌")
        self.initUI()

    def initUI(self):
        for block_id in range(self.landfromsQuantity):
            cell = DataLabel(self)
            cell.setPixmap(self.landformsBlocks[block_id])
            cell.setData("landforms.{0}".format(block_id))
            cell.setFixedSize(self.cellSize, self.cellSize)
            cell.move(block_id % 16 * (self.cellSize + 1), block_id // 16 * (self.cellSize + 1))


class MidSample(QWidget):
    def __init__(self, cell_size, terrain_text_color, value_text_color, *args):
        super(MidSample, self).__init__(*args)
        self.setAcceptDrops(True)
        self.setWindowFlags(Qt.SubWindow | Qt.WindowStaysOnTopHint)
        self.terrainList = T_NAME_LIST
        self.cellSize = cell_size
        self.terrainTextColor = terrain_text_color
        self.valueTextColor = value_text_color
        self.setStyleSheet("background-color: gray;")
        self.setFixedSize(self.cellSize * 2 + 15, (self.cellSize + 1) * 16 + 10)
        self.setWindowTitle("地形和防守权重")
        self.initUI()

    def initUI(self):
        for terrain_id in range(len(self.terrainList)):
            cell = DataLabel(self)
            cell.setFixedSize(self.cellSize, self.cellSize)
            cell.setFont(QFont("微软雅黑", 16))
            cell.setAlignment(Qt.AlignCenter)
            cell.setText(self.terrainList[terrain_id])
            cell.setStyleSheet("border: 2px double black; color: {0};".format(self.terrainTextColor))
            cell.setData("terrain.{0}".format(terrain_id))
            cell.move(5, 5 + terrain_id * (self.cellSize + 1))

        for value_id in range(16):
            cell = DataLabel(self)
            cell.setFixedSize(self.cellSize, self.cellSize)
            cell.setFont(QFont("微软雅黑", 16))
            cell.setAlignment(Qt.AlignCenter)
            cell.setText("{0:d}".format(value_id))
            cell.setStyleSheet("border: 2px double black; color: {0};".format(self.valueTextColor))
            cell.setData("value.{0}".format(value_id))
            cell.move(10 + self.cellSize, 5 + value_id * (self.cellSize + 1))


class PositionSample(QWidget):
    def __init__(self, *args):
        super(PositionSample, self).__init__(*args)
        self.setAcceptDrops(True)
        self.setWindowFlags(Qt.SubWindow | Qt.WindowStaysOnTopHint)
        self.positionList = S_NAME_LIST
        self.setStyleSheet("background-color: gray;")
        self.setFixedSize(810, (len(self.positionList) // 10 + 1) * 32)
        self.setWindowTitle("出阵站位")
        self.initUI()

    def initUI(self):
        for position_id in range(len(self.positionList)):
            cell = DataLabel(self)
            cell.setFixedSize(80, 30)
            cell.setFont(QFont("微软雅黑", 10))
            cell.setAlignment(Qt.AlignVCenter)
            cell.setText("{0}.{1}".format(position_id + 1, self.positionList[position_id]))
            cell.setStyleSheet("color: white; border: 1px double black")
            cell.setData("position.{0}".format(position_id))
            cell.move(position_id % 10 * 81, position_id // 10 * 32)
        none_cell = DataLabel(self)
        none_cell.setFixedSize(80, 30)
        none_cell.setFont(QFont("微软雅黑", 10))
        none_cell.setAlignment(Qt.AlignVCenter)
        none_cell.setText("255.無")
        none_cell.setStyleSheet("border: 1px double black")
        none_cell.setData("position.255")
        none_cell.move((len(self.positionList) + 1) % 10 * 81, (len(self.positionList) + 1) // 10 * 32)
