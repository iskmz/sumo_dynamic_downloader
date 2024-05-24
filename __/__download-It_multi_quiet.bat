@echo off
cls

echo.
echo - - - - - - - - -
echo  "Just"
echo      Download
echo       It !!
echo - - - - - - - - -
echo.

SET /p amount="Enter amount of files to download: "
SET /A _amount=%amount%
echo.

setlocal enabledelayedexpansion

FOR /L %%A IN (1,1,%_amount%) DO (
	echo %%A:
	SET /P _url="url:  "
	SET /P _name="filename:  "
	echo echo %%A:  >> "_download.bat"
	echo ffmpeg -v quiet -hide_banner -stats -i "!_url!" -c copy -bsf:a aac_adtstoasc "!_name!.mp4" >> "_download.bat"
	echo !_name!:  !_url! >> "_urls.txt"
)

endlocal

echo.
echo Downloading ...
CALL "_download.bat"
echo.
del "_download.bat"

echo. && echo DONE ! && echo.


timeout -1