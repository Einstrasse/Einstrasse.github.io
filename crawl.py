# -*- coding: utf-8 -*-
import requests
from urllib import parse
import json

regions = {
    '서울특별시': "서울",
    '경기도': "경기",
    '부산광역시': "부산",
    '대구광역시': "대구",
    '인천광역시': "인천",
    '대전광역시': "대전",
    '울산광역시': "울산",
    '강원도': "강원",
    '충청북도': "충북",
    '충청남도': "충남",
    '광주광역시': "광주",
    '전라북도': "전북",
    '전라남도': "전남",
    '경상북도': "경북",
    '경상남도': "경남",
    '제주특별자치도': "제주"
}
def getGu(region):
    url = "https://www.dhlottery.co.kr/store.do?method=searchGUGUN"
    resp = requests.post(url, data={"SIDO": parse.quote(region)})
    return resp.json()
def getData(shortRegion, gu):
    print (f"Fetching {shortRegion} - {gu}")
    url = "https://www.dhlottery.co.kr/store.do?method=sellerInfoPrintResult"
    data = {
        "searchType": "3",
        "sltSIDO2": parse.quote(shortRegion),
        "sltGUGUN2": parse.quote(gu),
        "corpYn": "Y"
        }
    resp = requests.post(url, data=data)
    result = resp.json()["arr"]
    def process(item):
        fieldNames = [
            "BPLCLOCPLC1", 
            "BPLCLOCPLC2", 
            "BPLCLOCPLC3", 
            "BPLCLOCPLC4", 
            ]
        for field in fieldNames:
            if item[field] == None:
                item[field] = ""
        ret = {
            "pos": [float(item["ADDR_LAT"]), float(item["ADDR_LOT"])],
            "title": item["SHOP_NM"].replace("&&#35;40;", "(").replace("&&#35;41;", ")").replace("&#35;", "#").replace("&amp;", "&"),
            "addr": " ".join(map(lambda x : x.replace("&&#35;40;", "(").replace("&&#35;41;", ")"), [item["BPLCLOCPLC1"], item["BPLCLOCPLC2"], item["BPLCLOCPLC3"], item["BPLCLOCPLC4"]])),
            "speeto500": item["SPEETTO500_YN"],
            "speeto1000": item["SPEETTO1000_YN"],
            "speeto2000": item["SPEETTO2000_YN"],
            "annuity": item["ANNUITY_YN"]
        }
        return ret
    
    return list(map(process, result))

result = []
for region in regions.keys():
    shortRegion = regions[region]
    gus = getGu(region)
    for gu in gus:
        result += getData(shortRegion, gu)
# print (result)
with open("lottory-map.json", "wt") as f:
    f.write(json.dumps(result))

#html entity unescape required.