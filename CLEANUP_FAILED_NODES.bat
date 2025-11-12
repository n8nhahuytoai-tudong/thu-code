@echo off
echo ============================================
echo CLEANUP COMFYUI FAILED NODES
echo ============================================
echo.
echo This script will DISABLE (rename) failed nodes.
echo They will NOT be deleted, just renamed with .disabled
echo You can re-enable them later by removing .disabled
echo.
echo ============================================
echo FAILED NODES TO DISABLE (12 total):
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

set /p choice="Do you want to DISABLE these nodes? (Y/N): "
if /i "%choice%" NEQ "Y" (
    echo Cancelled.
    pause
    exit /b
)

cd /d D:\ComfyUI_windows_portable\ComfyUI\custom_nodes

echo.
echo [1/12] Disabling AniTalker-ComfyUI...
if exist "AniTalker-ComfyUI" ren "AniTalker-ComfyUI" "AniTalker-ComfyUI.disabled"

echo [2/12] Disabling ComfyUI-Hallo...
if exist "ComfyUI-Hallo" ren "ComfyUI-Hallo" "ComfyUI-Hallo.disabled"

echo [3/12] Disabling ComfyUI-IP_LAP...
if exist "ComfyUI-IP_LAP" ren "ComfyUI-IP_LAP" "ComfyUI-IP_LAP.disabled"

echo [4/12] Disabling ComfyUI-MuseTalk_FSH...
if exist "ComfyUI-MuseTalk_FSH" ren "ComfyUI-MuseTalk_FSH" "ComfyUI-MuseTalk_FSH.disabled"

echo [5/12] Disabling DHLive-ComfyUI...
if exist "DHLive-ComfyUI" ren "DHLive-ComfyUI" "DHLive-ComfyUI.disabled"

echo [6/12] Disabling ViewCrafter-ComfyUI...
if exist "ViewCrafter-ComfyUI" ren "ViewCrafter-ComfyUI" "ViewCrafter-ComfyUI.disabled"

echo [7/12] Disabling ComfyUI-OllamaGemini...
if exist "ComfyUI-OllamaGemini" ren "ComfyUI-OllamaGemini" "ComfyUI-OllamaGemini.disabled"

echo [8/12] Disabling Comfyui-zhenzhen...
if exist "Comfyui-zhenzhen" ren "Comfyui-zhenzhen" "Comfyui-zhenzhen.disabled"

echo [9/12] Disabling ComfyUI-Open-Sora-I2V...
if exist "ComfyUI-Open-Sora-I2V" ren "ComfyUI-Open-Sora-I2V" "ComfyUI-Open-Sora-I2V.disabled"

echo [10/12] Disabling VideoSys-ComfyUI...
if exist "VideoSys-ComfyUI" ren "VideoSys-ComfyUI" "VideoSys-ComfyUI.disabled"

echo [11/12] Disabling ComfyUI-I2V-Adapter...
if exist "ComfyUI-I2V-Adapter" ren "ComfyUI-I2V-Adapter" "ComfyUI-I2V-Adapter.disabled"

echo [12/12] Disabling DiffSynth-ComfyUI...
if exist "DiffSynth-ComfyUI" ren "DiffSynth-ComfyUI" "DiffSynth-ComfyUI.disabled"

echo.
echo ============================================
echo DONE! All failed nodes have been disabled.
echo ============================================
echo.
echo To re-enable a node, rename it back:
echo Example: ren "AniTalker-ComfyUI.disabled" "AniTalker-ComfyUI"
echo.
echo Now restart ComfyUI to see the changes.
echo.
pause
