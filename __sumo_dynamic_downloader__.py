import os

# -------------------- constants ------------------ #

DOWNLOAD_LIST_FILENAME = "zzz_toDownload.txt"


# ------------------- functions ------------------ #

def runListGen():
	os.system('Call __\\__sumo-gen-download-list.bat')

def runDownload():
	os.system('Call __\\__download-It_multi_quiet.bat')
	exit()
	
def runDownload_ytdlp():
	os.system('Call __\\__download-It_multi_quiet__yt-dlp.bat')
	exit()
	
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


# -------------------- main ---------------------- #

os.system("title SUMO DYNAMIC DOWNLOADER")

if not os.path.isfile(DOWNLOAD_LIST_FILENAME):
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
	runDownload()
	
if inputStr=="y" or inputStr=="Y":
	runDownload_ytdlp()


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