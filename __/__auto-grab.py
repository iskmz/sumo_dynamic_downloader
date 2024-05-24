from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
from selenium import webdriver as wd
import os

URL = "https://www3.nhk.or.jp/nhkworld/en/tv/sumo/"
out_List = []

print("\n\n"+"getting request from: "+URL+" ...")

chrome_options = wd.ChromeOptions()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--headless")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.headless = True
driver = wd.Chrome(options=chrome_options)

driver.get(URL)

soup = bs(driver.page_source,'html.parser')

driver.quit()

print("\n"+"analyzing page and generating output data ...\n")
strMonthDay = soup.find_all(class_="p-hero__date")[0].contents[0]
firstSpace = strMonthDay.index(" ")
monthName=strMonthDay[:firstSpace]
startDay=strMonthDay[firstSpace+1:strMonthDay.index("-")]
year = str(dt.now().year)
months = {"January":"01","March":"03","May":"05","July":"07","September":"09","November":"11"}
out_List += year+"\n"
out_List += months[monthName]+"\n"
out_List += startDay+"\n"
titles_list = soup.find_all(class_="c-day")
rikishi_list = []
for title in titles_list:
	ttt = title.contents[0].upper()
	if ttt.find("DAY")==-1 and ttt.find("PREVIEW")==-1:
		rikishi_list.append(ttt)
	
rikishi_list.reverse()
rikishiNum = str(len(rikishi_list))
out_List += rikishiNum+"\n"
for rikishi in rikishi_list:
	out_List += rikishi+"\n"

txtFile = open("__tmp__.txt",'w')
txtFile.writelines(out_List)
txtFile.close()

os.system("__\__sumo-gen-download-list.bat<__tmp__.txt") ## using __\__ ... because it is run from root folder !
os.system("del __tmp__.txt")