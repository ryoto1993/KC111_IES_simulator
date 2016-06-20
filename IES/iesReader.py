# coding: UTF-8

import csv

class IESreader:
    # IESファイルのパス
    iesFile = ""

    def __init__(self):
        self.manufac = ""
        self.test = ""
        self.date = ""
        self.lumcat = ""
        self.lamp = ""
        self.lampcat = ""
        self.luminaire = ""

    def readCSV(self):
        f = open(IESreader.iesFile, 'r')
        reader = csv.reader(f)
        next(reader)  # ヘッダを読み飛ばす

        

        # 装置の準備
        for var in range(0, Initial.light):
            Initial.lightList.append(Light())

        for var in range(0, Initial.sensor):
            Initial.sensorList.append(Sensor())
            Initial.sensorList[var].set_influence(next(reader))