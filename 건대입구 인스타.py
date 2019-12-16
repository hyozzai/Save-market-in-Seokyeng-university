from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
import urllib.parse
from urllib.request import Request, urlopen
from time import sleep
import pandas as pd



search = input("검색어를 입력하세요 : " )
search = urllib.parse.quote(search)
url = 'https://www.instagram.com/explore/tags/'+str(search)+'/'
driver = webdriver.Chrome('C:/Users/효짜이/AppData/Local/Programs/Python/Python37-32/WebDriver/chromedriver.exe')

driver.get(url) 
sleep(5)


SCROLL_PAUSE_TIME = 1.0
reallink = []

while True:
    pageString = driver.page_source
    bsObj = BeautifulSoup(pageString, "lxml")

    for link1 in bsObj.find_all(name="div",attrs={"class":"Nnq7C weEfm"}):
        title = link1.select('a')[0] 
        real = title.attrs['href']
        reallink.append(real) 
        title = link1.select('a')[1] 
        real = title.attrs['href']
        reallink.append(real) 
        title = link1.select('a')[2] 
        real = title.attrs['href']
        reallink.append(real) 

    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
            
        else:
            last_height = new_height
            continue


csvtext = []

reallinknum = len(reallink)
print("총"+str(reallinknum)+"개의 데이터.")
try:
    for i in range(0,reallinknum):
        csvtext.append([])
        req = Request('https://www.instagram.com/p'+reallink[i],headers={'User-Agent': 'Mozilla/5.0'})

        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage,"lxml",from_encoding='utf-8')
        soup1 = soup.find("meta",attrs={"property":"og:description"})
        
        reallink1 = soup1['content']
        reallink1 = reallink1[reallink1.find("@")+1:reallink1.find(")")]
        reallink1 = reallink1[:20]
        if reallink1 == '':
            reallink1 = 'Null'
        csvtext[i].append(reallink1)
        
        for reallink2 in soup.find_all("meta",attrs={"property":"instapp:hashtags"}): 
            reallink2 = reallink2['content']
            csvtext[i].append(reallink2)
 
    
        print(str(i+1)+"개의 데이터 받아오는 중.")
        print(csvtext)
        data = pd.DataFrame(csvtext)
        data.to_csv('insta.txt', encoding='utf-8')  
                           
except:
    print("오류발생"+str(i+1)+"개의 데이터를 저장합니다.")   
    
    data = pd.DataFrame(csvtext)
    data.to_csv('건대입구.txt', encoding='utf-8')  
print("저장성공")   
