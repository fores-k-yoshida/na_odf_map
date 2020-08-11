import xml.etree.ElementTree as ET
import bisect
import datetime
import pytz
import sys
import json
from dateutil import parser
import glob
import codecs

#kmlファイル読み込み関数
def parse_kml(file_name):
    tree = ET.parse(file_name)
    return tree

#ファイル読み込み
files = glob.glob("./input/*")
for file in files:
    INPUT_FILENAME = file
    PrefectureName = INPUT_FILENAME.split('.kml')[0].split('./input\\')[1]
    print(PrefectureName + "実行中")
    OUTPUT_FILENAME= PrefectureName + '.json'

    #市区町村がいくつあるか数える
    citycount = 0

    #kmlファイル読み込み
    tree = parse_kml(INPUT_FILENAME)
    root = tree.getroot()

    #緯度経度リスト化
    cityslist = []
    for i in root.iter('{http://www.opengis.net/kml/2.2}coordinates'):
        trees = i.text
        cityslist.append(trees)

    #市ごとの緯度経度のリスト（['11,22','33,44'...],[],[]..）
    city = []
    #jaon形式のリスト[{'latitude': '12', 'longitude': '38'}, {'latitude': '137.1926780,,,}]
    position = []
    #市ごとに分割（['11,22 33,44 55,66 ..','','',,,]）
    for citys in cityslist:
        #市の緯度経度をセットでリスト化
        citysSP = citys.split()
        #（['11,22','33,44'...]）
        for i in citysSP:
            onecity = [x.strip() for x in i.split(',')]
            citymap = {'latitude':onecity[1], 'longitude':onecity[0]}
            city.append(citymap)
        position.append(city)
        city = []

    #シンプルデータ取り出し
    simple = []
    for a in root.iter("{http://www.opengis.net/kml/2.2}SchemaData"):
        #for文が回った階数をカウント
        citycount += 1
        simple1 = []
        aa = a.findall("{http://www.opengis.net/kml/2.2}SimpleData")
        #SchemaDataの中からSimpleDataを取り出す(最初と最後を除く)
        for b in aa[1:len(aa) - 1]:
            simple1.append(b.text)
        sin = {'name':simple1}
        simple.append(sin)

    #最終のjson形式に変換
    jsonlist = []
    counta = 0
    jsonlist.append(PrefectureName)
    for n in range(citycount):
        counta += 1
        kanseimap = {'num':counta, 'city':simple[n],'position':position[n]}
        jsonlist.append(kanseimap)

    #書き込み処理
    with open('./output/' + OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
        json.dump(jsonlist, f, ensure_ascii=False, indent=4)

print("finish!!")
sys.exit()
