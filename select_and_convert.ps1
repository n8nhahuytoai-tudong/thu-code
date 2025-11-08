# Video to JSON Converter - PowerShell Script
# Encoding: UTF-8

Add-Type -AssemblyName System.Windows.Forms

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   VIDEO TO JSON CONVERTER" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Kiểm tra Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python chưa được cài đặt!" -ForegroundColor Red
    Read-Host "Nhấn Enter để thoát"
    exit 1
}

# Kiểm tra opencv-python
Write-Host "[1/4] Kiểm tra thư viện Python..." -ForegroundColor Yellow
$opencvCheck = python -c "import cv2; print('OK')" 2>&1
if ($opencvCheck -notmatch "OK") {
    Write-Host "[!] Đang cài đặt opencv-python..." -ForegroundColor Yellow
    pip install opencv-python
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Không thể cài đặt opencv-python!" -ForegroundColor Red
        Read-Host "Nhấn Enter để thoát"
        exit 1
    }
    Write-Host "[OK] Đã cài đặt opencv-python!" -ForegroundColor Green
} else {
    Write-Host "[OK] OpenCV đã sẵn sàng!" -ForegroundColor Green
}

# Mở hộp thoại chọn file
Write-Host ""
Write-Host "[2/4] Mở hộp thoại chọn file..." -ForegroundColor Yellow

$openFileDialog = New-Object System.Windows.Forms.OpenFileDialog
$openFileDialog.Title = "Chọn file video"
$openFileDialog.Filter = "Video Files (*.mp4;*.avi;*.mov;*.mkv;*.webm)|*.mp4;*.avi;*.mov;*.mkv;*.webm|All Files (*.*)|*.*"
$openFileDialog.InitialDirectory = [Environment]::GetFolderPath("MyVideos")

$result = $openFileDialog.ShowDialog()

if ($result -eq [System.Windows.Forms.DialogResult]::OK) {
    $videoPath = $openFileDialog.FileName
    Write-Host "[OK] File đã chọn: $videoPath" -ForegroundColor Green
} else {
    Write-Host "[!] Không có file nào được chọn!" -ForegroundColor Yellow
    Read-Host "Nhấn Enter để thoát"
    exit 0
}

# Lấy thông tin file
$videoFile = Get-Item $videoPath
$videoDir = $videoFile.DirectoryName
$videoName = $videoFile.BaseName
$outputFile = Join-Path $videoDir "$videoName`_info.json"

# Tùy chọn xử lý
Write-Host ""
Write-Host "[3/4] Tùy chọn xử lý" -ForegroundColor Yellow
Write-Host ""
Write-Host "Bạn có muốn extract frames từ video không?"
Write-Host "  1 - Có (extract frames, file JSON sẽ lớn hơn)"
Write-Host "  2 - Không (chỉ lấy metadata, file JSON nhỏ)"
Write-Host ""

$extractChoice = Read-Host "Chọn (1 hoặc 2)"

if ($extractChoice -eq "2") {
    $extractParam = "--no-frames"
    Write-Host "[OK] Chỉ extract metadata" -ForegroundColor Green
} else {
    Write-Host ""
    $frameInterval = Read-Host "Khoảng cách giữa các frames (mặc định 30, Enter để bỏ qua)"
    if ([string]::IsNullOrWhiteSpace($frameInterval)) { $frameInterval = "30" }

    $maxFrames = Read-Host "Số frame tối đa (mặc định 10, Enter để bỏ qua)"
    if ([string]::IsNullOrWhiteSpace($maxFrames)) { $maxFrames = "10" }

    $extractParam = "--interval $frameInterval --max-frames $maxFrames"
    Write-Host "[OK] Sẽ extract frames (interval: $frameInterval, max: $maxFrames)" -ForegroundColor Green
}

# Chạy script Python
Write-Host ""
Write-Host "[4/4] Đang xử lý video..." -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptDir "video_to_json.py"

$arguments = "`"$videoPath`" $extractParam --output `"$outputFile`""
$processInfo = Start-Process -FilePath "python" -ArgumentList "`"$pythonScript`" $arguments" -Wait -NoNewWindow -PassThru

if ($processInfo.ExitCode -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "[SUCCESS] Hoàn thành!" -ForegroundColor Green
    Write-Host ""
    Write-Host "File JSON đã được lưu tại:" -ForegroundColor Cyan
    Write-Host $outputFile -ForegroundColor White
    Write-Host ""

    # Hỏi có muốn mở file JSON không
    $openChoice = Read-Host "Bạn có muốn mở file JSON không? (y/n)"
    if ($openChoice -eq "y" -or $openChoice -eq "Y") {
        Start-Process $outputFile
    }

    # Hỏi có muốn mở thư mục không
    $folderChoice = Read-Host "Bạn có muốn mở thư mục chứa file không? (y/n)"
    if ($folderChoice -eq "y" -or $folderChoice -eq "Y") {
        explorer $videoDir
    }

} else {
    Write-Host ""
    Write-Host "[ERROR] Có lỗi xảy ra khi xử lý video!" -ForegroundColor Red
}

Write-Host ""
Read-Host "Nhấn Enter để thoát"
