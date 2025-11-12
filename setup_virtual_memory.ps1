# ========================================
# Auto Setup Virtual Memory for ComfyUI
# Optimize SSD as swap when RAM is full
# ========================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Virtual Memory Setup for ComfyUI" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "[ERROR] Script nay can chay voi quyen Administrator!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Cach chay:" -ForegroundColor Yellow
    Write-Host "1. Click phai vao PowerShell" -ForegroundColor Yellow
    Write-Host "2. Chon 'Run as Administrator'" -ForegroundColor Yellow
    Write-Host "3. Chay lai script nay" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

# Get total RAM
Write-Host "[INFO] Dang kiem tra RAM cua may..." -ForegroundColor Green
$totalRAM = (Get-CimInstance Win32_PhysicalMemory | Measure-Object -Property capacity -Sum).Sum / 1GB
$totalRAM = [math]::Round($totalRAM, 2)

Write-Host "[INFO] Tong RAM: $totalRAM GB" -ForegroundColor Green
Write-Host ""

# Calculate optimal page file size
# Initial: 1.5x RAM, Maximum: 3x RAM
$initialSizeMB = [math]::Round($totalRAM * 1.5 * 1024)
$maximumSizeMB = [math]::Round($totalRAM * 3 * 1024)

Write-Host "[INFO] Kich thuoc Page File duoc khuyен nghi:" -ForegroundColor Cyan
Write-Host "  - Initial Size: $initialSizeMB MB ($([math]::Round($initialSizeMB/1024, 2)) GB)" -ForegroundColor Cyan
Write-Host "  - Maximum Size: $maximumSizeMB MB ($([math]::Round($maximumSizeMB/1024, 2)) GB)" -ForegroundColor Cyan
Write-Host ""

# Select drive (prefer SSD)
Write-Host "[INFO] Cac o dia hien co:" -ForegroundColor Yellow
Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Used -ne $null } | ForEach-Object {
    $drive = $_.Name
    $free = [math]::Round($_.Free / 1GB, 2)
    $used = [math]::Round($_.Used / 1GB, 2)
    $total = $free + $used
    Write-Host "  $drive`: Total ${total}GB, Free ${free}GB, Used ${used}GB" -ForegroundColor Yellow
}
Write-Host ""

# Ask user to select drive
$selectedDrive = Read-Host "Chon o dia dat Page File (C, D, E, ...)"
$selectedDrive = $selectedDrive.ToUpper()

# Validate drive
if (-not (Test-Path "${selectedDrive}:\")) {
    Write-Host "[ERROR] O dia ${selectedDrive}: khong ton tai!" -ForegroundColor Red
    pause
    exit 1
}

# Check free space
$drive = Get-PSDrive -Name $selectedDrive
$freeSpaceGB = [math]::Round($drive.Free / 1GB, 2)
$requiredSpaceGB = [math]::Round($maximumSizeMB / 1024, 2)

if ($freeSpaceGB -lt $requiredSpaceGB) {
    Write-Host "[WARNING] O dia ${selectedDrive}: chi con ${freeSpaceGB}GB, can it nhat ${requiredSpaceGB}GB!" -ForegroundColor Red
    $continue = Read-Host "Ban co muon tiep tuc? (y/n)"
    if ($continue -ne "y") {
        exit 0
    }
}

Write-Host ""
Write-Host "[INFO] Dang cau hinh Virtual Memory..." -ForegroundColor Green

try {
    # Disable automatic managed page file
    Write-Host "  - Tat auto-manage page file..." -ForegroundColor Gray
    $cs = Get-WmiObject -Class Win32_ComputerSystem -EnableAllPrivileges
    $cs.AutomaticManagedPagefile = $false
    $cs.Put() | Out-Null

    # Remove existing page file on selected drive
    Write-Host "  - Xoa page file cu (neu co)..." -ForegroundColor Gray
    $existingPF = Get-WmiObject -Class Win32_PageFileSetting -Filter "SettingID='pagefile.sys @ ${selectedDrive}:'"
    if ($existingPF) {
        $existingPF.Delete() | Out-Null
    }

    # Create new page file
    Write-Host "  - Tao page file moi tren ${selectedDrive}:..." -ForegroundColor Gray
    $newPF = Set-WmiInstance -Class Win32_PageFileSetting -Arguments @{
        Name = "${selectedDrive}:\pagefile.sys";
        InitialSize = $initialSizeMB;
        MaximumSize = $maximumSizeMB
    }

    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  THANH CONG!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Cau hinh Virtual Memory:" -ForegroundColor Cyan
    Write-Host "  - O dia: ${selectedDrive}:" -ForegroundColor Cyan
    Write-Host "  - Initial: $initialSizeMB MB ($([math]::Round($initialSizeMB/1024, 2)) GB)" -ForegroundColor Cyan
    Write-Host "  - Maximum: $maximumSizeMB MB ($([math]::Round($maximumSizeMB/1024, 2)) GB)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "[QUAN TRONG] Ban PHAI KHOI DONG LAI MAY de ap dung thay doi!" -ForegroundColor Yellow
    Write-Host ""

    $restart = Read-Host "Ban co muon khoi dong lai bay gio? (y/n)"
    if ($restart -eq "y") {
        Write-Host "Dang khoi dong lai..." -ForegroundColor Green
        Restart-Computer -Force
    }

} catch {
    Write-Host ""
    Write-Host "[ERROR] Loi khi cau hinh Virtual Memory!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Ban co the cau hinh thu cong:" -ForegroundColor Yellow
    Write-Host "1. Win + Pause -> Advanced system settings" -ForegroundColor Yellow
    Write-Host "2. Performance Settings -> Advanced -> Virtual memory -> Change" -ForegroundColor Yellow
    Write-Host "3. Bo tick 'Automatically manage', chon Custom size" -ForegroundColor Yellow
    Write-Host "4. Initial: $initialSizeMB MB, Maximum: $maximumSizeMB MB" -ForegroundColor Yellow
    pause
    exit 1
}

pause
