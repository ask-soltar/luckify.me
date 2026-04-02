@echo off
title Golf Analytics - Remote API
cd /d D:\Projects\luckify-me
echo Installing Flask...
C:\Users\crzzy\AppData\Local\Programs\Python\Python311\python.exe -m pip install flask -q
echo.
echo Starting API server...
echo.
C:\Users\crzzy\AppData\Local\Programs\Python\Python311\python.exe remote_api.py
pause
