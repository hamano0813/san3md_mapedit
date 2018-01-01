# !/usr/bin/env python
# -*- coding:utf-8 -*-

from PyQt5.QtCore import QFile
import struct
import resource_file


def load_resource(path: str):
    rc_file = QFile(path)
    rc_file.open(QFile.ReadOnly)
    return bytearray(rc_file.readAll())


S_NAME_LIST = load_resource(":/parameter/scene_name").decode("UTF-8").splitlines()

L_QTY_LIST = [int(line) for line in load_resource(":/parameter/landforms_quantity").decode("UTF-8").splitlines()]

T_NAME_LIST = load_resource(":/parameter/terrain_name").decode("UTF-8").splitlines()

P_NAME_LIST = S_NAME_LIST.copy()
P_NAME_LIST.extend(["" for i in range(256 - len(S_NAME_LIST))])


class MapData(object):
    def __init__(self, scene_id: int, scene_file=None):
        super(MapData, self).__init__()
        if scene_file is not None:
            file = open(scene_file, "rb")
            self._originalData = bytearray(file.read())
        else:
            self._originalData = load_resource(":/scene_data/{0:02d}.bin".format(scene_id))
        self.landformsData = self._getLandformsData()
        self.terrainData = self._getTerrainData()
        self.valueData = self._getValueData()
        self.positionData = self._getPositionData()

    def _getLandformsData(self):
        return list(struct.unpack_from("{0}B".format(22 * 21), self._originalData, 0))

    def _getTerrainData(self):
        return [data & 0x0F for data in struct.unpack_from("{0}B".format(22 * 20), self._originalData, 22 * 21)]

    def _getValueData(self):
        return [data >> 4 & 0x0F for data in struct.unpack_from("{0}B".format(22 * 20), self._originalData, 22 * 21)]

    def _getPositionData(self):
        return list(struct.unpack_from("{0}B".format(22 * 20), self._originalData, 22 * (21 + 20)))

    def saveFile(self, filename: str):
        landforms_struct = struct.pack("{0}B".format(len(self.landformsData)), *self.landformsData)
        mid_data = [self.valueData[i] << 4 | self.terrainData[i] for i in range(len(self.terrainData))]
        mid_struct = struct.pack("{0}B".format(len(self.terrainData)), *mid_data)
        position_struct = struct.pack("{0}B".format(len(self.positionData)), *self.positionData)
        data_struct = landforms_struct + mid_struct + position_struct
        with open(filename, "wb") as file:
            file.write(data_struct)
        return bytearray(data_struct)
