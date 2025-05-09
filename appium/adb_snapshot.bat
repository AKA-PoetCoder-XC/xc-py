@echo off
set filename=%~1
if "%filename%"=="" set filename=app

adb root
adb shell uiautomator dump /sdcard/%filename%.uix
adb shell screencap -p /sdcard/%filename%.png
adb pull /sdcard/%filename%.uix ./snapshot/%filename%.uix
adb pull /sdcard/%filename%.png ./snapshot/%filename%.png
adb shell rm /sdcard/%filename%.uix
adb shell rm /sdcard/%filename%.png