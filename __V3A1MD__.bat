@echo off

cls

title SUMO - V3A1MD
:: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
::  created 2025.11.18 
::  to put all the steps developed over the last week
::  in a single batch script , for a simpler future use
:: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
:: new download protocol
:: V3A1MD
:: download v3.m3u8
:: download a1.m3u8
:: merge v+a
:: delete v and a
:: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
:: BEFORE running this batch script
:: manually edit the LIST below for the required TITLES to be downloaded
:: get the TITLE NAMES from zzz_toDownload.txt based on what is new on the website
:: separate items by a single space

SET LIST=[TITLE_1] [TITLE_2] [TITLE_3] [TITLE_4]

:: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
::                             NO EDITS BELOW THIS LINE
:: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

echo.
echo 			- - - - - - - - - - - - -
echo 			     SUMO - V3A1MD
echo 			- - - - - - - - - - - - -
echo.
echo.

setlocal enabledelayedexpansion

:: - - - - - - - - - - - - - - - - - - - - - - - - - - - -
::  INPUT m3u8 urls for V3 and A1 
:: - - - - - - - - - - - - - - - - - - - - - - - - - - - -

echo.
echo.
echo    Enter m3u8 urls for-each title ... FIRST  v3  THEN  a1 :-
echo.
echo.

FOR %%A IN (%LIST%) DO (
	SET /P v_url="%%A_v:  "
	SET /P a_url="%%A_a:  "
	
	echo echo %%A_v:  >> "_download.bat"
	echo ffmpeg -v quiet -hide_banner -stats -i "!v_url!" -c copy -bsf:a aac_adtstoasc "%%A_v.mp4" >> "_download.bat"
	echo %%A_v:  !v_url!>> "_urls.txt"
	
	echo echo %%A_a:  >> "_download.bat"
	echo ffmpeg -v quiet -hide_banner -stats -i "!a_url!" -c copy -bsf:a aac_adtstoasc "%%A_a.mp4" >> "_download.bat"
	echo %%A_a:  !a_url!>> "_urls.txt"
)

echo.
echo.
echo - - - - - - - - - - - - - - - - - - - - - - - - - 
echo.
echo.

:: - - - - - - - - - - - - - - - - - - - - - - - - - - - -
:: DOWNLOAD V3 and A1
:: - - - - - - - - - - - - - - - - - - - - - - - - - - - -

echo Downloading ...
echo.
CALL "_download.bat"
echo.
echo.
del "_download.bat"
echo.
echo   DONE DOWNLOADING V3 and A1
echo.
echo.
echo.   next is MERGE step
echo.
echo.
pause

:: - - - - - - - - - - - - - - - - - - - - - - - - - - - -
:: MERGE
:: - - - - - - - - - - - - - - - - - - - - - - - - - - - -

cls

echo.
echo Merging each V and A to a single mp4 file ...
echo.

FOR %%A IN (%LIST%) DO (
	echo.
	echo  %%A_v.mp4  AND  %%A_a.mp4  TO  %%A.mp4:
	ffmpeg -v quiet -hide_banner -stats -i "%%A_v.mp4" -i "%%A_a.mp4" -c:v copy -c:a aac "%%A.mp4"
)

echo.
echo.
echo   DONE MERGING !!!
echo.
echo.
echo.  next is DELETION step
echo.
echo.
pause 

:: - - - - - - - - - - - - - - - - - - - - - - - - - - - -
:: DELETE
:: - - - - - - - - - - - - - - - - - - - - - - - - - - - -

cls

echo.
echo Cleaning up / deleting extra V and A files after merger ...
echo.
echo . . . . .
echo  . . . .
echo   . . .
echo    . .
echo     .
echo    . .
echo   . . .
echo  . . . .
echo . . . . .
echo.

del "*_v.mp4" 
del "*_a.mp4"

endlocal

echo.
echo.
echo DONE ALL !!!
echo.
echo.
pause