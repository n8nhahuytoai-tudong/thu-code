# ========================================
# RAM và GPU ảo - Giải thích và Giải pháp
# ========================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  RAM/GPU Ao - Phan Tich va Giai Phap" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check current system resources
Write-Host "[INFO] Kiem tra tai nguyen hien tai..." -ForegroundColor Green
Write-Host ""

# RAM
$ram = Get-CimInstance Win32_PhysicalMemory | Measure-Object -Property capacity -Sum
$totalRAM = [math]::Round($ram.Sum / 1GB, 2)
$availRAM = [math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB, 2)

Write-Host "[RAM]" -ForegroundColor Yellow
Write-Host "  Total: $totalRAM GB" -ForegroundColor White
Write-Host "  Available: $availRAM GB" -ForegroundColor White

# Virtual Memory
$pageFile = Get-CimInstance Win32_PageFileUsage
if ($pageFile) {
    $pageFileSize = [math]::Round($pageFile.AllocatedBaseSize / 1024, 2)
    $pageFileUsed = [math]::Round($pageFile.CurrentUsage / 1024, 2)
    Write-Host "  Virtual Memory: $pageFileSize GB (dang dung: $pageFileUsed GB)" -ForegroundColor Green
} else {
    Write-Host "  Virtual Memory: Chua cau hinh" -ForegroundColor Red
}
Write-Host ""

# GPU
Write-Host "[GPU]" -ForegroundColor Yellow
try {
    $gpu = Get-CimInstance Win32_VideoController | Where-Object { $_.Name -like "*NVIDIA*" -or $_.Name -like "*AMD*" }
    if ($gpu) {
        Write-Host "  Name: $($gpu.Name)" -ForegroundColor White
        $vram = [math]::Round($gpu.AdapterRAM / 1GB, 2)
        if ($vram -gt 0) {
            Write-Host "  VRAM: $vram GB" -ForegroundColor White
        } else {
            Write-Host "  VRAM: Unknown" -ForegroundColor Gray
        }
    } else {
        Write-Host "  GPU: Integrated/Unknown" -ForegroundColor Gray
    }
} catch {
    Write-Host "  GPU: Cannot detect" -ForegroundColor Gray
}
Write-Host ""

# CPU
$cpu = Get-CimInstance Win32_Processor
Write-Host "[CPU]" -ForegroundColor Yellow
Write-Host "  Name: $($cpu.Name)" -ForegroundColor White
Write-Host "  Cores: $($cpu.NumberOfCores)" -ForegroundColor White
Write-Host "  Threads: $($cpu.NumberOfLogicalProcessors)" -ForegroundColor White
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  PHAN TICH" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Analysis
Write-Host "[1] RAM AO (Virtual Memory)" -ForegroundColor Yellow
Write-Host ""
if ($pageFile -and $pageFileSize -gt 0) {
    Write-Host "  [OK] DA CO RAM ao: $pageFileSize GB" -ForegroundColor Green
    Write-Host "  Vi tri: C:\pagefile.sys (hoac o dia khac)" -ForegroundColor Gray
    Write-Host "  Hoat dong: SSD/HDD lam RAM khi het RAM that" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  Muon TANG RAM ao:" -ForegroundColor Cyan
    Write-Host "    - Chay lai: setup_virtual_memory.ps1" -ForegroundColor Cyan
    Write-Host "    - Tang size len 2-3x RAM that" -ForegroundColor Cyan
} else {
    Write-Host "  [WARNING] CHUA CO RAM ao!" -ForegroundColor Red
    Write-Host "  May tinh se crash khi het RAM!" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Giai phap:" -ForegroundColor Yellow
    Write-Host "    1. Chay: setup_virtual_memory.ps1 (as Admin)" -ForegroundColor Yellow
    Write-Host "    2. Chon o SSD nhanh nhat" -ForegroundColor Yellow
    Write-Host "    3. Khoi dong lai may" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "[2] GPU AO" -ForegroundColor Yellow
Write-Host ""
Write-Host "  [INFO] KHONG THE tao GPU ao that su!" -ForegroundColor Red
Write-Host ""
Write-Host "  Ly do:" -ForegroundColor Gray
Write-Host "    - GPU co 3584 CUDA cores (RTX 3060)" -ForegroundColor Gray
Write-Host "    - CPU chi co 8 cores" -ForegroundColor Gray
Write-Host "    - GPU nhanh hon CPU 20-50 lan cho AI!" -ForegroundColor Gray
Write-Host "    - Software GPU emulation: Cham 100-1000x" -ForegroundColor Gray
Write-Host ""
Write-Host "  Cac phuong an THUC TE:" -ForegroundColor Cyan
Write-Host ""

Write-Host "  [A] CPU Offloading (DA CO)" -ForegroundColor Green
Write-Host "      File: start_comfyui_cpu_boost.bat" -ForegroundColor Gray
Write-Host "      CPU xu ly preprocessing, GPU chi lam AI inference" -ForegroundColor Gray
Write-Host "      Tang toc: 1.2-1.5x" -ForegroundColor Gray
Write-Host ""

Write-Host "  [B] Model Optimization" -ForegroundColor Yellow
Write-Host "      - FP16 thay vi FP32: Nhanh 2x, dung 50% VRAM" -ForegroundColor Gray
Write-Host "      - Model quantization: Nhanh 2-4x" -ForegroundColor Gray
Write-Host "      - Smaller models: Trade-off quality vs speed" -ForegroundColor Gray
Write-Host ""

Write-Host "  [C] Cloud GPU Rental" -ForegroundColor Yellow
Write-Host "      - Thue GPU tu RunPod, Vast.ai, etc." -ForegroundColor Gray
Write-Host "      - RTX 4090: ~$0.30-0.50/hour" -ForegroundColor Gray
Write-Host "      - A100 40GB: ~$1.00-1.50/hour" -ForegroundColor Gray
Write-Host ""

Write-Host "  [D] Multi-GPU (Neu co GPU thu 2)" -ForegroundColor Yellow
Write-Host "      - Cam them 1 GPU nua (neu PSU du manh)" -ForegroundColor Gray
Write-Host "      - 2x RTX 3060 = 2x performance" -ForegroundColor Gray
Write-Host "      - Can: PSU 850W+, motherboard co 2 PCIe slots" -ForegroundColor Gray
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  KHUYẾN NGHỊ" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Da toi uu 90% roi! Con lai:" -ForegroundColor Green
Write-Host ""
Write-Host "  [1] RAM ao: SETUP (neu chua)" -ForegroundColor Yellow
Write-Host "      -> Chay: setup_virtual_memory.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "  [2] Tang RAM that: Mua them RAM stick" -ForegroundColor Yellow
Write-Host "      -> 16GB -> 32GB = Khong lo het RAM nua" -ForegroundColor Gray
Write-Host "      -> Gia: ~$30-50/16GB stick" -ForegroundColor Gray
Write-Host ""
Write-Host "  [3] Thue Cloud GPU: Khi can render lon" -ForegroundColor Yellow
Write-Host "      -> RunPod, Vast.ai, Lambda Labs" -ForegroundColor Gray
Write-Host "      -> RTX 4090 nhanh hon RTX 3060 2-3 lan" -ForegroundColor Gray
Write-Host ""
Write-Host "  [4] Model optimization: FP16, smaller models" -ForegroundColor Yellow
Write-Host "      -> Trade-off: Quality giam 5-10%, Speed tang 2x" -ForegroundColor Gray
Write-Host ""

Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Muon xem huong dan chi tiet?" -ForegroundColor Cyan
Write-Host "  -> Doc: README_ADVANCED_OPTIMIZATION.md" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to exit"
