from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By



driver = webdriver.Chrome('./chromedriver')  # 드라이버를 실행합니다.


url = "https://kopis.or.kr/por/db/pblprfr/pblprfr.do?menuId=MNU_00019&searchType=total&searchWord="


driver.get(url)  # 드라이버에 해당 url의 웹페이지를 띄웁니다.
sleep(3)  # 페이지가 로딩되는 동안 5초 간 기다립니다.
tag_name='tabaaab'
elements = driver.find_element(By.NAME, tag_name)
elements.click()
sleep(3)


req = driver.page_source  # html 정보를 가져옵니다.
driver.quit()  # 정보를 가져왔으므로 드라이버는 꺼줍니다.

# soup = BeautifulSoup(data.text, 'html.parser')
soup = BeautifulSoup(req, 'html.parser')  # 가져온 정보를 beautifulsoup으로 파싱해줍니다.



musicals = soup.select("#search_listType01 > ul > li")

print(musicals)

for musical in musicals:
    img = musical.select_one("div.tu > a > img")['src']
    title = musical.select_one("div.zi > h4 > a").text
    date = musical.select_one("div.zi > ul > li:nth-child(1)").text
    place = musical.select_one("div.zi > ul > li:nth-child(2)").text
    print("https://kopis.or.kr"+img)
    print(title)
    print(date)
    print(place)

#몽고디비 셋팅하시구 insert 하면 끝
