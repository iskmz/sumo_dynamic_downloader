@echo off
cls
echo.
echo.

SET /p year="> Enter Tournament's Year (YYYY): "
SET /p month="> Enter Tournament's Month (MM): "
SET /p day="> Enter Tournament's starting day (DD): "
SET /A _day1=%day%
SET /A _day14=%_day1%+13
SET /A _day15=%_day1%+14
echo.
Set /p rikishi="> Enter number of rikishi intro. videos: "
Set /A _rikishi=%rikishi%

echo 00__PREVIEW>> "zzz_toDownload.txt"

setlocal enabledelayedexpansion

FOR /L %%A IN (1,1,%_rikishi%) DO (
	Set /p name=">>> name of rikishi #%%A: " 
	echo 00_!name!>> "zzz_toDownload.txt"
)

echo.
echo . . .
echo.

echo.>> "zzz_toDownload.txt"

echo LIVE_01_%_day1%_OpeningDay>> "zzz_toDownload.txt"

SET /A currDay=%_day1%

FOR /L %%A IN (1,1,7) DO (
	echo 0%%A_!currDay!>> "zzz_toDownload.txt"
	SET /A currDay=!currDay!+1
)

echo.>> "zzz_toDownload.txt"

echo LIVE_08_%currDay%_HalfwayPoint>> "zzz_toDownload.txt"
echo 08_%currDay%>> "zzz_toDownload.txt"
SET /A currDay=%currDay%+1
echo 09_%currDay%>> "zzz_toDownload.txt"
SET /A currDay=%currDay%+1

FOR /L %%A IN (10,1,15) DO (
	echo %%A_!currDay!>> "zzz_toDownload.txt"
	SET /A currDay=!currDay!+1
)


echo LIVE_14_%_day14%>> "zzz_toDownload.txt"
echo LIVE_15_%_day15%_FinalDay>> "zzz_toDownload.txt"

echo.>> "zzz_toDownload.txt"

echo summary_%year%_%month%>> "zzz_toDownload.txt"

endlocal

echo. && echo DONE ! && echo.

timeout -1