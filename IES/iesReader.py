# coding: UTF-8

import csv
import math


class IESreader:
    # IESファイルのパス
    iesFile = "IES/profile.ies"
    # 照明座標ファイルのパス
    lightFile = "IES/ies_light.csv"
    # 照度センサファイルのパス
    sensorFile = "IES/ies_sensor.csv"
    # 影響度ファイル
    coefficientFile = "IES/coefficient.csv"
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
        self.make_coefficient()

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

        f.close()

    # 距離から影響度を算出するメソッド
    def solve_coefficient(self, dist):
        height = IESreader.height
        degree = math.degrees(math.atan(dist / height))
        degree_index = int(degree/5)

        floor = degree_index * 5
        sub = float(degree - floor)

        lum = float(self.data[degree_index]) + (float(self.data[degree_index+1]) - float(self.data[degree_index]))*sub

        return lum/((self.height/1000)**2 + (dist/1000)**2) / float(self.data[0])


    def make_coefficient(self):
        f = open(IESreader.coefficientFile, 'w')
        writer = csv.writer(f, lineterminator='\n')

        lights = [[int(elm) for elm in v] for v in csv.reader(open(IESreader.lightFile, "r"))]
        sensors = [[int(elm) for elm in v] for v in csv.reader(open(IESreader.sensorFile, "r"))]

        # ライト読み込みとヘッダ記述
        tmp = ["Light"]
        for i in range(0, len(lights)):
            tmp.append("Light" + str(i+1))
        writer.writerow(tmp)

        # センサ読み込みと影響度計算
        for i, s in enumerate(sensors):
            tmp.clear()
            tmp.append("Sensor" + str(i+1))
            for l in lights:
                tmp.append(self.solve_coefficient(self.dist(s, l)))
            writer.writerow(tmp)





        f.close()

    def dist(self, p1, p2):
        p1x = float(p1[0])
        p1y = float(p1[1])
        p2x = float(p2[0])
        p2y = float(p2[1])

        return math.sqrt((p1x-p2x)**2 + (p1y-p2y)**2)
