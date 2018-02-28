# !/usr/bin/env python
# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from typing import List


class _HexagonalWidget(QWidget):
    def __init__(self, *args):
        super(_HexagonalWidget, self).__init__(*args)
        self.cellSize: int = 32
        self.cells: List[QLabel] = []
        self.setFixedSize(self.cellSize * 22, self.cellSize * 20)
        self.textFont = None
        self.textColor = None
        self._initUI()

    def _initUI(self):
        for row in range(20):
            for col in range(22):
                cell: QLabel = QLabel(self)
                cell.setFixedSize(self.cellSize, self.cellSize)
                self.cells.append(cell)
                if col % 2 is 0:
                    cell.move(self.cellSize * col, self.cellSize * row)
                elif row is 19:
                    cell.move(self.cellSize * col, self.cellSize * row + self.cellSize // 2)
                    cell.setVisible(False)
                else:
                    cell.move(self.cellSize * col, self.cellSize * row + self.cellSize // 2)

    def setTextAlignment(self, alignment: Qt.AlignmentFlag):
        for cell in self.cells:
            cell.setAlignment(alignment)

    def setTextFont(self, font: QFont):
        self.textFont = font
        for cell in self.cells:
            cell.setFont(font)

    def setTextColor(self, color: QColor):
        self.textColor = color.name()
        for cell in self.cells:
            cell.setStyleSheet(f"color: {self.textColor};")

    def setTextMargin(self, margin: int):
        for cell in self.cells:
            cell.setMargin(margin)


class _HexagonalInterpolationWidget(_HexagonalWidget):
    def __init__(self, *args):
        super(_HexagonalInterpolationWidget, self).__init__(*args)
        self._interpolationUI()

    def _interpolationUI(self):
        for col in range(22):
            cell = QLabel(self)
            cell.setFixedSize(self.cellSize, self.cellSize)
            self.cells.append(cell)
            cell.move(col % 11 * self.cellSize * 2 + self.cellSize, col // 11 * self.cellSize * 20 - self.cellSize // 2)


class _HexagonalBorderWidget(_HexagonalInterpolationWidget):
    def __init__(self, *args):
        super(_HexagonalBorderWidget, self).__init__(*args)
        self.usualColor = None

    def setUsualColor(self, color):
        self.usualColor: str = color.name()
        for cell in self.cells:
            cell.setStyleSheet(f"border:1px solid {self.usualColor};")


class HexagonalMapWidget(QWidget):
    def __init__(self, *args):
        super(HexagonalMapWidget, self).__init__(*args)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self._landformsLayer()
        self._terrainLayer()
        self._valueLayer()
        self._positionLayer()
        self._borderLayer()
        self.setFixedSize(self.landformsLayer.size())

    def _landformsLayer(self):
        self.landformsLayer = _HexagonalInterpolationWidget(self)
        self.cellSize: int = self.landformsLayer.cellSize

    def _borderLayer(self):
        self.borderLayer = _HexagonalBorderWidget(self)

    def _terrainLayer(self):
        self.terrainLayer = _HexagonalWidget(self)

    def _valueLayer(self):
        self.valueLayer = _HexagonalWidget(self)

    def _positionLayer(self):
        self.positionLayer = _HexagonalWidget(self)
        for cell in self.positionLayer.cells:
            cell.setWordWrap(True)
