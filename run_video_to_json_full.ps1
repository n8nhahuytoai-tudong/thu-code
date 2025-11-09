# Video to JSON Converter - PowerShell Script (FULL VERSION)
# Encoding: UTF-8
# Modified to encode ENTIRE video

Add-Type -AssemblyName System.Windows.Forms

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "       CHUYEN DOI VIDEO THANH JSON - FULL VERSION" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Kiem tra Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python chua duoc cai dat!" -ForegroundColor Red
    Read-Host "Nhan Enter de thoat"
    exit 1
}

# Kiem tra opencv-python
Write-Host "[1/4] Kiem tra thu vien Python..." -ForegroundColor Yellow
$opencvCheck = python -c "import cv2; print('OK')" 2>&1
if ($opencvCheck -notmatch "OK") {
    Write-Host "[!] Dang cai dat opencv-python..." -ForegroundColor Yellow
    pip install opencv-python
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Khong the cai dat opencv-python!" -ForegroundColor Red
        Read-Host "Nhan Enter de thoat"
        exit 1
    }
    Write-Host "[OK] Da cai dat opencv-python!" -ForegroundColor Green
} else {
    Write-Host "[OK] OpenCV da san sang!" -ForegroundColor Green
}

# Mo hop thoai chon file
Write-Host ""
Write-Host "[2/4] Mo hop thoai chon file..." -ForegroundColor Yellow

$openFileDialog = New-Object System.Windows.Forms.OpenFileDialog
$openFileDialog.Title = "Chon file video"
$openFileDialog.Filter = "Video Files (*.mp4;*.avi;*.mov;*.mkv;*.webm)|*.mp4;*.avi;*.mov;*.mkv;*.webm|All Files (*.*)|*.*"
$openFileDialog.InitialDirectory = [Environment]::GetFolderPath("MyVideos")

$result = $openFileDialog.ShowDialog()

if ($result -eq [System.Windows.Forms.DialogResult]::OK) {
    $videoPath = $openFileDialog.FileName
    Write-Host "[OK] File da chon: $videoPath" -ForegroundColor Green
} else {
    Write-Host "[!] Khong co file nao duoc chon!" -ForegroundColor Yellow
    Read-Host "Nhan Enter de thoat"
    exit 0
}

# Lay thong tin file
$videoFile = Get-Item $videoPath
$videoDir = $videoFile.DirectoryName
$videoName = $videoFile.BaseName
$outputFile = Join-Path $videoDir "$videoName`_full.json"

# Tuy chon xu ly
Write-Host ""
Write-Host "[3/4] Tuy chon xu ly - ENCODE TOAN BO VIDEO" -ForegroundColor Yellow
Write-Host ""
Write-Host "Chon che do extract frames:"
Write-Host "  1 - FULL (moi 2 giay, ~20 frames cho video 40s) - KHUYEN NGHI"
Write-Host "  2 - DETAILED (moi 1 giay, ~40 frames)"
Write-Host "  3 - VERY DETAILED (moi 0.5 giay, ~80 frames)"
Write-Host "  4 - TUY CHINH (tu nhap)"
Write-Host "  5 - Chi lay metadata (khong extract frames)"
Write-Host ""

$extractChoice = Read-Host "Chon (1-5)"

switch ($extractChoice) {
    "1" {
        # FULL - moi 2 giay
        $frameInterval = "120"  # 2 giay * 60fps
        $maxFrames = "999"      # Khong gioi han (999 la du lon)
        Write-Host "[OK] Che do FULL: moi 2 giay, toan bo video" -ForegroundColor Green
    }
    "2" {
        # DETAILED - moi 1 giay
        $frameInterval = "60"   # 1 giay * 60fps
        $maxFrames = "999"
        Write-Host "[OK] Che do DETAILED: moi 1 giay, toan bo video" -ForegroundColor Green
    }
    "3" {
        # VERY DETAILED - moi 0.5 giay
        $frameInterval = "30"   # 0.5 giay * 60fps
        $maxFrames = "999"
        Write-Host "[OK] Che do VERY DETAILED: moi 0.5 giay, toan bo video" -ForegroundColor Green
    }
    "4" {
        # TUY CHINH
        Write-Host ""
        $frameInterval = Read-Host "Khoang cach giua cac frames (so frames, mac dinh 120)"
        if ([string]::IsNullOrWhiteSpace($frameInterval)) { $frameInterval = "120" }

        $maxFrames = Read-Host "So frame toi da (mac dinh 999 = khong gioi han)"
        if ([string]::IsNullOrWhiteSpace($maxFrames)) { $maxFrames = "999" }

        Write-Host "[OK] Tuy chinh: interval $frameInterval, max $maxFrames" -ForegroundColor Green
    }
    "5" {
        # Chi metadata
        $extractParam = "--no-frames"
        Write-Host "[OK] Chi extract metadata" -ForegroundColor Green
    }
    default {
        # Mac dinh la FULL
        $frameInterval = "120"
        $maxFrames = "999"
        Write-Host "[OK] Che do FULL (mac dinh): moi 2 giay" -ForegroundColor Green
    }
}

if ($extractChoice -ne "5") {
    $extractParam = "--interval $frameInterval --max-frames $maxFrames"
}

# Chay script Python
Write-Host ""
Write-Host "[4/4] Dang xu ly video..." -ForegroundColor Yellow
Write-Host "Vui long doi, co the mat 1-3 phut..." -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptDir "video_to_json.py"

# Kiem tra file Python script co ton tai khong
if (-not (Test-Path $pythonScript)) {
    # Neu khong co, dung script moi
    $pythonScript = Join-Path $scriptDir "video_to_json_full.py"
}

$arguments = "`"$videoPath`" $extractParam"
$processInfo = Start-Process -FilePath "python" -ArgumentList "`"$pythonScript`" $arguments" -Wait -NoNewWindow -PassThru

if ($processInfo.ExitCode -eq 0) {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "[SUCCESS] Hoan thanh!" -ForegroundColor Green
    Write-Host ""

    # Tim file output
    $possibleOutputs = @(
        $outputFile,
        (Join-Path $videoDir "$videoName`_info.json"),
        (Join-Path $videoDir "123_full.json")
    )

    $actualOutput = $null
    foreach ($path in $possibleOutputs) {
        if (Test-Path $path) {
            $actualOutput = $path
            break
        }
    }

    if ($actualOutput) {
        Write-Host "File JSON da duoc luu tai:" -ForegroundColor Cyan
        Write-Host $actualOutput -ForegroundColor White

        # Hien thi kich thuoc file
        $fileSize = (Get-Item $actualOutput).Length / 1MB
        Write-Host "Kich thuoc: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Cyan
        Write-Host ""

        # Hoi co muon mo file JSON khong
        $openChoice = Read-Host "Ban co muon mo file JSON khong? (y/n)"
        if ($openChoice -eq "y" -or $openChoice -eq "Y") {
            Start-Process notepad $actualOutput
        }

        # Hoi co muon mo thu muc khong
        $folderChoice = Read-Host "Ban co muot mo thu muc chua file khong? (y/n)"
        if ($folderChoice -eq "y" -or $folderChoice -eq "Y") {
            explorer $videoDir
        }
    } else {
        Write-Host "Khong tim thay file output!" -ForegroundColor Yellow
        Write-Host "Hay kiem tra thu muc: $videoDir" -ForegroundColor Yellow
    }

} else {
    Write-Host ""
    Write-Host "[ERROR] Co loi xay ra khi xu ly video!" -ForegroundColor Red
    Write-Host "Ma loi: $($processInfo.ExitCode)" -ForegroundColor Red
}

Write-Host ""
Read-Host "Nhan Enter de thoat"
