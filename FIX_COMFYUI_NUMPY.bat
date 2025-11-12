@echo off
echo ============================================
echo FIX COMFYUI - NUMPY VERSION CONFLICT
echo ============================================
echo.
echo Problem: NumPy 2.2.6 is incompatible with opencv-python
echo Solution: Downgrade NumPy to 1.26.4
echo.
echo Press any key to start fixing...
pause > nul

cd /d D:\ComfyUI_windows_portable

echo.
echo [1/3] Uninstalling NumPy 2.2.6...
.\python_embeded\python.exe -m pip uninstall -y numpy

echo.
echo [2/3] Installing NumPy 1.26.4...
.\python_embeded\python.exe -m pip install "numpy<2"

echo.
echo [3/3] Verifying NumPy version...
.\python_embeded\python.exe -c "import numpy; print(f'NumPy version: {numpy.__version__}')"

echo.
echo ============================================
echo DONE! Please restart ComfyUI
echo ============================================
echo.
echo Press any key to exit...
pause > nul
