# coding: UTF-8

import csv

class IESreader:
    # IESファイルのパス
    iesFile = "IES/profile.ies"
    # データ部分でアングルが記載されている行
    iesAngleLine = 14
    # データ部分で光度が記載されている行
    iesDataLine = 16

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

        print(self.angles)
        print(self.data)