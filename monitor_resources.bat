@echo off
REM ========================================
REM Monitor ComfyUI Resource Usage
REM CPU, GPU, RAM, SSD, Network
REM ========================================

echo.
echo ========================================
echo   ComfyUI Resource Monitor
echo   Press Ctrl+C to stop
echo ========================================
echo.

REM Set Python path
set PYTHON=D:\ComfyUI_windows_portable\ComfyUI\python_embeded\python.exe

REM Check if Python exists
if not exist "%PYTHON%" (
    echo [ERROR] Khong tim thay Python!
    echo Duong dan: %PYTHON%
    pause
    exit /b 1
)

REM Create temporary monitoring script
set MONITOR_SCRIPT=%TEMP%\comfyui_monitor.py

echo import psutil > "%MONITOR_SCRIPT%"
echo import time >> "%MONITOR_SCRIPT%"
echo import os >> "%MONITOR_SCRIPT%"
echo. >> "%MONITOR_SCRIPT%"
echo try: >> "%MONITOR_SCRIPT%"
echo     import torch >> "%MONITOR_SCRIPT%"
echo     GPU_AVAILABLE = torch.cuda.is_available() >> "%MONITOR_SCRIPT%"
echo except: >> "%MONITOR_SCRIPT%"
echo     GPU_AVAILABLE = False >> "%MONITOR_SCRIPT%"
echo. >> "%MONITOR_SCRIPT%"
echo def get_size(bytes): >> "%MONITOR_SCRIPT%"
echo     for unit in ['B', 'KB', 'MB', 'GB', 'TB']: >> "%MONITOR_SCRIPT%"
echo         if bytes ^< 1024.0: >> "%MONITOR_SCRIPT%"
echo             return f"{bytes:.2f} {unit}" >> "%MONITOR_SCRIPT%"
echo         bytes /= 1024.0 >> "%MONITOR_SCRIPT%"
echo. >> "%MONITOR_SCRIPT%"
echo def monitor_loop(): >> "%MONITOR_SCRIPT%"
echo     print("\nMonitoring resources... Press Ctrl+C to stop\n") >> "%MONITOR_SCRIPT%"
echo     while True: >> "%MONITOR_SCRIPT%"
echo         os.system('cls' if os.name == 'nt' else 'clear') >> "%MONITOR_SCRIPT%"
echo         print("="*70) >> "%MONITOR_SCRIPT%"
echo         print("  ComfyUI Resource Monitor - " + time.strftime("%%Y-%%m-%%d %%H:%%M:%%S")) >> "%MONITOR_SCRIPT%"
echo         print("="*70) >> "%MONITOR_SCRIPT%"
echo         print() >> "%MONITOR_SCRIPT%"
echo. >> "%MONITOR_SCRIPT%"
echo         # CPU >> "%MONITOR_SCRIPT%"
echo         cpu_percent = psutil.cpu_percent(interval=1, percpu=False) >> "%MONITOR_SCRIPT%"
echo         cpu_count = psutil.cpu_count() >> "%MONITOR_SCRIPT%"
echo         cpu_freq = psutil.cpu_freq() >> "%MONITOR_SCRIPT%"
echo         print(f"[CPU]") >> "%MONITOR_SCRIPT%"
echo         print(f"  Usage: {cpu_percent:.1f}%%") >> "%MONITOR_SCRIPT%"
echo         print(f"  Cores: {cpu_count}") >> "%MONITOR_SCRIPT%"
echo         if cpu_freq: >> "%MONITOR_SCRIPT%"
echo             print(f"  Frequency: {cpu_freq.current:.0f} MHz") >> "%MONITOR_SCRIPT%"
echo. >> "%MONITOR_SCRIPT%"
echo         # Memory >> "%MONITOR_SCRIPT%"
echo         mem = psutil.virtual_memory() >> "%MONITOR_SCRIPT%"
echo         print(f"\n[RAM]") >> "%MONITOR_SCRIPT%"
echo         print(f"  Total: {get_size(mem.total)}") >> "%MONITOR_SCRIPT%"
echo         print(f"  Used: {get_size(mem.used)} ({mem.percent:.1f}%%)") >> "%MONITOR_SCRIPT%"
echo         print(f"  Available: {get_size(mem.available)}") >> "%MONITOR_SCRIPT%"
echo. >> "%MONITOR_SCRIPT%"
echo         # Swap >> "%MONITOR_SCRIPT%"
echo         swap = psutil.swap_memory() >> "%MONITOR_SCRIPT%"
echo         print(f"\n[SWAP/Page File]") >> "%MONITOR_SCRIPT%"
echo         print(f"  Total: {get_size(swap.total)}") >> "%MONITOR_SCRIPT%"
echo         print(f"  Used: {get_size(swap.used)} ({swap.percent:.1f}%%)") >> "%MONITOR_SCRIPT%"
echo         print(f"  Free: {get_size(swap.free)}") >> "%MONITOR_SCRIPT%"
echo. >> "%MONITOR_SCRIPT%"
echo         # GPU >> "%MONITOR_SCRIPT%"
echo         if GPU_AVAILABLE: >> "%MONITOR_SCRIPT%"
echo             try: >> "%MONITOR_SCRIPT%"
echo                 gpu_name = torch.cuda.get_device_name(0) >> "%MONITOR_SCRIPT%"
echo                 gpu_mem_allocated = torch.cuda.memory_allocated(0) >> "%MONITOR_SCRIPT%"
echo                 gpu_mem_reserved = torch.cuda.memory_reserved(0) >> "%MONITOR_SCRIPT%"
echo                 gpu_mem_total = torch.cuda.get_device_properties(0).total_memory >> "%MONITOR_SCRIPT%"
echo                 gpu_mem_free = gpu_mem_total - gpu_mem_allocated >> "%MONITOR_SCRIPT%"
echo                 gpu_utilization = (gpu_mem_allocated / gpu_mem_total) * 100 >> "%MONITOR_SCRIPT%"
echo. >> "%MONITOR_SCRIPT%"
echo                 print(f"\n[GPU]") >> "%MONITOR_SCRIPT%"
echo                 print(f"  Name: {gpu_name}") >> "%MONITOR_SCRIPT%"
echo                 print(f"  VRAM Total: {get_size(gpu_mem_total)}") >> "%MONITOR_SCRIPT%"
echo                 print(f"  VRAM Used: {get_size(gpu_mem_allocated)} ({gpu_utilization:.1f}%%)") >> "%MONITOR_SCRIPT%"
echo                 print(f"  VRAM Free: {get_size(gpu_mem_free)}") >> "%MONITOR_SCRIPT%"
echo             except Exception as e: >> "%MONITOR_SCRIPT%"
echo                 print(f"\n[GPU] Error: {e}") >> "%MONITOR_SCRIPT%"
echo         else: >> "%MONITOR_SCRIPT%"
echo             print(f"\n[GPU] Not available") >> "%MONITOR_SCRIPT%"
echo. >> "%MONITOR_SCRIPT%"
echo         # Disk >> "%MONITOR_SCRIPT%"
echo         print(f"\n[DISK]") >> "%MONITOR_SCRIPT%"
echo         partitions = psutil.disk_partitions() >> "%MONITOR_SCRIPT%"
echo         for partition in partitions[:3]:  # Show first 3 drives >> "%MONITOR_SCRIPT%"
echo             try: >> "%MONITOR_SCRIPT%"
echo                 usage = psutil.disk_usage(partition.mountpoint) >> "%MONITOR_SCRIPT%"
echo                 print(f"  {partition.device}") >> "%MONITOR_SCRIPT%"
echo                 print(f"    Total: {get_size(usage.total)}, Used: {get_size(usage.used)} ({usage.percent:.1f}%%), Free: {get_size(usage.free)}") >> "%MONITOR_SCRIPT%"
echo             except: >> "%MONITOR_SCRIPT%"
echo                 pass >> "%MONITOR_SCRIPT%"
echo. >> "%MONITOR_SCRIPT%"
echo         # Network >> "%MONITOR_SCRIPT%"
echo         net = psutil.net_io_counters() >> "%MONITOR_SCRIPT%"
echo         print(f"\n[NETWORK]") >> "%MONITOR_SCRIPT%"
echo         print(f"  Sent: {get_size(net.bytes_sent)}") >> "%MONITOR_SCRIPT%"
echo         print(f"  Received: {get_size(net.bytes_recv)}") >> "%MONITOR_SCRIPT%"
echo. >> "%MONITOR_SCRIPT%"
echo         # Processes >> "%MONITOR_SCRIPT%"
echo         print(f"\n[TOP PROCESSES]") >> "%MONITOR_SCRIPT%"
echo         processes = [] >> "%MONITOR_SCRIPT%"
echo         for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']): >> "%MONITOR_SCRIPT%"
echo             try: >> "%MONITOR_SCRIPT%"
echo                 info = proc.info >> "%MONITOR_SCRIPT%"
echo                 if 'python' in info['name'].lower() or 'comfyui' in info['name'].lower(): >> "%MONITOR_SCRIPT%"
echo                     processes.append(info) >> "%MONITOR_SCRIPT%"
echo             except: >> "%MONITOR_SCRIPT%"
echo                 pass >> "%MONITOR_SCRIPT%"
echo         processes = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:5] >> "%MONITOR_SCRIPT%"
echo         for proc in processes: >> "%MONITOR_SCRIPT%"
echo             print(f"  {proc['name'][:20]:20s} - CPU: {proc['cpu_percent']:.1f}%%, MEM: {proc['memory_percent']:.1f}%%") >> "%MONITOR_SCRIPT%"
echo. >> "%MONITOR_SCRIPT%"
echo         print("\n" + "="*70) >> "%MONITOR_SCRIPT%"
echo         print("Press Ctrl+C to stop monitoring") >> "%MONITOR_SCRIPT%"
echo. >> "%MONITOR_SCRIPT%"
echo         time.sleep(2) >> "%MONITOR_SCRIPT%"
echo. >> "%MONITOR_SCRIPT%"
echo if __name__ == '__main__': >> "%MONITOR_SCRIPT%"
echo     try: >> "%MONITOR_SCRIPT%"
echo         monitor_loop() >> "%MONITOR_SCRIPT%"
echo     except KeyboardInterrupt: >> "%MONITOR_SCRIPT%"
echo         print("\n\nMonitoring stopped.") >> "%MONITOR_SCRIPT%"

REM Run monitoring script
echo [INFO] Starting resource monitor...
echo.
"%PYTHON%" "%MONITOR_SCRIPT%"

REM Cleanup
del "%MONITOR_SCRIPT%" >nul 2>&1

pause
