# sumo_dynamic_downloader


- - - - - - - - - - -
<b><p align="center"> こんにちは sumo fans ! </p></b>
- - - - - - - - - - -


a python script to simplify the process of downloading grand-sumo-highlights found on [NHK website](https://www3.nhk.or.jp/nhkworld/en/tv/sumo/) every Odd numbered month for every basho during that month !


- - - - - - - - - - -

prerequisites:  
  1. a windows OS
  2. [ffmpeg](https://ffmpeg.org/) & [yt-dlp](https://github.com/yt-dlp/yt-dlp) installed and PATH set for both of them
  3. python3 installed


simply create a folder for current month's basho (for e.g. "2024_05") , and copy the python script and the folder "__" and its contents inside it to that folder.
Then, run the python script and follow the instructions.


Notes:
  + to get the m3u8-urls needed for download, open the website url above, using chrome browser, during the basho month - as the videos are removed afterwards; then hit F12 for developer settings, click on the Network Tab above and look for the .m3u8 url needed.
  + everytime, could use the 'legacy' batch scripts provided to download 'manually', but it's a longer process, which was simplified by the python script
      - use "__download-It_multi_quiet.bat" with longer urls, such as: https://<i></i>eqj833muwr.eq.webcdn.stream.ne.jp/www50/eqj833muwr/jmc_pub/jmc_pd/[#####]/[LONG_HASH_CODE]_22.m3u8
      - use "__download-It_multi_quiet__yt-dlp.bat" with shorter urls, such as:  https://<i></i>vod-stream.nhk.jp/nhkworld/en/tv/sumo/tournament/[#####]/movies/[XYZ]/index_640x360_836k.m3u8
  + also, could manually run, "__sumo-gen-download-list.bat" , before downloading to get an ordered & well spaced STANDARD list of 'filenames' to download !


- - - - - - - - - - -


<b>
<p align="center">楽しむ</p>


<p align="center">&</p>


<p align="center">ありがとうございます</p>
</b>


<p align="center"><img src="https://www3.nhk.or.jp/nhkworld/en/tv/sumo/assets/images/logo.png" width="50%" height="50%"></p>

