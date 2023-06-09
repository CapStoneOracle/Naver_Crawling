import pandas as pd # 표 형식의 데이터를 다룰 수 있는 pandas를 pd라고 줄여서 불러옵니다
from selenium import webdriver # 크롬 창을 조종하기 위한 모듈입니다
from selenium.webdriver.common.by import By # 웹사이트의 구성요소를 선택하기 위해 By 모듈을 불려옵니다
from selenium.webdriver.support.ui import WebDriverWait # 웹페이지가 전부 로드될때까지 기다리는 (Explicitly wait) 기능을 하는 모듈입니다
from webdriver_manager.chrome import ChromeDriverManager # 크롬에서 크롤링을 하기 위해, 웹 드라이버를 설치하는 모듈입니다
from selenium.webdriver.support import expected_conditions as EC # 크롬의 어떤 부분의 상태를 확인하는 모듈입니다
import time # 정해진 시간만큼 기다리게 하기 위한 패키지입니다
from selenium.webdriver.chrome.options import Options # 크롬 옵션
from selenium.webdriver.common.keys import Keys #브라우저에 키입력 용
from selenium.webdriver.common.by import By #webdriver를 이용해 태그를 찾기 위함
from selenium.webdriver.support.ui import WebDriverWait #Explicitly wait을 위함
from selenium.webdriver.support import expected_conditions as EC #브라우저에 특정 요소 상태 확인을 위해
import requests # bs 이용해서 필요한 정보 가져오기 위함
from bs4 import BeautifulSoup #브라우저 태그를 가져오고 파싱하기 위함
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException,TimeoutException #예외처리를 위한 예외들 


filename = 'C:\\Users\\ghkdd\\Desktop\\Python\\excel\\노원구음식점_가공.csv'
df = pd.read_csv(filename, encoding='cp949')

keyword = []
adress = []
keyword = df.get('사업장명')
adress = df.get('도로명주소').str.split(' ').str[0:4]


# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)


driver = webdriver.Chrome(options=chrome_options)

# 웹페이지 해당 주소 이동
driver.get("https://map.naver.com/v5/")

try:
   element = WebDriverWait(driver, 10).until(
       EC.presence_of_element_located((By.CLASS_NAME, "input_search"))
   ) #입력창이 뜰 때까지 대기
finally:
   pass

for i in range(len(keyword)):
    search_box = driver.find_element(By.CLASS_NAME,"input_search")
    if("노원" in str(keyword[i]) or "점" in str(keyword[i])): 
       search_box.send_keys(str(keyword[i]))
    else: 
       search_box.send_keys("노원 "+ str(keyword[i])+","+str(adress[i]).replace('[', '').replace(']', '').replace(',','').replace('\'',''))
        
    search_box.send_keys(Keys.ENTER)
    time.sleep(2)
    
    driver.switch_to.frame("searchIframe")
       
    try:          
      driver.find_element(By.XPATH, f'//*[@id="_pcmap_list_scroll_container"]/ul/li[1]/div[1]/div[2]/a[1]/div/div/span[1]').click()
      time.sleep(3)
      driver.find_element(By.XPATH, f'//*[@id="container"]/shrinkable-layout/div/app-base/search-layout/div[2]/entry-layout/entry-place-bridge/div')
      driver.find_element(By.XPATH, f'//*[@id="app-root"]/div/div/div/div[5]/div/div/div/div/a[3]/span').click()
      time.sleep(10)
    except NoSuchElementException as e:
       driver.switch_to.default_content()
   
       
    
    driver.find_element(By.CLASS_NAME,"button_clear").send_keys(Keys.ENTER)
    
   #  str(adress[i]).replace('[', '').replace(']', '').replace(',','').replace('\'','')
    

