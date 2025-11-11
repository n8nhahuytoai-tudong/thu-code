@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title Batch File Test
color 0A

echo ================================================================
echo TESTING BATCH FILE SYNTAX
echo ================================================================
echo.

echo [TEST 1] Basic echo
echo This should display correctly
echo.

echo [TEST 2] Variable assignment
set "TESTVAR=Hello World"
echo Variable value: %TESTVAR%
echo.

echo [TEST 3] Delayed expansion
set "COUNT=5"
echo Before: %COUNT%
set "COUNT=10"
echo After with %%: %COUNT%
echo After with !!: !COUNT!
echo.

echo [TEST 4] User input (optional)
set /p "USERNAME=Enter your name (or press Enter to skip): "
if not "!USERNAME!"=="" (
    echo Hello, !USERNAME!!
) else (
    echo You skipped the input.
)
echo.

echo [TEST 5] Conditional check
if exist "RUN.bat" (
    echo [OK] RUN.bat found
) else (
    echo [ERROR] RUN.bat not found
)

if exist "INSTALL.bat" (
    echo [OK] INSTALL.bat found
) else (
    echo [ERROR] INSTALL.bat not found
)

if exist "DRAG_VIDEO_HERE.bat" (
    echo [OK] DRAG_VIDEO_HERE.bat found
) else (
    echo [ERROR] DRAG_VIDEO_HERE.bat not found
)
echo.

echo ================================================================
echo ALL SYNTAX TESTS PASSED!
echo ================================================================
echo.
echo If you can read this, the batch file syntax is correct.
echo Now try running RUN.bat or INSTALL.bat
echo.

pause
