# !/usr/bin/env python
# -*- coding:utf-8 -*-

from PyQt5.QtCore import QFile
from struct import unpack_from, pack
from typing import List
import program.resource_file


def load_resource(path: str)->bytearray:
    rc_file = QFile(path)
    rc_file.open(QFile.ReadOnly)
    return bytearray(rc_file.readAll())


S_NAME_LIST = load_resource(":/parameter/scene_name").decode("UTF-8").splitlines()
L_QTY_LIST = [int(line) for line in load_resource(":/parameter/landforms_quantity").decode("UTF-8").splitlines()]
T_NAME_LIST = load_resource(":/parameter/terrain_name").decode("UTF-8").splitlines()
P_NAME_LIST = S_NAME_LIST.copy()
P_NAME_LIST.extend(["" for i in range(256 - len(S_NAME_LIST))])


class MapData(object):
    def __init__(self, scene_id: int, scene_file: str = None):
        super(MapData, self).__init__()
        if scene_file:
            file = open(scene_file, "rb")
            self._originalData = bytearray(file.read())
        else:
            self._originalData = load_resource(f":/scene_data/{scene_id:02d}.bin")

    @property
    def landformsData(self)->List[int]:
        return list(unpack_from(f"{22*21}B", self._originalData, 0))

    @property
    def terrainData(self)->List[int]:
        return [data & 0x0F for data in unpack_from(f"{22*20}B", self._originalData, 22 * 21)]

    @property
    def valueData(self)->List[int]:
        return [data >> 4 & 0x0F for data in unpack_from(f"{22*20}B", self._originalData, 22 * 21)]

    @property
    def positionData(self)->List[int]:
        return list(unpack_from(f"{22*20}B", self._originalData, 22 * (21 + 20)))

    def saveFile(self, filename: str):
        landforms_struct = pack(f"{len(self.landformsData)}B", *self.landformsData)
        mid_data: List[int] = [self.valueData[i] << 4 | self.terrainData[i] for i in range(len(self.terrainData))]
        mid_struct = pack(f"{len(self.terrainData)}B", *mid_data)
        position_struct = pack(f"{len(self.positionData)}B", *self.positionData)
        data_struct = landforms_struct + mid_struct + position_struct
        with open(filename, "wb") as file:
            file.write(data_struct)
        return bytearray(data_struct)
