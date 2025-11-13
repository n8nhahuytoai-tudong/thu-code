@echo off
title Ket noi VPS
echo ====================================
echo    Dang ket noi den VPS...
echo ====================================
echo.
echo Port forward: http://localhost:8080
echo.
ssh -p 56254 root@115.231.176.132 -L 8080:localhost:8080
pause
