import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.lpapihe.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

# //*[@id="search_listType01"]/ul/li[1]/div/div[1]/a/img
# //*[@id="search_listType01"]/ul/li[2]/div/div[1]/a/img
# //*[@id="search_listType01"]/ul/li[3]/div/div[1]/a/img

# 코딩 시작


driver = webdriver.Chrome('./chromedriver')

url = "https://kopis.or.kr/por/db/pblprfr/pblprfr.do?menuId=MNU_00020&searchType=total&searchWord="
driver.get(url)
# kopis열기

#su_con > div.bxo_vbk > div.zi
time.sleep(5)

a = driver.find_element("xpath", '//*[@id="su_con"]/div[2]/ul/li[3]/p/a').click()
# 뮤지컬창 클릭
time.sleep(3)



for i in range(2,30):

    b = driver.find_element("xpath", f'//*[@id="search_listType01"]/ul/li[{i}]/div/div[1]/a/img').click()
        #1번째 이미지 클릭
    time.sleep(4)

    c = driver.find_element("xpath", '//*[@id="su_con"]/div[2]/div[2]/ul/li[6]/div/dl')
        # //*[@id="su_con"]/div[2]/div[2]/ul/li[6]/div/dl << 출연진 위치 xpeke 고정임
    d = driver.find_element("xpath", '//*[@id="su_con"]/div[2]/div[2]/ul/li[7]/div/dl')
    e = driver.find_element("xpath", '//*[@id="su_con"]/div[1]/div[1]/h4')
    actor= c.text
    maker= d.text
    title= e.text

    driver.back()
    time.sleep(4)

    doc = {
        "출연진": actor,
        "제작진": maker,
        "title":title
        }
    db.musical_detail.insert_one(doc)





#su_con > div.bxo_vbk > div.zi > ul > li:nth-child(6) > div > dl
#su_con > div.bxo_vbk > div.zi > ul > li:nth-child(7) > div > dl


#
# //*[@id="su_con"]/div[1]/div[1]/h4








