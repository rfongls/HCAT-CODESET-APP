@echo off
rem Launch Codeset UI server and open browser
cd /d "%~dp0\codeset_ui_app"
start "" python app.py
rem wait for server to start
timeout /t 3 >nul
start "" http://127.0.0.1:5000/
