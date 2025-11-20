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
  2. FIREFOX browser installed (used as a web driver, as of the 2025-07-22 update; check Updates below)
  3. [ffmpeg](https://ffmpeg.org/) & [yt-dlp](https://github.com/yt-dlp/yt-dlp) installed & PATH set for both
  4. python3 installed + required modules installed (check imports at top of the script)



how to use it ?

simply create a folder for current month's basho (for e.g. "2024_05") , and copy the python script to that folder and run it following the instructions.


- - - - - - - - - - -


<details>
<summary> Notes (more relevant to older versions) </summary>

  + to get the m3u8-urls needed for download, open the website url above, using chrome browser, during the basho month - as the videos are removed afterwards; then hit F12 for developer settings, click on the Network Tab above and look for the .m3u8 url needed, after playing the video.
  + everytime, could use the 'legacy' batch scripts provided to download 'manually', but it's a longer process, which was simplified by the python script
      - use "__download-It_multi_quiet.bat" with longer urls, such as: https://<i></i>eqj833muwr.eq.webcdn.stream.ne.jp/www50/eqj833muwr/jmc_pub/jmc_pd/[#####]/[LONG_HASH_CODE]_22.m3u8
      - use "__download-It_multi_quiet__yt-dlp.bat" with shorter urls, such as:  https://<i></i>vod-stream.nhk.jp/nhkworld/en/tv/sumo/tournament/[#####]/movies/[XYZ]/index_640x360_836k.m3u8
  + also, could manually run, "__sumo-gen-download-list.bat" , before downloading to get an ordered & well spaced STANDARD list of 'filenames' to download !

  
</details>

  
- - - - - - - - - - -


Updates:-


<details>
<summary> 2024-05-24 20:41 </summary>

* added [__auto-grab.py](https://github.com/iskmz/sumo_dynamic_downloader/blob/OLD_20240804/__/__auto-grab.py) { which utilizes [selenium](https://pypi.org/project/selenium/) webdriver & [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) }  option to choose from when running main python script for the first time, to auto-generate download list from NHK-Grand-Sumo-Highlights website instead of manual input of parameters.
    
</details>


<details>
<summary> 2024-07-25 22:45 </summary>

  + added [__sumo_dynamic_downloader__AUTO.py](https://github.com/iskmz/sumo_dynamic_downloader/blob/OLD_20240804/__sumo_dynamic_downloader__AUTO.py) ... which as the name says, does everything AUTOMATICALLY  ... simply double-click on it .. and leave it to do it all ...
  + it runs [__auto-grab.py](https://github.com/iskmz/sumo_dynamic_downloader/blob/OLD_20240804/__/__auto-grab.py) if run for first time , and afterwards it compares what is available (already downloaded) with what can be downloaded/updated currently from the website ... then it grabs .m3u8 files required for each item to be downloaded, and downloads it all one by one ... all automatically , you just have to double click on it !
  + Of course, it utilizes [selenium](https://pypi.org/project/selenium/) webdriver & [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) , which should be installed along with python3, ffmpeg, yt-dlp , & with PATH set for all !
  + ~~remains TODO: is to add option for downloading the "summary" video .. hopefully , at the end of this month, when it is uploaded !~~ (added on 10:45 2024-07-30)
  +  using this AUTO script .. sumo basho videos could be downloaded automatically if running task-scheduler from windows and configuring it to run this auto script during each basho's Odd-numbered month. Should make sure to run it inside a different folder for each basho, to avoid conflicts !

</details>


<details>
<summary> 2024-08-04 18:05 </summary>

  - all the files inside "__" folder were replaced by code in a single file: "[__sumo_dynamic_downloader__.py](https://github.com/iskmz/sumo_dynamic_downloader/blob/main/__sumo_dynamic_downloader__.py)" , including code for legacy batch scripts (converted to python code) and for other .py scripts (integrated into main one)
  - all the scripts for AUTO downloading are inside as well !
  - also added a new BOTD script , to download "bouts-of-the-day" which appear every single day of the basho (for the previous day)
    + it is better to run BOTD after the basho's last day to get all the files required at once
    + it works for previous/historic bashos as well , but might miss a few (or many) bouts-of-the-day [could be already deleted from site storage , or , simply, my-code didn't "guess" the right .m3u8 url]
  - to run BOTD functions directly, simply double click on [__sumo_dynamic_downloader__botd.py](https://github.com/iskmz/sumo_dynamic_downloader/blob/main/__sumo_dynamic_downloader__botd.py)
  - to run AUTO-downloader functions directly, simply double click on [__sumo_dynamic_downloader__auto.py](https://github.com/iskmz/sumo_dynamic_downloader/blob/main/__sumo_dynamic_downloader__auto.py)
  - the scripts "__sumo_dynamic_downloader__auto.py" & "__sumo_dynamic_downloader__botd.py" are simply a helper one-liners to call what is needed from the main script !
  - <b>PREVIOUS CODE FILES WERE ARCHIVED: check the [OLD_20240804](https://github.com/iskmz/sumo_dynamic_downloader/tree/OLD_20240804) branch.</b>

</details>

<details>
<summary> 2024-09-21 09:11</summary>

  - <b>PREVIOUS CODE FILES WERE ARCHIVED: check the [OLD_20240921](https://github.com/iskmz/sumo_dynamic_downloader/tree/OLD_20240921) branch.</b>
  - instead, uploaded a single code file (similar to the last one) but with a selection menu at the beginning to choose from:  AUTO|MAIN|BOTD|EXIT
  - therefore, no need for additional helper one-liner scripts like in the previous branch/update
  - for further details regarding the selection menu code , check [python_generic_console_menu](https://github.com/iskmz/python_generic_console_menu) repo.
  - also: few bug fixes (more on: 2024-09-23)

<p align="center"><img src="https://github.com/user-attachments/assets/7bac5ed3-e824-4db0-9e77-d71f9da2da59"/></p>

</details>

<details>
<summary> 2025-07-22 13:11 </summary>

  - <b> previous code file was NOT archived , only updated ... </b>
  - two main issues / errors were addressed:
      + Minor compatibility issue with BOTD downloads which appeared after updating yt-dlp to the "2025.05.22" release. A simple fix was by removing "/" for some file-path generated in the code solved the issue.
      + Major issue which appeared this month , and it is most likely NOT related to the yt-dlp update: All AUTO features suddenly FAILED, reason unknown, but some digging suggested selenium & chrome-driver issue related to "ERR_HTTP2_PROTOCOL_ERROR".  Could not fix this issue directly, so instead replaced the chrome-driver which selenium uses with the FIREFOX webdriver, and kept an option/switch to return back to chrome-driver if needed (by changing a boolean at the top of the code). HOWEVER, currently, firefox webdriver is the DEFAULT used with selenium, and it might need [geckodriver](https://github.com/mozilla/geckodriver/releases) downloaded and PATH set for it , depending on the firefox version installed. It worked fine without it in my system, so it might have came pre-installed with firefox browser.  Needless to say: FIREFOX web-browser must be installed on your system for the code to work.
  - I suggest keeping the FIREFOX webdriver, because it is much cleaner when downloading, as it does not add extra prompts that I could not hide when using chrome-driver.
  - Also: added some minor fixes and extra prompts when downloading .m3u8 urls.
  - SOMETIMES: .m3u8 urls do not get grabbed for UNKNOWN reason, in that case they are skipped (the ones that fail to be grabbed). This issue was always resolved by simply RE-RUNNING the script again (or 3 times) until the URL gets grabbed. It might be related to some "delay" in the selenium driver.
  - NOTE: should use the yt-dlp 2025.05.22 release with this script, as newer updates were not tested and might have some new issues/errors.


</details>


<details>
<summary> 2025-09-12 13:19 </summary>
  
  - <b> previous code file was NOT archived , only updated ... </b>
  - minor fix: used regex for pattern recognition for better adaptability with site changes (check changes in lines 104-116)

</details>

- - - - - - - - - - -

<h3><b> MAJOR CHANGES </b></h3>

<h4><i>2025.11.20</i></h4>

an update to batch script V3A1MD:

instead of inputing items to LIST by editing this script, added an input loop at the start so that users simply copy titles from zzz_toDownload.txt after running the script. NO need for editing the LIST anymore.

<h4><i>2025.11.18</i></h4>

Towards the end of the 2025.09 basho, there were major changes to NHK website video player and the way [.m3u8] streams are handled. These changes persist to this day and resulted in failure of the AUTO section of the [__sumo_dd__](https://github.com/iskmz/sumo_dynamic_downloader/blob/main/__sumo_dd__.py) ; other parts MAIN & BOTD still work fine, and also the 4 "rikishi" videos can be downloaded using the AUTO section but all others fail to download due to these changes.

uploaded a temporary batch script to help in handling the now NOT AUTOMATIC download process [__V3A1MD__](https://github.com/iskmz/sumo_dynamic_downloader/blob/main/__V3A1MD__.bat) ; it helps make manual downloads easier but .m3u8 urls need to be manually copied again as explained in the NOTES section above for each video individually ; and now audio and video are separated due to NHK changes so two streams are needed to be downloaded for each video !  one video [v3.m3u8] and one audio [a1.m3u8] , hence the V3A1 in the name and also they need to be merged [M] into one .mp4 file and then deleted [D] , so it's <b><i>V3A1MD protocol</b></i>.

The batch scripts handles the download, merge and delete process using ffmpeg only, so no python is needed for this.

It only needs the titles to be provided to it , by editing the LIST variable at the top of the script BEFORE running it. Title names could be copied from the "zzz_toDownload.txt" files generated from the sumo_dd auto script when it first runs. Then, after doing so and running the batch scripts it only ask for the v3 & a1 .m3u8 streams which the user needs to copy from chrome-dev-tools as explained in NOTES section above.
Afterwards, download is handled quietly using ffmpeg. There is a pause before each section [merge or delete] so that the user can check things out and continue or exit.

Unfortunately, a permanent fix for the sumo_dd python script won't be written in the near future due to busy schedule !

maybe towards the spring/summer of 2026 !


- - - - - - - - - - -


<b>
<p align="center">楽しむ</p>


<p align="center">と</p>


<p align="center">ありがとうございます</p>
</b>



<p align="center"><img src="https://c.tenor.com/epsgnw_07kIAAAAC/tenor.gif" width="30%" height="30%"></p>

