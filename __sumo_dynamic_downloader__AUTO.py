from bs4 import BeautifulSoup as bs
from selenium import webdriver as wd
from selenium.webdriver.support.ui import WebDriverWait as wdwait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import os

# ------------------------ constants ---------------------------------- #

URL = "https://www3.nhk.or.jp/nhkworld/en/tv/sumo/"
URL_prefix = "https://www3.nhk.or.jp"
DOWNLOAD_LIST_FILENAME = "zzz_toDownload.txt"
DELAY = 11 # seconds
m3u8_prefix = "https://eqj833muwr.eq.webcdn.stream.ne.jp/www50/eqj833muwr/jmc_pub/jmc_pd/"
m3u8_suffix = "_22.m3u8"
m3u8_prefix_alt = "https://vod-stream.nhk.jp"
m3u8_suffix_alt = "/index_640x360_836k.m3u8"


# ------------------------ functions ---------------------------------- #

def get_chrome_options(webdriver):
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument("--disable-extensions")
	chrome_options.add_argument("--disable-gpu")
	chrome_options.add_argument("--headless=new")
	chrome_options.add_argument("--headless")
	chrome_options.headless = True
	return chrome_options
	
	
def get_m3u8_url(page_url):
	driver = wd.Chrome(options=get_chrome_options(wd))
	driver.get(page_url)
	try:
		myElem = wdwait(driver, DELAY).until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
	except TimeoutException:
		print(end="")
	soup = bs(driver.page_source,'html.parser')
	vid_div = soup.find("div",{"id":"p-bout__vod"})
	iframe = vid_div.find("iframe")
	next_url= URL_prefix + iframe.attrs.get("src")
	driver.get(next_url)
	try:
		myElem = wdwait(driver, DELAY).until(EC.presence_of_element_located((By.CLASS_NAME, "jsp-video-cover controller")))
	except TimeoutException:
		print(end="")
	soup = bs(driver.page_source,'html.parser')
	driver.quit()
	url_elm = soup.find("div",{"class":"jsp-video-cover controller"})
	url = url_elm.attrs.get("style")
	v1 = url[url.find("thumbnail")+10:url.rfind("/")]
	v2 = url[url.rfind("/"):url.rfind("_")]
	v2 = v2[:v2.rfind("_")]
	m3u8_url = m3u8_prefix + v1 + v2 + v2 + m3u8_suffix
	return m3u8_url

def get_m3u8_url_alt(page_url):
	driver = wd.Chrome(options=get_chrome_options(wd))
	driver.get(page_url)
	try:
		myElem = wdwait(driver, DELAY).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
	except TimeoutException:
		print(end="")
	soup = bs(driver.page_source,'html.parser')
	vid_div = soup.find("div",{"id":"p-bout__video"})
	img = vid_div.find("img")
	url = img.attrs.get("src")
	driver.quit()
	v = url.replace("images","movies").replace("_v_","_").replace(".jpg","")
	m3u8_url = m3u8_prefix_alt + v + m3u8_suffix_alt
	return m3u8_url

def updateDownloadTxtFile():
	updated_list = []
	txtFile = open(DOWNLOAD_LIST_FILENAME,'r')
	lines = txtFile.readlines()
	for line in lines:
		if line=='\n':
			updated_list.append(line);
		elif not os.path.isfile(line.replace("\n",".mp4")):
			updated_list.append(line);
	txtFile.close()
	txtFile = open(DOWNLOAD_LIST_FILENAME,'w')
	txtFile.writelines(updated_list)
	txtFile.close()

def runAutoListGen():
	os.system('__\\__auto-grab.py')
	
# ------------------------------------------------------------------------------------------------- #


# ------------------- PART 0: download-list auto generation , if first-time-run  ------------------ #

os.system("title SUMO DYNAMIC DOWNLOADER -- AUTO ")

if not os.path.isfile(DOWNLOAD_LIST_FILENAME):
	print("\n\n\t running for the FIRST time !!! \n\n")
	print("\tAuto-Generating download list from NHK-Grand-Sumo-Highlights website ... ")
	os.system("timeout /T 11")
	runAutoListGen()

os.system("cls")


# ------------------- PART 1: getting items list from main website into a dictionary data-type ------------------ #

print("\n > checking what is available online to download !")

print("\n > getting request from: " + URL + " ...")


driver = wd.Chrome(options=get_chrome_options(wd))

driver.get(URL)

soup = bs(driver.page_source,'html.parser')

driver.quit()

list = soup.find("div",{"id":"p-topTournament__list"})
titles_list = list.find_all(class_="c-day")
urls_list = list.find_all(class_="c-item__link")

titles = []
urls = []

for title in titles_list:
	titles.append(title.contents[0].upper())
	
for url in urls_list:
	urls.append(url.attrs.get("href"))


data_dic = {}

for i in range(len(titles)):
	data_dic[titles[i]] = urls[i]

data_dic = dict(reversed(data_dic.items()))


# adding summary video m3u8 url to data_dic , if exists
# notice that it already is an .m3u8 url , so less processing further on !
summary_div = soup.find("div",{"id":"p-bout__video"})
summary_img = summary_div.find("img")
img_url = summary_img.attrs.get("src")
if img_url.find("day")==-1:
	if img_url.find("high")>0 or img_url.find("hlts")>0 or img_url.find("hgts")>0:
		url = img_url.replace("images","movies").replace(".jpg","")
		data_dic["summary"] =  m3u8_prefix_alt + url + m3u8_suffix_alt


# ------------------- PART 2: comparing what is available currently online (data_dic) with local items list toDownload ! (i.e. what remains to get) ------------------ #

print("\n > comparing what is available with what is required to update/download ! ")

current_list = []
txtFile = open(DOWNLOAD_LIST_FILENAME,'r')
Lines = txtFile.readlines()
for line in Lines:
	if line != '\n':
		current_list.append(line.replace("\n",""))
txtFile.close()
if current_list==[]:
	print("\n\n\t","DONE downloading for this month, \n\n\t deleting \""+DOWNLOAD_LIST_FILENAME+"\" ... \n\n\t See you in the next basho !!! \n\n")
	os.system("del " + DOWNLOAD_LIST_FILENAME)
	os.system("timeout /T 11")
	exit()


items_to_get = {}

for item in current_list:
	if item[:2]=="00":
		if item.find("PREVIEW")>-1:
			for k,v in data_dic.items():
				if k.find("PREVIEW")>-1:
					items_to_get[item]=URL_prefix+v
		else:
			for k,v in data_dic.items():
				if k.find(item[3:])>-1:
					items_to_get[item]=URL_prefix+v
	elif item[:4]=="LIVE":
		for k,v in data_dic.items():
			if k.find("LIVE")>-1:
				if k.find(item[5:7])>-1:     # finds LIVE for days 14 & 15 => 2 chars
					items_to_get[item]=URL_prefix+v
				elif k.find(item[6:7])>-1:	# finds LIVE for days 1 & 8 => 1 char
					if int(item[6:7])==1 and (k.find("DAY 14")>-1 or k.find("DAY 15")>-1): # special case !
						break
					else:
						items_to_get[item]=URL_prefix+v
	elif item.find("summary")>-1:
		for k,v in data_dic.items():
			if k.find("summary")>-1:
				items_to_get[item] = v
	else:
		day_num = int(item[0:2])
		for k in sorted(data_dic.keys()):
			if k.find("LIVE")==-1:
				if k.find("DAY "+str(day_num))>-1:
					if day_num==1:  # special case !
						only_one=True
						for i in range(0,6):
							if k.find("DAY 1"+str(i))>-1:
								only_one=False
								break
						if only_one:
							items_to_get[item]=URL_prefix+data_dic[k]
					else:
						items_to_get[item]=URL_prefix+data_dic[k]


if not items_to_get:
	print("\n\n\t ALL is UPDATED ... nothing will be downloaded at the moment ... goodbye ! \n")
	os.system("timeout /T 11")
	exit()

print("\n > The following items will be downloaded:- \n")
for k in (items_to_get.keys()):
	print("\t\t",k)

print("\n")

# ------------------- PART 3: going over items_to_get "page-urls" and getting an "m3u8" url for each one  ------------------ #


print("\n > grabbing .m3u8 urls for videos ... it will take about ~ ",DELAY*2+8," seconds / per url ... be patient !")

for k,v in items_to_get.items():
	if k.find("summary")>-1:
		continue  # skip this iteration , as "v" is already an .m3u8 url !
	if k[:2]=="00":
		if k=="00__PREVIEW":
			items_to_get[k]=get_m3u8_url(items_to_get[k])
		else:
			items_to_get[k]=get_m3u8_url_alt(items_to_get[k])
	else:
		items_to_get[k]=get_m3u8_url(items_to_get[k])


print("\n\n > done grabbing required .m3u8 urls ... download will start in ...")
os.system("timeout /T 11")

# ------------------- PART 4: downloading and updating _urls.txt along the way  ------------------ #

os.system("cls")

print("\n\n > items to be downloaded:-\n")
for k,v in items_to_get.items():
	print(" + ",k,":  "+v)

print("\n\n"," - "*(11),"\n\n")
print("Downloading ...\n")


for k,v in items_to_get.items():
	print("\n + ",k,":")
	if k.find("00")==0 or k.find("summary")==0:
		os.system("yt-dlp \"" + v + "\" -o \"" + k + ".mp4\" --quiet --no-warnings --progress")
	else:
		os.system("ffmpeg -v quiet -hide_banner -stats -i \"" + v + "\" -c copy -bsf:a aac_adtstoasc \"" + k + ".mp4\"")
	if k.find("LIVE_01")==0 or k.find("LIVE_08")==0 or k.find("summary")==0:
		os.system("echo:>> \"_urls.txt\"")
	os.system("echo " + k + ":  " + v + ">> \"_urls.txt\"")


print("\n\n"," - "*(11),"\n\n")

updateDownloadTxtFile()
os.system("pause")
