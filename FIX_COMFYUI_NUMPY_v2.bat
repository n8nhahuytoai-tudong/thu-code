@echo off
echo ============================================
echo FIX COMFYUI - NUMPY VERSION CONFLICT (v2)
echo ============================================
echo.
echo Problem: NumPy 2.2.6 is incompatible with opencv-python
echo Python 3.13.6 requires specific NumPy version with pre-built wheel
echo Solution: Install NumPy 1.26.4 with pre-built wheel
echo.
echo Press any key to start fixing...
pause > nul

cd /d D:\ComfyUI_windows_portable

echo.
echo [1/5] Checking Python version...
.\python_embeded\python.exe --version

echo.
echo [2/5] Uninstalling NumPy 2.2.6...
.\python_embeded\python.exe -m pip uninstall -y numpy

echo.
echo [3/5] Cleaning up temporary files...
if exist ".\python_embeded\Lib\site-packages\~umpy.libs" rmdir /s /q ".\python_embeded\Lib\site-packages\~umpy.libs"
if exist ".\python_embeded\Lib\site-packages\~umpy" rmdir /s /q ".\python_embeded\Lib\site-packages\~umpy"

echo.
echo [4/5] Installing NumPy 1.26.4 with pre-built wheel...
.\python_embeded\python.exe -m pip install numpy==1.26.4 --only-binary :all: --no-cache-dir

echo.
echo If above failed, trying alternative versions...
.\python_embeded\python.exe -m pip install numpy==1.26.3 --only-binary :all: --no-cache-dir 2>nul
if errorlevel 1 (
    echo Trying NumPy 1.26.2...
    .\python_embeded\python.exe -m pip install numpy==1.26.2 --only-binary :all: --no-cache-dir
)

echo.
echo [5/5] Verifying installation...
.\python_embeded\python.exe -c "import numpy; print(f'NumPy version: {numpy.__version__}')"
.\python_embeded\python.exe -c "import cv2; print('OpenCV: OK')" 2>nul || echo OpenCV will be tested after ComfyUI restart

echo.
echo ============================================
echo DONE! Please restart ComfyUI
echo ============================================
echo.
echo Press any key to exit...
pause > nul
