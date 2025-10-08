@echo off
setlocal EnableDelayedExpansion

set "PORT=5000"

rem Launch Codeset UI server
cd /d "%~dp0\codeset_ui_app" || exit /b 1
start "Codeset UI Server" cmd /c "python app.py"

echo Waiting for Codeset UI server to start...
for /l %%I in (1,1,20) do (
    timeout /t 1 /nobreak >nul
    powershell -NoProfile -Command "try { $client = New-Object System.Net.Sockets.TcpClient('127.0.0.1',%PORT%); if ($client.Connected) { $client.Dispose(); exit 0 } else { exit 1 } } catch { exit 1 }"
    if !errorlevel! EQU 0 goto resolve_ip
)
echo Unable to confirm server availability; continuing to open the browser.

:resolve_ip
for /f "usebackq tokens=*" %%I in (`powershell -NoProfile -Command "try { $ip = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceOperationalStatus Up | Where-Object { $_.IPAddress -notlike '127.*' -and $_.IPAddress -notlike '169.254.*' } | Select-Object -First 1 -ExpandProperty IPAddress); if (-not $ip) { $ip = '127.0.0.1' }; Write-Output $ip } catch { '127.0.0.1' }"`) do set "HOST_IP=%%I"
if not defined HOST_IP set "HOST_IP=127.0.0.1"
set "HOST_IP=%HOST_IP: =%"
set "SERVER_URL=http://%HOST_IP%:%PORT%/"

echo Opening %SERVER_URL%
start "" "%SERVER_URL%"

endlocal
