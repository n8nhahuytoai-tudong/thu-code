# Video to JSON Converter - PowerShell Script
# Encoding: UTF-8

Add-Type -AssemblyName System.Windows.Forms

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "       CHUYEN DOI VIDEO THANH JSON" -ForegroundColor Cyan
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
$outputFile = Join-Path $videoDir "$videoName`_info.json"

# Tuy chon xu ly
Write-Host ""
Write-Host "[3/4] Tuy chon xu ly" -ForegroundColor Yellow
Write-Host ""
Write-Host "Ban co muon extract frames tu video khong?"
Write-Host "  1 - Co (extract frames, file JSON se lon hon)"
Write-Host "  2 - Khong (chi lay metadata, file JSON nho)"
Write-Host ""

$extractChoice = Read-Host "Chon (1 hoac 2)"

if ($extractChoice -eq "2") {
    $extractParam = "--no-frames"
    Write-Host "[OK] Chi extract metadata" -ForegroundColor Green
} else {
    Write-Host ""
    $frameInterval = Read-Host "Khoang cach giua cac frames (mac dinh 30, Enter de bo qua)"
    if ([string]::IsNullOrWhiteSpace($frameInterval)) { $frameInterval = "30" }

    $maxFrames = Read-Host "So frame toi da (mac dinh 10, Enter de bo qua)"
    if ([string]::IsNullOrWhiteSpace($maxFrames)) { $maxFrames = "10" }

    $extractParam = "--interval $frameInterval --max-frames $maxFrames"
    Write-Host "[OK] Se extract frames (interval: $frameInterval, max: $maxFrames)" -ForegroundColor Green
}

# Chay script Python
Write-Host ""
Write-Host "[4/4] Dang xu ly video..." -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptDir "video_to_json.py"

$arguments = "`"$videoPath`""
$processInfo = Start-Process -FilePath "python" -ArgumentList "`"$pythonScript`" $arguments" -Wait -NoNewWindow -PassThru

if ($processInfo.ExitCode -eq 0) {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "[SUCCESS] Hoan thanh!" -ForegroundColor Green
    Write-Host ""
    Write-Host "File JSON da duoc luu tai:" -ForegroundColor Cyan
    Write-Host $outputFile -ForegroundColor White
    Write-Host ""

    # Hoi co muon mo file JSON khong
    $openChoice = Read-Host "Ban co muon mo file JSON khong? (y/n)"
    if ($openChoice -eq "y" -or $openChoice -eq "Y") {
        Start-Process $outputFile
    }

    # Hoi co muon mo thu muc khong
    $folderChoice = Read-Host "Ban co muon mo thu muc chua file khong? (y/n)"
    if ($folderChoice -eq "y" -or $folderChoice -eq "Y") {
        explorer $videoDir
    }

} else {
    Write-Host ""
    Write-Host "[ERROR] Co loi xay ra khi xu ly video!" -ForegroundColor Red
}

Write-Host ""
Read-Host "Nhan Enter de thoat"
