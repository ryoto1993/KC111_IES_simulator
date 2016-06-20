# coding: UTF-8

import csv
import math

class IESreader:
    # IESファイルのパス
    iesFile = "IES/profile.ies"
    # データ部分で光束が記載されている行
    iesLumen = 2
    # データ部分でアングルが記載されている行
    iesAngleLine = 14
    # データ部分で光度が記載されている行
    iesDataLine = 16
    # 照明から机上面までの距離
    height = 1985

    def __init__(self):
        self.profile = ""
        self.manufac = ""
        self.test = ""
        self.date = ""
        self.lumcat = ""
        self.lamp = ""
        self.lampcat = ""
        self.luminaire = ""
        self.tilt = ""
        self.angles = []
        self.data = []
        self.lumen = 0

        self.readCSV()

    def readCSV(self):
        # ヘッダ以降のデータが始まる行
        start_line = 0

        f = open(IESreader.iesFile, 'r')
        lines = f.readlines()

        self.profile = lines[0][6:]

        print(self.profile)

        # ヘッダ部分を読み込む

        i = 1
        while True:
            if lines[i].find("[MANUFAC]") > -1:
                self.manufac = lines[i][9:]
            elif lines[i].find("[TEST]") > -1:
                self.test = lines[i][6:]
            elif lines[i].find("[DATE]") > -1:
                self.test = lines[i][6:]
            elif lines[i].find("[LUMCAT]") > -1:
                self.test = lines[i][8:]
            elif lines[i].find("[LAMP]") > -1:
                self.test = lines[i][6:]
            elif lines[i].find("[LAMPCAT]") > -1:
                self.test = lines[i][8:]
            elif lines[i].find("[LUMINAIRE]") > -1:
                self.test = lines[i][11:]
            elif lines[i].find("TILT") > -1:
                self.test = lines[i][4:]
            else:
                start_line = i-1
                break
            i += 1

        # ヘッダ以降のデータを読み込む
        self.angles = lines[start_line + IESreader.iesAngleLine][:-1].split(' ')
        self.data = lines[start_line + IESreader.iesDataLine][:-1].split(' ')
        self.lumen = lines[start_line + IESreader.iesLumen]

        print(self.angles)
        print(self.data)

    # 距離から影響度を算出するメソッド
    def solve_coefficient(self, dist):
        height = IESreader.height
        degree = math.degrees(math.atan(height / dist))
        degree_index = int(degree/5)
        print(degree)
        print(degree_index)

        floor = degree_index * 5
        sub = float(degree - floor)

        lum = float(self.data[degree_index]) + (float(self.data[degree_index+1]) - float(self.data[degree_index]))*sub
        print(lum)
        lum *= float(self.lumen)/1000

        print(lum)
