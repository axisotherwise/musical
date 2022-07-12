import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By

import requests
from bs4 import BeautifulSoup
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



for i in range(1,5):

    b = driver.find_element("xpath", f'//*[@id="search_listType01"]/ul/li[{i}]/div/div[1]/a/img').click()
        #1번째 이미지 클릭
    time.sleep(3)

    c = driver.find_element("xpath", '//*[@id="su_con"]/div[2]/div[2]/ul/li[6]/div/dl')
        # //*[@id="su_con"]/div[2]/div[2]/ul/li[6]/div/dl << 출연진 위치 xpeke 고정임
    d = driver.find_element("xpath", '//*[@id="su_con"]/div[2]/div[2]/ul/li[7]/div/dl')
    e= c.text
    f= d.text

    print(e)
    print(f)

    driver.back()
    time.sleep(3)





#su_con > div.bxo_vbk > div.zi > ul > li:nth-child(6) > div > dl
#su_con > div.bxo_vbk > div.zi > ul > li:nth-child(7) > div > dl












