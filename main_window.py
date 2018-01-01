# !/usr/bin/env python
# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import QMainWindow, QAction, QActionGroup, QFileDialog, QColorDialog, QFontDialog, QMessageBox
from PyQt5.QtCore import Qt, QRect, QCoreApplication, QFile, QProcess, QDir
from PyQt5.QtGui import QPixmap, QColor, QFont, QIcon
from hexagonal_map_widget import HexagonalMapWidget
from sample_widget import LandformsSample, MidSample, PositionSample
from parameter import MapData, S_NAME_LIST, L_QTY_LIST, T_NAME_LIST, P_NAME_LIST
from functools import partial
import resource_file


class MainWindow(QMainWindow):
    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.sceneID = None
        self.sceneFilename = None
        self.menuBarHeight = 28
        self._initHexagonalMap()
        self._initFileMenu()
        self._initEditMenu()
        self._initFontMenu()
        self._initColorMenu()
        self._initDisplayMenu()
        self._initOtherMenu()
        self.setWindowIcon(QIcon(QPixmap(":/icon/icon.png").scaled(32, 32)))
        self.setFixedSize(self.cellSize * 22, self.cellSize * 20 + 50)
        self.show()

    def _initHexagonalMap(self):
        self.setStyleSheet("QMainWindow{background-color: gray}")
        self.setCentralWidget(HexagonalMapWidget(self))
        self.centralWidget().borderLayer.setUsualColor(QColor(Qt.lightGray))
        self.centralWidget().terrainLayer.setTextMargin(3)
        self.centralWidget().terrainLayer.setTextFont(QFont("微软雅黑", 8, QFont.Bold))
        self.centralWidget().terrainLayer.setTextAlignment(Qt.AlignRight | Qt.AlignTop)
        self.centralWidget().terrainLayer.setTextColor(QColor(Qt.yellow))
        self.centralWidget().valueLayer.setTextMargin(3)
        self.centralWidget().valueLayer.setTextFont(QFont("微软雅黑", 8, QFont.Bold))
        self.centralWidget().valueLayer.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.centralWidget().valueLayer.setTextColor(QColor(Qt.blue))
        self.centralWidget().positionLayer.setTextMargin(1)
        self.centralWidget().positionLayer.setTextFont(QFont("微软雅黑", 7, QFont.Bold))
        self.centralWidget().positionLayer.setTextAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.centralWidget().positionLayer.setTextColor(QColor(Qt.white))
        self.cellSize = self.centralWidget().cellSize
        self.setWindowTitle("三国志III MD版地图编辑器")
        self.statusBar()

    def _initFileMenu(self):
        self.fileMenu = self.menuBar().addMenu("文件")

        self.loadLandformsMenu = self.fileMenu.addMenu("载入地貌")
        landforms_action_group = QActionGroup(self)
        load_landforms_custom = QAction("打开地貌图片…", self)
        load_landforms_custom.triggered.connect(self.loadLandformsCustomFile)
        load_landforms_custom.setCheckable(True)
        self.loadLandformsMenu.addAction(load_landforms_custom)
        landforms_action_group.addAction(load_landforms_custom)
        self.loadLandformsMenu.addSeparator()
        for landforms_id in range(len(L_QTY_LIST)):
            load_landforms_id = QAction("第{0}组默认地貌".format(landforms_id + 1), self)
            load_landforms_id.triggered.connect(partial(self.loadLandformsID, landforms_id))
            load_landforms_id.setCheckable(True)
            self.loadLandformsMenu.addAction(load_landforms_id)
            landforms_action_group.addAction(load_landforms_id)
        landforms_action_group.setExclusive(True)

        self.loadSceneDataMenu = self.fileMenu.addMenu("载入地图")
        scene_data_action_group = QActionGroup(self)
        load_scene_data_custom = QAction("打开地图文件…", self)
        load_scene_data_custom.triggered.connect(self.loadSceneDataCustomFile)
        load_scene_data_custom.setCheckable(True)
        self.loadSceneDataMenu.addAction(load_scene_data_custom)
        scene_data_action_group.addAction(load_scene_data_custom)
        self.loadSceneDataMenu.addSeparator()
        load_city_data_menu = self.loadSceneDataMenu.addMenu("都市")
        for scene_id in range(46):
            load_scene_data_id = QAction(S_NAME_LIST[scene_id], self)
            load_scene_data_id.triggered.connect(partial(self.loadSceneDataID, scene_id))
            load_scene_data_id.setCheckable(True)
            load_city_data_menu.addAction(load_scene_data_id)
            scene_data_action_group.addAction(load_scene_data_id)
        load_battlefield_data_menu = self.loadSceneDataMenu.addMenu("战场")
        for scene_id in range(46, len(S_NAME_LIST)):
            load_scene_data_id = QAction(S_NAME_LIST[scene_id], self)
            load_scene_data_id.triggered.connect(partial(self.loadSceneDataID, scene_id))
            load_scene_data_id.setCheckable(True)
            load_battlefield_data_menu.addAction(load_scene_data_id)
            scene_data_action_group.addAction(load_scene_data_id)
        self.loadSceneDataMenu.setEnabled(False)
        scene_data_action_group.setExclusive(True)

        self.saveAction = QAction("保存地图文件", self)
        self.saveAction.triggered.connect(self.saveSceneFile)
        self.saveAction.setEnabled(False)
        self.fileMenu.addAction(self.saveAction)

    def _initEditMenu(self):
        self.editMenu = self.menuBar().addMenu("编辑")

        self.landformsSample = QAction("地貌", self)
        self.landformsSample.setCheckable(True)
        self.landformsSample.setEnabled(False)
        self.landformsSample.triggered.connect(self.openLandformsSampleWindow)
        self.editMenu.addAction(self.landformsSample)

        self.midSample =  QAction("地形和防守权重", self)
        self.midSample.setCheckable(True)
        self.midSample.triggered.connect(self.openMidSampleWindow)
        self.editMenu.addAction(self.midSample)

        self.positionSample = QAction("出阵站位", self)
        self.positionSample.setCheckable(True)
        self.positionSample.triggered.connect(self.openPositionSampleWindow)
        self.editMenu.addAction(self.positionSample)

        self.editMenu.setEnabled(False)

    def _initFontMenu(self):
        self.fontMenu = self.menuBar().addMenu("字体")

        select_terrain_text_font = QAction("地形显示字体", self)
        select_terrain_text_font.triggered.connect(self.selectTerrainTextFont)
        self.fontMenu.addAction(select_terrain_text_font)

        select_value_text_font = QAction("防守权重字体", self)
        select_value_text_font.triggered.connect(self.selectValueTextFont)
        self.fontMenu.addAction(select_value_text_font)

        select_position_text_font = QAction("出阵站位字体", self)
        select_position_text_font.triggered.connect(self.selectPositionTextFont)
        self.fontMenu.addAction(select_position_text_font)

    def _initColorMenu(self):
        self.colorMenu = self.menuBar().addMenu("颜色")

        select_terrain_text_color = QAction("地形显示文字颜色", self)
        select_terrain_text_color.triggered.connect(self.selectTerrainTextColor)
        self.colorMenu.addAction(select_terrain_text_color)

        select_value_text_color = QAction("防守权重文字颜色", self)
        select_value_text_color.triggered.connect(self.selectValueTextColor)
        self.colorMenu.addAction(select_value_text_color)

        select_position_text_color = QAction("出阵站位文字颜色", self)
        select_position_text_color.triggered.connect(self.selectPositionTextColor)
        self.colorMenu.addAction(select_position_text_color)

        select_border_color = QAction("边框颜色", self)
        select_border_color.triggered.connect(self.selectBorderColor)
        self.colorMenu.addAction(select_border_color)

    def _initDisplayMenu(self):
        self.displayMenu = self.menuBar().addMenu("图层")

        landforms_layer = QAction("地貌图像", self)
        landforms_layer.setCheckable(True)
        landforms_layer.setChecked(True)
        landforms_layer.triggered.connect(self.displayLandformsLayer)
        self.displayMenu.addAction(landforms_layer)

        terrain_layer = QAction("地型显示", self)
        terrain_layer.setCheckable(True)
        terrain_layer.setChecked(True)
        terrain_layer.triggered.connect(self.displayTerrainLayer)
        self.displayMenu.addAction(terrain_layer)

        value_layer = QAction("防守权重", self)
        value_layer.setCheckable(True)
        value_layer.setChecked(True)
        value_layer.triggered.connect(self.displayValueLayer)
        self.displayMenu.addAction(value_layer)

        position_layer = QAction("出阵站位", self)
        position_layer.setCheckable(True)
        position_layer.setChecked(True)
        position_layer.triggered.connect(self.displayPositionLayer)
        self.displayMenu.addAction(position_layer)

        border_layer = QAction("边框", self)
        border_layer.setCheckable(True)
        border_layer.setChecked(True)
        border_layer.triggered.connect(self.displayBorderLayer)
        self.displayMenu.addAction(border_layer)

    def _initOtherMenu(self):
        self.otherMenu = self.menuBar().addMenu("其他")

        extract_program = QAction("文件压缩工具", self)
        extract_program.triggered.connect(self.openExtractProgram)
        self.otherMenu.addAction(extract_program)

        about = QAction("使用说明", self)
        about.triggered.connect(self.aboutWindow)
        self.otherMenu.addAction(about)

    def loadLandformsID(self, blocks_id: int):
        landforms_image = QPixmap(":/landforms/landforms{0}.png".format(blocks_id))
        self.landformsQuantity = L_QTY_LIST[blocks_id]
        self.landformsBlocks = []
        for block_id in range(self.landformsQuantity):
            box = QRect((block_id % 16) * 16, (block_id // 16) * 16, 16, 16)
            landforms_block = landforms_image.copy(box).scaled(self.cellSize, self.cellSize)
            self.landformsBlocks.append(landforms_block)
        for dummy in range(158 - len(self.landformsBlocks)):
            self.landformsBlocks.append(self.landformsBlocks[0])
        if self.sceneID:
            self.loadSceneDataID(self.sceneID)
        elif self.sceneFilename:
            self.loadSceneDataCustomFile(self.sceneFilename)
        self.loadSceneDataMenu.setEnabled(True)
        self.editMenu.setEnabled(True)
        self.saveAction.setEnabled(True)
        self.landformsSample.setEnabled(True)

    def loadLandformsCustomFile(self):
        file_path = QFileDialog.getOpenFileName(self, "选择自定义地貌图片", "./", "BMP图片(*.bmp);;All Files (*)")[0]
        if file_path:
            landforms_image = QPixmap(file_path)
            max_row = landforms_image.height() // 16
            max_col = landforms_image.width() // 16
            self.landformsQuantity = min((max_row + 1) * (max_col + 1), 159)
            self.landformsBlocks = []
            for block_id in range(max_row * max_col):
                box = QRect((block_id % 16) * 16, (block_id // 16) * 16, 16, 16)
                landforms_block = landforms_image.copy(box).scaled(self.cellSize, self.cellSize)
                self.landformsBlocks.append(landforms_block)
            for dummy in range(158 - len(self.landformsBlocks)):
                self.landformsBlocks.append(self.landformsBlocks[0])
            self.loadSceneDataMenu.setEnabled(True)
            self.editMenu.setEnabled(True)
            self.saveAction.setEnabled(True)
            self.landformsSample.setEnabled(True)
        else:
            self.sender().setChecked(False)

    def loadSceneDataID(self, scene_id):
        self.sceneID = scene_id
        self.mapData = MapData(scene_id)
        self.setWindowTitle("{0} - {1}".format("三国志III MD版地图编辑器", S_NAME_LIST[self.sceneID]))
        l_data = self.mapData.landformsData
        for block_id in range(len(l_data)):
            self.centralWidget().landformsLayer.cells[block_id].setPixmap(self.landformsBlocks[l_data[block_id]])
        t_data = self.mapData.terrainData
        for block_id in range(len(t_data)):
            self.centralWidget().terrainLayer.cells[block_id].setText(T_NAME_LIST[t_data[block_id]])
        v_data = self.mapData.valueData
        for block_id in range(len(v_data)):
            self.centralWidget().valueLayer.cells[block_id].setText(str(v_data[block_id]))
        p_data = self.mapData.positionData
        for block_id in range(len(p_data)):
            self.centralWidget().positionLayer.cells[block_id].setText(P_NAME_LIST[p_data[block_id]])

    def loadSceneDataCustomFile(self):
        file_path = QFileDialog.getOpenFileName(self, "选择地图文件", "./", "All Files (*)")[0]
        if file_path:
            self.sceneID = 255
            self.sceneFilename = file_path
            self.mapData = MapData(0, file_path)
            l_data = self.mapData.landformsData
            for block_id in range(len(l_data)):
                self.centralWidget().landformsLayer.cells[block_id].setPixmap(self.landformsBlocks[l_data[block_id]])
            t_data = self.mapData.terrainData
            for block_id in range(len(t_data)):
                self.centralWidget().terrainLayer.cells[block_id].setText(T_NAME_LIST[t_data[block_id]])
            v_data = self.mapData.valueData
            for block_id in range(len(v_data)):
                self.centralWidget().valueLayer.cells[block_id].setText(str(v_data[block_id]))
            p_data = self.mapData.positionData
            for block_id in range(len(p_data)):
                self.centralWidget().positionLayer.cells[block_id].setText(P_NAME_LIST[p_data[block_id]])
        else:
            self.sender().setChecked(False)

    def saveSceneFile(self):
        file_path = QFileDialog.getSaveFileName(self, "保存地图文件", "./", "地图文件 (*.bin)")[0]
        if file_path:
            self.mapData.saveFile(file_path)

    def selectTerrainTextFont(self):
        font, ok = QFontDialog.getFont(self.centralWidget().terrainLayer.textFont, self, "设置地形显示字体")
        if ok:
            self.centralWidget().terrainLayer.setTextFont(font)

    def selectValueTextFont(self):
        font, ok = QFontDialog.getFont(self.centralWidget().valueLayer.textFont, self, "设置防守权重字体")
        if ok:
            self.centralWidget().valueLayer.setTextFont(font)

    def selectPositionTextFont(self):
        font, ok = QFontDialog.getFont(self.centralWidget().positionLayer.textFont, self, "设置出阵站位字体")
        if ok:
            self.centralWidget().positionLayer.setTextFont(font)

    def selectTerrainTextColor(self):
        color = QColorDialog.getColor(QColor(self.centralWidget().terrainLayer.textColor).toRgb(), self, "设置地形显示文字颜色")
        if color:
            self.centralWidget().terrainLayer.setTextColor(color)

    def selectValueTextColor(self):
        color = QColorDialog.getColor(QColor(self.centralWidget().valueLayer.textColor).toRgb(), self, "设置防守权重文字颜色")
        if color:
            self.centralWidget().valueLayer.setTextColor(color)

    def selectPositionTextColor(self):
        color = QColorDialog.getColor(QColor(self.centralWidget().positionLayer.textColor).toRgb(), self, "设置出阵站位文字颜色")
        if color:
            self.centralWidget().positionLayer.setTextColor(color)

    def selectBorderColor(self):
        color = QColorDialog.getColor(QColor(self.centralWidget().borderLayer.usualColor).toRgb(), self, "设置边框颜色")
        if color:
            self.centralWidget().borderLayer.setUsualColor(color)

    def displayLandformsLayer(self):
        if self.sender().isChecked():
            self.centralWidget().landformsLayer.setVisible(True)
        else:
            self.centralWidget().landformsLayer.setVisible(False)

    def displayTerrainLayer(self):
        if self.sender().isChecked():
            self.centralWidget().terrainLayer.setVisible(True)
        else:
            self.centralWidget().terrainLayer.setVisible(False)

    def displayValueLayer(self):
        if self.sender().isChecked():
            self.centralWidget().valueLayer.setVisible(True)
        else:
            self.centralWidget().valueLayer.setVisible(False)

    def displayPositionLayer(self):
        if self.sender().isChecked():
            self.centralWidget().positionLayer.setVisible(True)
        else:
            self.centralWidget().positionLayer.setVisible(False)

    def displayBorderLayer(self):
        if self.sender().isChecked():
            self.centralWidget().borderLayer.setVisible(True)
        else:
            self.centralWidget().borderLayer.setVisible(False)
            
    def openLandformsSampleWindow(self):
        if self.sender().isChecked():
            self.landformsSampleWindow = LandformsSample(self.landformsBlocks, self.landformsQuantity, self.cellSize)
            self.landformsSampleWindow.show()
        else:
            self.landformsSampleWindow.close()

    def openMidSampleWindow(self):
        if self.sender().isChecked():
            self.midSampleWindow = MidSample(
                self.cellSize, self.centralWidget().terrainLayer.textColor, self.centralWidget().valueLayer.textColor)
            self.midSampleWindow.show()
        else:
            self.midSampleWindow.close()

    def openPositionSampleWindow(self):
        if self.sender().isChecked():
            self.positionSampleWindow = PositionSample()
            self.positionSampleWindow.show()
        else:
            self.positionSampleWindow.close()

    def openExtractProgram(self):
        exe_path = "{0}/压缩解压.exe".format(QDir().currentPath())
        QFile.copy(":/exe/compress.exe", exe_path)
        process = QProcess()
        process.startDetached(exe_path)

    def aboutWindow(self):
        QMessageBox.about(self, "使用说明",
                          """1.通过“文件->载入地貌”来载入地貌组合，已内建了游戏内置的6套组合<br>
                          2.支持自定义地貌组合图片，图片尺寸不超过256×256，单块大小为16×16<br>
                          3.再通过“文件->载入地图”来载入地图数据，已内建游戏内置全部地图<br>
                          4.可以通过“编辑”菜单打开素材窗口，拖放素材到对应地图格子实现编辑<br>
                          5.地图共4层，分别为地貌、地形、AI防守重视权重、出阵站位<br>
                          6.允许自定义各层次显示的字体和颜色，并支持选择隐藏各个图层<br>
                          7.编辑完成后通过“文件->保存地图文件”将编辑完毕的地图保存为文件<br>
                          8.内嵌了压缩程序，文件通过压缩可写入ROM，可参考银河漫步地图编辑器<br>
                          <div align="right">created by 全力全开</div>""")

    def mouseMoveEvent(self, QEvent):
        if QEvent.pos() in self.centralWidget().geometry():
            x = QEvent.pos().x() // self.cellSize
            if x % 2 is 0:
                row = (QEvent.pos().y() - self.menuBarHeight) // self.cellSize
                col = x
            elif (QEvent.pos().y() - self.menuBarHeight) < self.cellSize // 2:
                row = 20
                col = (QEvent.pos().x() - self.cellSize) // self.cellSize // 2

            elif (QEvent.pos().y() - self.menuBarHeight) > self.cellSize * 20 - self.cellSize // 2:
                row = 20
                col = (QEvent.pos().x() - self.cellSize) // self.cellSize // 2 + 11
            else:
                row = ((QEvent.pos().y() - self.menuBarHeight) - self.cellSize // 2) // self.cellSize
                col = x
            self.statusBar().showMessage("({0}, {1})".format(row, col))
        else:
            self.statusBar().clearMessage()

    def dragEnterEvent(self, QEvent):
        if QEvent.mimeData().hasFormat("text/plain"):
            QEvent.accept()
        else:
            QEvent.ignore()

    def dragMoveEvent(self, QEvent):
        if QEvent.mimeData().hasFormat("text/plain"):
            if QEvent.pos() in self.centralWidget().geometry():
                x = QEvent.pos().x() // self.cellSize
                if x % 2 is 0:
                    row = (QEvent.pos().y() - self.menuBarHeight) // self.cellSize
                    col = x
                elif (QEvent.pos().y() - self.menuBarHeight) < self.cellSize // 2:
                    row = 20
                    col = (QEvent.pos().x() - self.cellSize) // self.cellSize // 2
                elif (QEvent.pos().y() - self.menuBarHeight) > self.cellSize * 20 - self.cellSize // 2:
                    row = 20
                    col = (QEvent.pos().x() - self.cellSize) // self.cellSize // 2 + 11
                else:
                    row = ((QEvent.pos().y() - self.menuBarHeight) - self.cellSize // 2) // self.cellSize
                    col = x
                self.statusBar().showMessage("(拖放到{0}, {1})".format(row, col))
                QEvent.accept()
            else:
                self.statusBar().clearMessage()
        else:
            QEvent.ignore()

    def dropEvent(self, QEvent):
        if QEvent.mimeData().hasFormat("text/plain"):
            x = QEvent.pos().x() // self.cellSize
            if x % 2 is 0:
                row = (QEvent.pos().y() - self.menuBarHeight) // self.cellSize
                col = x
            elif (QEvent.pos().y() - self.menuBarHeight) < self.cellSize // 2:
                row = 20
                col = (QEvent.pos().x() - self.cellSize) // self.cellSize // 2
            elif (QEvent.pos().y() - self.menuBarHeight) > self.cellSize * 20 - self.cellSize // 2:
                row = 20
                col = (QEvent.pos().x() - self.cellSize) // self.cellSize // 2 + 11
            else:
                row = ((QEvent.pos().y() - self.menuBarHeight) - self.cellSize // 2) // self.cellSize
                col = x
            if self.sceneID is not None:
                layer = QEvent.mimeData().text().split(".")[0]
                data = int(QEvent.mimeData().text().split(".")[1])
                if layer == "landforms":
                    self.centralWidget().landformsLayer.cells[row * 22 + col].setPixmap(self.landformsBlocks[data])
                    self.mapData.landformsData[row * 22 + col] = data
                elif layer == "terrain":
                    self.centralWidget().terrainLayer.cells[row * 22 + col].setText(T_NAME_LIST[data])
                    self.mapData.terrainData[row * 22 + col] = data
                elif layer == "value":
                    self.centralWidget().valueLayer.cells[row * 22 + col].setText(str(data))
                    self.mapData.valueData[row * 22 + col] = data
                elif layer == "position":
                    self.centralWidget().positionLayer.cells[row * 22 + col].setText(P_NAME_LIST[data])
                    self.mapData.positionData[row * 22 + col] = data
            QEvent.accept()
        else:
            QEvent.ignore()

    def closeEvent(self, QEvent):
        QCoreApplication.quit()
