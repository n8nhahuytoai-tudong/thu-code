@echo off
title Ket noi VPS
echo ====================================
echo    Dang ket noi den VPS...
echo ====================================
echo.
ssh -p 30195 root@ssh6.vast.ai -L 8080:localhost:8080
pause
