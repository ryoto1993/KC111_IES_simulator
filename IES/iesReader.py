# coding: UTF-8

import csv
import math


class IESreader:
    # IESファイルのパス
    iesFile = "IES/91820fb_5700k.ies"
    # 照明座標ファイルのパス
    lightFile = "IES/ies_light_downlight.csv"
    # 照度センサファイルのパス
    sensorFile = "IES/ies_sensor_12island.csv"
    # 影響度ファイル
    coefficientFile = "IES/coefficient.csv"
    # データ部分で光束が記載されている行
    iesLumen = 2
    # データ部分でアングルが記載されている行
    iesAngleLine = 10
    # データ部分で光度が記載されている行
    iesDataLine = 12
    # 照明から机上面までの距離
    height = 1960.0

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
        self.flux = 0

        self.read_ies()
        self.make_coefficient()

    def read_ies(self):
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
                self.date = lines[i][6:]
            elif lines[i].find("[LUMCAT]") > -1:
                self.lumcat = lines[i][8:]
            elif lines[i].find("[LAMP]") > -1:
                self.lamp = lines[i][6:]
            elif lines[i].find("[LAMPCAT]") > -1:
                self.lampcat = lines[i][8:]
            elif lines[i].find("[LUMINAIRE]") > -1:
                self.luminaire = lines[i][11:]
            elif lines[i].find("TILT") > -1:
                self.tilt = lines[i][4:]
            else:
                start_line = i-1
                break
            i += 1

        # ヘッダ以降のデータを読み込む
        self.angles = lines[start_line + IESreader.iesAngleLine][:-1].split(' ')
        self.data = lines[start_line + IESreader.iesDataLine][:-1].split(' ')
        self.flux = float(lines[start_line + IESreader.iesLumen])

        f.close()

    # 距離から影響度を算出するメソッド
    def solve_coefficient(self, dist):
        # 直下1mの照度=光度を計算
        luminance = float(self.data[0]) * self.flux / 1000

        # 測光点の水平面照度を計算
        rdegree = math.atan(float(dist) / float(IESreader.height))
        degree = math.degrees(rdegree)
        degree_index = int(degree / 5)
        floor = (degree_index + 1) * 5
        sub = float(degree - floor)
        raw = float(self.data[degree_index]) + float(sub / 5.0) * (float(self.data[degree_index + 1]) - float(self.data[degree_index]))
        illuminance = raw * self.flux / 1000 / ((dist/1000)**2 + (IESreader.height/1000)**2) * math.cos(rdegree)

        # 照度/光度影響度を計算
        return illuminance/luminance

    def make_coefficient(self):
        f = open(IESreader.coefficientFile, 'w')
        writer = csv.writer(f, lineterminator='\n')

        lights = [[int(elm) for elm in v] for v in csv.reader(open(IESreader.lightFile, "r"))]
        sensors = [[int(elm) for elm in v] for v in csv.reader(open(IESreader.sensorFile, "r"))]

        # ライト読み込みとヘッダ記述
        tmp = [""]
        for i in range(0, len(lights)):
            tmp.append("Light" + str(i+1))
        writer.writerow(tmp)

        # センサ読み込みと影響度計算
        for i, s in enumerate(sensors):
            tmp.clear()
            tmp.append("Sensor" + str(i+1))
            for l in lights:
                tmp.append(str(self.solve_coefficient(self.dist(s, l))))
            writer.writerow(tmp)
        f.close()

    def dist(self, p1, p2):
        p1x = float(p1[0])
        p1y = float(p1[1])
        p2x = float(p2[0])
        p2y = float(p2[1])

        d = (p1x-p2x)**2 + (p1y-p2y)**2
        dist = math.sqrt(d)

        return dist
