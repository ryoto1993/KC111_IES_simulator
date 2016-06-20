# coding: utf-8

from ANA_RC.anarc import *
from ANA_DB.anadb import *

if __name__ == "__main__":
    print("IESファイルを用いたシミュレーション ver.0.3")
    print("最適化アルゴリズム：ANA/DB")

    Initial.set()

    ana = AnaDb()

    ana.start()
