@echo off
echo ============================================
echo DELETE COMFYUI FAILED NODES
echo ============================================
echo.
echo WARNING: This will PERMANENTLY DELETE failed nodes!
echo This action CANNOT be undone!
echo.
echo You will need to reinstall them from ComfyUI Manager if you want them back.
echo.
echo ============================================
echo FAILED NODES TO DELETE (12 total):
echo ============================================
echo.
echo 1.  AniTalker-ComfyUI (missing: scipy.integrate.simps)
echo 2.  ComfyUI-Hallo (missing: mediapipe)
echo 3.  ComfyUI-IP_LAP (missing: mediapipe)
echo 4.  ComfyUI-MuseTalk_FSH (missing: mmpose)
echo 5.  DHLive-ComfyUI (missing: mediapipe)
echo 6.  ViewCrafter-ComfyUI (missing: pytorch3d)
echo 7.  ComfyUI-OllamaGemini (missing: anthropic)
echo 8.  Comfyui-zhenzhen (missing: nest_asyncio)
echo 9.  ComfyUI-Open-Sora-I2V (missing: colossalai)
echo 10. VideoSys-ComfyUI (missing: colossalai)
echo 11. ComfyUI-I2V-Adapter (missing: diffusers.modeling_utils)
echo 12. DiffSynth-ComfyUI (import conflict)
echo.
echo ============================================
echo.

set /p choice="Are you SURE you want to DELETE these nodes? (Y/N): "
if /i "%choice%" NEQ "Y" (
    echo Cancelled.
    pause
    exit /b
)

echo.
set /p confirm="Type 'DELETE' to confirm: "
if /i "%confirm%" NEQ "DELETE" (
    echo Cancelled - confirmation failed.
    pause
    exit /b
)

cd /d D:\ComfyUI_windows_portable\ComfyUI\custom_nodes

echo.
echo Deleting failed nodes...
echo.

if exist "AniTalker-ComfyUI" (
    echo [1/12] Deleting AniTalker-ComfyUI...
    rmdir /s /q "AniTalker-ComfyUI"
)

if exist "ComfyUI-Hallo" (
    echo [2/12] Deleting ComfyUI-Hallo...
    rmdir /s /q "ComfyUI-Hallo"
)

if exist "ComfyUI-IP_LAP" (
    echo [3/12] Deleting ComfyUI-IP_LAP...
    rmdir /s /q "ComfyUI-IP_LAP"
)

if exist "ComfyUI-MuseTalk_FSH" (
    echo [4/12] Deleting ComfyUI-MuseTalk_FSH...
    rmdir /s /q "ComfyUI-MuseTalk_FSH"
)

if exist "DHLive-ComfyUI" (
    echo [5/12] Deleting DHLive-ComfyUI...
    rmdir /s /q "DHLive-ComfyUI"
)

if exist "ViewCrafter-ComfyUI" (
    echo [6/12] Deleting ViewCrafter-ComfyUI...
    rmdir /s /q "ViewCrafter-ComfyUI"
)

if exist "ComfyUI-OllamaGemini" (
    echo [7/12] Deleting ComfyUI-OllamaGemini...
    rmdir /s /q "ComfyUI-OllamaGemini"
)

if exist "Comfyui-zhenzhen" (
    echo [8/12] Deleting Comfyui-zhenzhen...
    rmdir /s /q "Comfyui-zhenzhen"
)

if exist "ComfyUI-Open-Sora-I2V" (
    echo [9/12] Deleting ComfyUI-Open-Sora-I2V...
    rmdir /s /q "ComfyUI-Open-Sora-I2V"
)

if exist "VideoSys-ComfyUI" (
    echo [10/12] Deleting VideoSys-ComfyUI...
    rmdir /s /q "VideoSys-ComfyUI"
)

if exist "ComfyUI-I2V-Adapter" (
    echo [11/12] Deleting ComfyUI-I2V-Adapter...
    rmdir /s /q "ComfyUI-I2V-Adapter"
)

if exist "DiffSynth-ComfyUI" (
    echo [12/12] Deleting DiffSynth-ComfyUI...
    rmdir /s /q "DiffSynth-ComfyUI"
)

echo.
echo ============================================
echo DONE! All failed nodes have been deleted.
echo ============================================
echo.
echo Restart ComfyUI to see the changes.
echo You can reinstall nodes from ComfyUI Manager if needed.
echo.
pause
