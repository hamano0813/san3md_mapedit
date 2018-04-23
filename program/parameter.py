# !/usr/bin/env python
# -*- coding:utf-8 -*-

from PyQt5.QtCore import QFile
from struct import unpack_from, pack
from typing import List
import program.rec


def load_resource(path: str)->bytearray:
    rc_file = QFile(path)
    rc_file.open(QFile.ReadOnly)
    return bytearray(rc_file.readAll())


S_NAME_LIST = load_resource(':/parameter/scene_name').decode('UTF-8').splitlines()
L_QTY_LIST = [int(line) for line in load_resource(':/parameter/landforms_quantity').decode('UTF-8').splitlines()]
T_NAME_LIST = load_resource(':/parameter/terrain_name').decode('UTF-8').splitlines()
P_NAME_LIST = S_NAME_LIST.copy()
P_NAME_LIST.extend(['' for i in range(256 - len(S_NAME_LIST))])


class MapData(object):
    def __init__(self, scene_id: int, scene_file: str = None):
        super(MapData, self).__init__()
        if scene_file:
            file = open(scene_file, 'rb')
            self._originalData = bytearray(file.read())
        else:
            self._originalData = load_resource(f':/scene_data/{scene_id:02d}.bin')

    @property
    def landformsData(self)->List[int]:
        return list(unpack_from(f'{22*21}B', self._originalData, 0))

    @property
    def terrainData(self)->List[int]:
        return [data & 0x0F for data in unpack_from(f'{22*20}B', self._originalData, 22 * 21)]

    @property
    def valueData(self)->List[int]:
        return [data >> 4 & 0x0F for data in unpack_from(f'{22*20}B', self._originalData, 22 * 21)]

    @property
    def positionData(self)->List[int]:
        return list(unpack_from(f'{22*20}B', self._originalData, 22 * (21 + 20)))

    def saveFile(self, filename: str):
        landforms_byte: bytearray = pack(f'{len(self.landformsData)}B', *self.landformsData)
        mid_data: List[int] = [value << 4 | terrain for value, terrain in zip(self.valueData, self.terrainData)]
        mid_byte: bytearray = pack(f'{len(self.terrainData)}B', *mid_data)
        position_byte: bytearray = pack(f'{len(self.positionData)}B', *self.positionData)
        data_byte: bytearray = landforms_byte + mid_byte + position_byte
        with open(filename, 'wb') as file:
            file.write(data_byte)
        return bytearray(data_byte)
