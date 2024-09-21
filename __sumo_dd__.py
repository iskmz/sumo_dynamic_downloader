from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
from selenium import webdriver as wd
from selenium.webdriver.support.ui import WebDriverWait as wdwait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import os
import sys
import keyboard
import threading

# ------------------------ constants ------------------------------------- #


URL = "https://www3.nhk.or.jp/nhkworld/en/tv/sumo/"
URL_prefix = "https://www3.nhk.or.jp"
DOWNLOAD_LIST_FILENAME = "zzz_toDownload.txt"
DELAY = 11 # seconds
m3u8_prefix = "https://eqj833muwr.eq.webcdn.stream.ne.jp/www50/eqj833muwr/jmc_pub/jmc_pd/"
m3u8_suffix = "_22.m3u8"  # 22=HD-quality(720p) # try 23 for higher # 19 or 21 for lower
m3u8_prefix_alt = "https://vod-stream.nhk.jp"
m3u8_suffix_alt = "/index_640x360_836k.m3u8"


# ------------------- functions (common for all sections) ---------------- #

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

def get_chrome_options(webdriver):
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument("--disable-extensions")
	chrome_options.add_argument("--disable-gpu")
	chrome_options.add_argument("--headless=new")
	chrome_options.add_argument("--headless")
	chrome_options.headless = True
	return chrome_options

def down_list_gen(year,month,start_day,rikishi_list):
	# year="YYYY", month="MM", start_day="DD" 
	# all are strings
	startDay = int(start_day)
	d_lst = []
	d_lst.append("00__PREVIEW"+"\n")
	for rikishi in rikishi_list:
		d_lst.append("00_" + rikishi + "\n")
	d_lst.append("\n")
	d_lst.append("LIVE_01_" + start_day + "_OpeningDay"+"\n")
	for i in range(1,8):
		d_lst.append("0"+str(i)+"_"+str(startDay+i-1)+"\n")
	d_lst.append("\n")
	d_lst.append("LIVE_08_" + str(startDay+7) + "_HalfwayPoint"+"\n")
	d_lst.append("08_"+str(startDay+7)+"\n")
	d_lst.append("09_"+str(startDay+8)+"\n")
	for i in range(10,16):
		d_lst.append(str(i)+"_"+str(startDay+i-1)+"\n")
	d_lst.append("LIVE_14_" + str(startDay+13) + "\n")
	d_lst.append("LIVE_15_" + str(startDay+14) + "_FinalDay"+"\n")
	d_lst.append("\n")
	d_lst.append("summary_" + year + "_" + month + "\n")
	# write d_lst to file
	txtFile = open(DOWNLOAD_LIST_FILENAME,'w')
	txtFile.writelines(d_lst)
	txtFile.close()
	print("\n\t DONE ! \n\n")

def auto_grab_py():
	# to replace the old "__auto-grab.py" script
	print("\n\n"+" > getting request from: "+URL+" ...")
	driver = wd.Chrome(options=get_chrome_options(wd))
	driver.get(URL)
	soup = bs(driver.page_source,'html.parser')
	driver.quit()
	print("\n"+" > analyzing page and generating output data ...\n")
	strMonthDay = soup.find_all(class_="p-hero__date")[0].contents[0]
	firstSpace = strMonthDay.index(" ")
	monthName=strMonthDay[:firstSpace]
	startDay=strMonthDay[firstSpace+1:strMonthDay.index("-")]
	year = str(dt.now().year)
	months = {"January":"01","March":"03","May":"05","July":"07","September":"09","November":"11"}
	titles_list = soup.find_all(class_="c-day")
	rikishi_list = []
	for title in titles_list:
		ttt = title.contents[0].upper()
		if ttt.find("DAY")==-1 and ttt.find("PREVIEW")==-1:
			rikishi_list.append(ttt)
	rikishi_list.reverse()
	print("\n"+" > generating download list ...\n")
	down_list_gen(year,months[monthName],startDay,rikishi_list)

def sumo_gen_download_list():
	# to replace the old "__sumo-gen-download-list.bat" script
	year = input("\n\n > Enter Tournament's Year (YYYY): ")
	month = input(" > Enter Tournament's Month (MM): ")
	start_d = input(" > Enter Tournament's starting day (DD): ")
	print()
	rikishi_num = int(input(" > Enter number of rikishi intro. videos: "))
	rikishi_list = []
	for i in range(rikishi_num):
		rikishi_list.append(input(" >>> name of rikishi #" + str(i+1) + ": "))
	down_list_gen(year,month,start_d,rikishi_list)


# ------------------- functions (only for AUTO section) ------------------ #


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


def get_available_items():
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
	# adding summary video m3u8 url to data_dic , IF EXISTS !!!
	# notice that it already is an .m3u8 url , so less processing further on !
	# updated: 2024-09-06 , bug fix, added try/except clause !
	try:
		summary_div = soup.find("div",{"id":"p-bout__video"})
		summary_img = summary_div.find("img")
		img_url = summary_img.attrs.get("src")
		if img_url.find("day")==-1:
			if img_url.find("high")>0 or img_url.find("hlts")>0 or img_url.find("hgts")>0:
				url = img_url.replace("images","movies").replace(".jpg","")
				data_dic["summary"] =  m3u8_prefix_alt + url + m3u8_suffix_alt
	except Exception as e:
		print()
	return data_dic


def compare_available_required(data_dic,current_list):
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
	return items_to_get


def auto_main():
	os.system("title SUMO DYNAMIC DOWNLOADER -- AUTO ")
	os.system("cls")
	#
	# - - - - - PART 0: download-list auto generation , if first-time-run
	#
	if not os.path.isfile(DOWNLOAD_LIST_FILENAME):
		print("\n\n\t running for the FIRST time !!! \n\n")
		print("\tAuto-Generating download list from NHK-Grand-Sumo-Highlights website ... ")
		os.system("timeout /T 11")
		auto_grab_py()
		os.system("timeout /T 11")
	os.system("cls")
	#
	# - - - - - PART 1: getting items list from main website into a dictionary data-type
	#
	print("\n > checking what is available online to download !")
	data_dic = get_available_items()
	#
	# - - - - - PART 2: comparing what is available currently online (data_dic) with local items list toDownload ! (i.e. what remains to get)
	#
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
	items_to_get = compare_available_required(data_dic,current_list)
	if not items_to_get:
		print("\n\n\t ALL is UPDATED ... nothing will be downloaded at the moment ... goodbye ! \n")
		os.system("timeout /T 11")
		exit()
	print("\n > The following items will be downloaded:- \n")
	for k in (items_to_get.keys()):
		print("\t\t",k)
	#
	# - - - - - PART 3: going over items_to_get "page-urls" and getting an "m3u8" url for each one
	#
	print("\n\n > grabbing .m3u8 urls for videos ... it will take about ~ ",DELAY*2+8," seconds / per url ... be patient !")
	for k,v in items_to_get.items():
		if k.find("summary")>-1:
			continue  # skip this iteration , as "v" is already an .m3u8 url !
		try:
			if k[:2]=="00":
				if k=="00__PREVIEW":
					items_to_get[k]=get_m3u8_url(items_to_get[k])
				else:
					items_to_get[k]=get_m3u8_url_alt(items_to_get[k])
			else:
				items_to_get[k]=get_m3u8_url(items_to_get[k])
		except Exception as e:
			print("UNKNOWN ERROR while grabbing .m3u8 url for: ",k)
			print("skipping this one !\n")
			items_to_get[k]="" # mark it for PART 4 !
	print("\n\n > done grabbing required .m3u8 urls ... download will start in ...")
	os.system("timeout /T 11")
	#
	# - - - - - PART 4: downloading and updating _urls.txt along the way
	#
	os.system("cls")
	print("\n\n > items to be downloaded:-\n")
	for k,v in items_to_get.items():
		if v=="":
			continue
		print(" + ",k,":  "+v)
	print("\n\n"," - "*(11),"\n\n")
	print("Downloading ...\n")
	for k,v in items_to_get.items():
		if v=="":
			continue
		print("\n + ",k,":")
		if k.find("00")==0 or k.find("summary")==0:
			os.system("yt-dlp \"" + v + "\" -o \"" + k + ".mp4\" --quiet --no-warnings --progress")
		else:
			os.system("ffmpeg -v quiet -hide_banner -stats -i \"" + v + "\" -c copy -bsf:a aac_adtstoasc \"" + k + ".mp4\"")
		if k.find("LIVE_01")==0 or k.find("LIVE_08")==0 or k.find("summary")==0:
			os.system("echo:>> \"_urls.txt\"")
		os.system("echo " + k + ":  " + v + ">> \"_urls.txt\"")
	print("\n\n"," - "*(11),"\n\n")
	# - - - - - PART 5: finishing touches ... - - - - - #
	updateDownloadTxtFile()
	print("\n\n\t DONE !!!\n\n")
	os.system("pause")


# ------------------- functions (only for BOTD section) ------------------ #

def leading_zero(num):
	if num<10:
		return "0"+str(num)
	else:
		return str(num)

def botd_main():
	os.system("title sumo -- BOUT OF THE DAY -- downloader")
	os.system("cls")
	destination_folder_name = "xtra__bout-of-the-day/"
	botd_url_prefix = "https://vod-stream.nhk.jp/nhkworld/en/tv/sumo/movies/day"
	botd_url_suffix = "/index_640x360_836k.m3u8"
	year = input("\n  Enter basho's year [YYYY]: ")
	month = input("\n  Enter basho's month [MM]: ")
	start_day = input("\n  Enter basho's starting day [DD]: ")
	year=year[2:]
	m3u8_urls_list = []
	filename_list = []
	for i in range (1,16):
		url_str = botd_url_prefix + str(i) + "_" + year + month + (leading_zero(int(start_day)+i)) + botd_url_suffix
		m3u8_urls_list.append(url_str)
		day_order = leading_zero(i)
		filename_list.append(day_order+"_"+(str(int(start_day)+i-1)))
	print("\n\n\t > Downloading bouts of the day ... \n")
	for filename,url in zip(filename_list,m3u8_urls_list):
		print("\n "+ filename +": ")
		os.system("yt-dlp \""+url+"\" -o \""+"/"+destination_folder_name+filename+".mp4\" --quiet --no-warnings --progress")
		os.system("echo " +filename+ ":  " +url+ ">> \""+destination_folder_name+"_urls.txt\"")
	print("\n\n\t DONE !!!\n\n")
	os.system("pause")

# ------------------- functions (only for MAIN section) ------------------ #

def runListGen():
	# REPLACED: "__sumo-gen-download-list.bat" script
	sumo_gen_download_list()
	os.system("pause")
	
def runAutoListGen():
	# REPLACED "__auto-grab.py" script
	auto_grab_py()
	os.system("pause")	

def runDownload():
	# REPLACED "__download-It_multi_quiet.bat" script
	os.system("cls")
	print()
	print(" - - - - - - - - -")
	print("  \"Just\"")
	print("  Download-It !")
	print(" - - - - - - - - -")
	print()
	amount = int(input(" > Enter amount of files to download: "))
	print()
	urls = []
	filenames = []
	for i in range(amount):
		print(" " + str(i+1) + ":")
		urls.append(input(" url: "))
		filenames.append(input(" filename: "))
		os.system("echo " + filenames[i] + ":  " + urls[i] + ">> \"_urls.txt\"")
	print("\n Downloading ...\n")
	for i in range(amount):
		print(" " + str(i+1) + ":")
		os.system("ffmpeg -v quiet -hide_banner -stats -i \""+urls[i]+"\" -c copy -bsf:a aac_adtstoasc \""+filenames[i]+".mp4\"")
	print("\n\n\t DONE ! \n\n")
	os.system("pause")
	exit()

def runDownload_ytdlp():
	# REPLACED "__download-It_multi_quiet__yt-dlp.bat" script
	os.system("cls")
	print()
	print(" - - - - - - - - -")
	print("  \"Just\"")
	print("  Download-It !")
	print(" - - - - - - - - -")
	print("  yt-dlp version")
	print(" - - - - - - - - -")
	print()
	amount = int(input(" > Enter amount of files to download: "))
	print()
	urls = []
	filenames = []
	for i in range(amount):
		print(" " + str(i+1) + ":")
		urls.append(input(" url: "))
		filenames.append(input(" filename: "))
		os.system("echo " + filenames[i] + ":  " + urls[i] + ">> \"_urls.txt\"")
	print("\n Downloading ...\n")
	for i in range(amount):
		print(" " + str(i+1) + ":")
		os.system("yt-dlp \"" + urls[i] + "\" -o \"" + filenames[i] +".mp4\"")
	print("\n\n\t DONE ! \n\n")
	os.system("pause")
	exit()
			

def getNameListFromFile():
	txtFile = open(DOWNLOAD_LIST_FILENAME,'r')
	Lines = txtFile.readlines()
	lst = []
	for line in Lines:
		if line != '\n':
			lst.append(line.replace("\n",""))
	txtFile.close()
	return lst

def showMenuFromList(lst):
	print("\n","  items remaining to download:- ","\n")
	for i,line in enumerate(lst,start=1):
		print("\t",i,end="")
		print(" " if i<10 else "",end="")
		print(". ",line)
	if lst==[]:
		print("\n\t","DONE downloading for this month, should delete \""+DOWNLOAD_LIST_FILENAME+"\" manually\n\n\t\t\t... and move on !\n")
	print("\t","- "*11)
	print("\t","x. RUN  \"__download-It_multi_quiet.bat\"")
	print("\t","y. RUN  \"__download-It_multi_quiet__yt-dlp.bat\"")
	print("\t","- "*11,"\n")
		
def InvalidInput(str,lstLen):
	if str=="x" or str=="X" or str=="y" or str=="Y":
		return False # valid input
	elif str.isdigit():
		num = int(str)
		if num >= 1 and num <= lstLen:
			return False # valid input 
	elif str.find("-")>0:
		i = str.find("-")
		min,max = str[:i],str[i+1:]
		if min.isdigit() and max.isdigit():
			mn,mx = int(min),int(max)
			if mn>=1 and mx>=1 and mn<=lstLen and mx<=lstLen and mx>=mn:
				return False # valid input
	return True # INVALID input
	
# assumes VALID input, as checked in function above
def analyzeInput(str):
	if str.isdigit():
		return int(str),-1,-1
	else:
		i = str.find("-")
		return -1,int(str[:i]),int(str[i+1:])


def main():
	# the OLD main section of the __sumo_dynamic_downloader__.py  script
	os.system("cls")
	if not os.path.isfile(DOWNLOAD_LIST_FILENAME):
		print("\n\n\t running for the FIRST time !!! \n\n")
		inputStr = input(" Auto-Generate download list from NHK-Grand-Sumo-Highlights website ?!?? [y/else]: ")
		os.system("cls")
		if inputStr=="y" or inputStr=="Y":
			runAutoListGen()
		else:
			runListGen()
	os.system("cls")
	remainingList = getNameListFromFile()
	showMenuFromList(remainingList)
	nameList = []
	urlList = []
	inputStr = input("\n  SELECT , from the list above, an item [#] , OR a range of items [min#-max#]: ")
	if InvalidInput(inputStr,len(remainingList)):
		print("INVALID input, try again!")
		os.system("pause")
		exit()
	if inputStr=="x" or inputStr=="X":
		runDownload()  # exits after
	if inputStr=="y" or inputStr=="Y":
		runDownload_ytdlp() # exits after 
	item,min,max = analyzeInput(inputStr)
	if item==-1: # a range was selected
		nameList = remainingList[min-1:max]
	else: # one item was selected
		nameList.append(remainingList[item-1])
	os.system("cls")
	print("\n\n  Enter urls for selected items:-\n")
	for i,itemName in enumerate(nameList):
		urlList.append(input("  "+str(i+1)+". "+itemName+":  "))
	print("\n\n"," - "*(11),"\n\n")
	print("Downloading ...\n")
	for i,item in enumerate(nameList):
		print("\n "+str(i+1)+". "+item+": ")
		if item.find("00")==0 or item.find("summary")==0:
			os.system("yt-dlp \""+urlList[i]+"\" -o \""+item+".mp4\" --quiet --no-warnings --progress")
		else:
			os.system("ffmpeg -v quiet -hide_banner -stats -i \""+urlList[i]+"\" -c copy -bsf:a aac_adtstoasc \""+item+".mp4\"")
		if item.find("LIVE_01")==0 or item.find("LIVE_08")==0 or item.find("summary")==0:
			os.system("echo:>> \"_urls.txt\"")
		os.system("echo " + item + ":  " + urlList[i] + ">> \"_urls.txt\"")
	print("\n\n"," - "*(11),"\n\n")
	updateDownloadTxtFile()
	os.system("pause")
	
	
# ------------------------------------------------------------------------ #


menu = ["AUTO Downloader","MAIN downloader","Bout of the Day","Quit"]
menu_selection = [auto_main,main,botd_main,exit] # function names, mapped to menu-items above 
max_menu_item_len = max([len(item) for item in menu])


selected = 0


space_factor = 16
top_b = "\u256d"+"\u2500"*(max_menu_item_len+space_factor*2)+"\u256e"
left_b = "\t\u2502"
right_b = "\u2502"
bottom_b = "\u2570"+"\u2500"*(max_menu_item_len+space_factor*2)+"\u256f"
space_item = " "*max_menu_item_len
select_sp_left = "\x1b[30;101m"+" "*space_factor	# 31: black foreground , 101: bright-red background
select_sp_right = " "*space_factor+"\x1b[0m"  	# 0: resets all colors
unselect_sp = " "*space_factor
def show_menu():
	global selected
	os.system("cls")
	print("\t"+top_b)
	for i in range(len(menu)):
		 x_space = max_menu_item_len-len(menu[i])
		 left_sp , right_sp = " "*(x_space//2) , " "*(x_space-x_space//2)
		 menu_item = left_sp+menu[i]+right_sp
		 left = select_sp_left if selected == i else unselect_sp
		 right = select_sp_right if selected == i else unselect_sp
		 print("{3}{0}{2}{1}{4}".format(left,right,space_item,left_b,right_b))
		 print("{3}{0}{2}{1}{4}".format(left,right,menu_item,left_b,right_b))
		 print("{3}{0}{2}{1}{4}".format(left,right,space_item,left_b,right_b))
	print("\t"+bottom_b)
	print(" * select an item using up/down/enter keys")

def up():
	global selected
	if selected==0:
		selected=len(menu)-1
	else:
		selected -= 1
	show_menu()

def down():
	global selected
	if selected==len(menu)-1:
		selected=0
	else:
		selected += 1
	show_menu()

def goto_selection():
	menu_selection[selected]()

def menu_loop():
	while True:
		x = keyboard.read_event(suppress=True)
		if x.event_type == "up":
			continue
		else:
			if x.name=='up':
				up()
			elif x.name=='down':
				down()
			elif x.name=='enter':
				goto_selection()
				exit()	# updated: 2024-09-21 , bug fix, unwanted behavior (looping)
			else:
				show_menu()


keypress = False
done_counting = False
waiting_time = 11 # seconds
def show_auto_msg():
	global keypress
	global done_counting
	counter = waiting_time
	while counter>0 and not keypress:
		print(" * or wait ",counter," seconds for "+menu[0]+" to run ...")
		time.sleep(1)
		counter -= 1
		print ("\x1b[A\x1b[A")
	if not keypress:
		done_counting = True
		auto_main()
		exit()
		
def stop_auto_msg():
	global keypress
	global done_counting
	while True and not done_counting:
		if keyboard.is_pressed('up') or keyboard.is_pressed('down') or keyboard.is_pressed('enter'):
			keypress=True
			break
	if not done_counting:
		menu_loop()

def main_menu():
	show_menu()
	t1 = threading.Thread(target=show_auto_msg)
	t2 = threading.Thread(target=stop_auto_msg)
	t1.start()
	t2.start()

# ------------------------------------------------------------------------ #
# ------------------------ MAIN ------------------------------------------ #
# ------------------------------------------------------------------------ #

os.system("title SUMO DYNAMIC DOWNLOADER")

n = len(sys.argv)
if n>1:
	if sys.argv[1].lower()=="auto":
		auto_main()  # auto-download script
		exit()
	elif sys.argv[1].lower()=="botd":
		botd_main()  # botd: bout-of-the-day
		exit()
	elif sys.argv[1].lower()=="main":
		main()  	# main: old main 
		exit()
else:
	main_menu()