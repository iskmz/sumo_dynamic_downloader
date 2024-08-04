this is an ARCHIVED branch (archived on 2024-08-04)

no further changes will happen to it

- - - - - - - - - - -

# sumo dynamic downloader


<b>
<p align="center"> こんにちは </p>
<p align="center"> sumo fans ! </p>
</b>


<p align="center"><img src="https://c.tenor.com/7fz6VTVZTfQAAAAC/tenor.gif" width="25%" height="25%"></p>


- - - - - - - - - - -


a python script to simplify the process of downloading grand-sumo-highlights found on [NHK website](https://www3.nhk.or.jp/nhkworld/en/tv/sumo/) 

the highlights are uploaded to the website every odd-numbered month for every basho during that month !


- - - - - - - - - - -


prerequisites:  
  1. a windows OS
  2. [ffmpeg](https://ffmpeg.org/) & [yt-dlp](https://github.com/yt-dlp/yt-dlp) installed & PATH set for both
  3. python3 installed



how to use it ?

simply create a folder for current month's basho (for e.g. "2024_05") , and copy the python script and the folder "__" and its contents inside it to that folder.
Then, run the python script and follow the instructions.



Notes:
  + to get the m3u8-urls needed for download, open the website url above, using chrome browser, during the basho month - as the videos are removed afterwards; then hit F12 for developer settings, click on the Network Tab above and look for the .m3u8 url needed, after playing the video.
  + everytime, could use the 'legacy' batch scripts provided to download 'manually', but it's a longer process, which was simplified by the python script
      - use "__download-It_multi_quiet.bat" with longer urls, such as: https://<i></i>eqj833muwr.eq.webcdn.stream.ne.jp/www50/eqj833muwr/jmc_pub/jmc_pd/[#####]/[LONG_HASH_CODE]_22.m3u8
      - use "__download-It_multi_quiet__yt-dlp.bat" with shorter urls, such as:  https://<i></i>vod-stream.nhk.jp/nhkworld/en/tv/sumo/tournament/[#####]/movies/[XYZ]/index_640x360_836k.m3u8
  + also, could manually run, "__sumo-gen-download-list.bat" , before downloading to get an ordered & well spaced STANDARD list of 'filenames' to download !

- - - - - - - - - - -
Updates:-

+ 2024-05-24 20:41 local time: added [__auto-grab.py](__/__auto-grab.py) { which utilizes [selenium](https://pypi.org/project/selenium/) webdriver & [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) }  option to choose from when running main python script for the first time, to auto-generate download list from NHK-Grand-Sumo-Highlights website instead of manual input of parameters.

+ 2024-07-25 22:45  local time:  added [__sumo_dynamic_downloader__AUTO.py](__sumo_dynamic_downloader__AUTO.py) ... which as the name says, does everything AUTOMATICALLY  ... simply double-click on it .. and leave it to do it all ...
    + it runs [__auto-grab.py](__/__auto-grab.py) if run for first time , and afterwards it compares what is available (already downloaded) with what can be downloaded/updated currently from the website ... then it grabs .m3u8 files required for each item to be downloaded, and downloads it all one by one ... all automatically , you just have to double click on it !
    + Of course, it utilizes [selenium](https://pypi.org/project/selenium/) webdriver & [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) , which should be installed along with python3, ffmpeg, yt-dlp , & with PATH set for all !
    + ~~remains TODO: is to add option for downloading the "summary" video .. hopefully , at the end of this month, when it is uploaded !~~ (added on 10:45 2024-07-30)
    +  using this AUTO script .. sumo basho videos could be downloaded automatically if running task-scheduler from windows and configuring it to run this auto script during each basho's Odd-numbered month. Should make sure to run it inside a different folder for each basho, to avoid conflicts !
  
- - - - - - - - - - -


<b>
<p align="center">楽しむ</p>


<p align="center">と</p>


<p align="center">ありがとうございます</p>
</b>



<p align="center"><img src="https://c.tenor.com/epsgnw_07kIAAAAC/tenor.gif" width="30%" height="30%"></p>

