# 🚀 Tự động chạy ComfyUI khi bật máy

Hướng dẫn cấu hình ComfyUI **tự động khởi động** khi bật máy Windows.

---

## ❌ Mặc định: KHÔNG tự động chạy

**Tất cả file `.bat` đều KHÔNG tự động chạy khi bật máy!**

File | Tự động chạy? | Cách chạy
-----|---------------|----------
`start_comfyui_optimized.bat` | ❌ KHÔNG | Double-click thủ công
`start_comfyui_cpu_boost.bat` | ❌ KHÔNG | Double-click thủ công
`run_nvidia_gpu.bat` | ❌ KHÔNG | Double-click thủ công

**Để tự động chạy:** Dùng các script bên dưới! ⬇️

---

## 📦 Các file đã tạo

### 1. **enable_autostart_simple.bat** - Đơn giản (Khuyến nghị)
```
D:\thu-code\enable_autostart_simple.bat
```

**Phương pháp:** Thêm shortcut vào Startup folder

**Ưu điểm:**
- ✅ Đơn giản, dễ setup
- ✅ Không cần quyền Administrator
- ✅ ComfyUI chạy ngay khi đăng nhập
- ✅ Dễ tắt (xóa shortcut)

**Nhược điểm:**
- ⚠️ Không delay được (chạy ngay lập tức)
- ⚠️ Cửa sổ CMD luôn hiển thị

---

### 2. **enable_autostart_advanced.bat** - Nâng cao
```
D:\thu-code\enable_autostart_advanced.bat
```

**Phương pháp:** Tạo Windows Task Scheduler task

**Ưu điểm:**
- ✅ Delay được (chạy sau 30s, 60s, 2 phút)
- ✅ Chạy với quyền cao (Administrator)
- ✅ Cấu hình linh hoạt (trigger, conditions)
- ✅ Có thể chạy ẩn (không hiện cửa sổ)

**Nhược điểm:**
- ⚠️ Cần quyền Administrator
- ⚠️ Phức tạp hơn một chút

---

### 3. **disable_autostart.bat** - Tắt tự động chạy
```
D:\thu-code\disable_autostart.bat
```

**Tác dụng:**
- ✅ Xóa shortcut trong Startup folder
- ✅ Xóa task trong Task Scheduler
- ✅ Kiểm tra các vị trí khác (Registry, System Startup)

---

## 🚀 Hướng dẫn sử dụng

### **Cách 1: Đơn giản (Khuyến nghị cho người mới)**

#### **Bật auto-start:**
```cmd
# Double-click file này
D:\thu-code\enable_autostart_simple.bat

# Chọn Y khi hỏi xác nhận
# Xong! ComfyUI sẽ tự chạy khi bật máy
```

#### **Tắt auto-start:**
```cmd
# Double-click file này
D:\thu-code\disable_autostart.bat
```

**Khi nào dùng:**
- ✅ Bạn muốn ComfyUI chạy ngay khi đăng nhập Windows
- ✅ Không cần delay
- ✅ Muốn setup nhanh (30 giây)

---

### **Cách 2: Nâng cao (Có delay + chạy ẩn)**

#### **Bật auto-start:**
```cmd
# Click phải → Run as Administrator
D:\thu-code\enable_autostart_advanced.bat

# Chọn thời gian delay (khuyến nghị: 30 giây)
# 1. Ngay lập tức
# 2. Sau 30 giây ✅ (Khuyến nghị)
# 3. Sau 60 giây
# 4. Sau 2 phút

# Chọn 2 hoặc 3
# Xong! ComfyUI sẽ tự chạy sau 30s khi bật máy
```

#### **Tắt auto-start:**
```cmd
# Click phải → Run as Administrator
D:\thu-code\disable_autostart.bat
```

**Khi nào dùng:**
- ✅ Bạn muốn máy boot xong hẳn rồi mới chạy ComfyUI
- ✅ Tránh quá tải CPU/RAM khi boot
- ✅ Muốn cấu hình nâng cao

---

## 📊 So sánh 2 phương pháp

| Tiêu chí | Simple (Startup) | Advanced (Task Scheduler) |
|----------|------------------|---------------------------|
| **Dễ setup** | ✅ Rất dễ | ⚠️ Cần Admin |
| **Delay** | ❌ Không có | ✅ 0s / 30s / 60s / 2m |
| **Quyền Admin** | ❌ Không cần | ✅ Cần |
| **Chạy ẩn** | ❌ Luôn hiện cửa sổ | ✅ Có thể ẩn |
| **Dễ tắt** | ✅ Xóa shortcut | ⚠️ Cần xóa task |
| **Khuyến nghị** | Người mới | Người có kinh nghiệm |

---

## 🎯 Hướng dẫn chi tiết từng bước

### **Phương pháp 1: Startup Folder (Đơn giản)**

#### **Bước 1: Chạy enable script**
```cmd
# Đi tới thư mục
cd D:\thu-code

# Double-click hoặc chạy
enable_autostart_simple.bat
```

#### **Bước 2: Xác nhận**
```
Script sẽ hỏi:
- File ComfyUI đã đúng chưa? → Kiểm tra
- Ghi đè shortcut cũ? → Chọn Y (nếu có)
- Mở Startup folder? → Chọn Y (để xem)
```

#### **Bước 3: Xong!**
```
Shortcut "ComfyUI_AutoStart.lnk" đã được tạo
Vị trí: %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
```

#### **Kiểm tra:**
```cmd
# Mở Startup folder thủ công
Win + R → shell:startup → Enter

# Bạn sẽ thấy shortcut "ComfyUI_AutoStart.lnk"
```

---

### **Phương pháp 2: Task Scheduler (Nâng cao)**

#### **Bước 1: Chạy enable script với quyền Admin**
```cmd
# Click phải vào file → Run as Administrator
enable_autostart_advanced.bat
```

#### **Bước 2: Chọn delay time**
```
Script sẽ hỏi:
Ban muon ComfyUI chay sau bao lau khi bat may?
  1. Ngay lap tuc (0 giay)
  2. Sau 30 giay (khuynen nghi)  ← Chọn cái này
  3. Sau 60 giay
  4. Sau 120 giay (2 phut)

Chon (1-4): 2
```

#### **Bước 3: Xác nhận**
```
Task "ComfyUI_AutoStart" sẽ được tạo với:
- Trigger: Khi đăng nhập Windows
- Delay: 30 giây
- Priority: Highest
```

#### **Bước 4: Xong!**
```
Mở Task Scheduler để xem:
Win + R → taskschd.msc → Enter
→ Tìm task "ComfyUI_AutoStart"
```

#### **Kiểm tra:**
```cmd
# Xem danh sách tasks
schtasks /Query /TN "ComfyUI_AutoStart"

# Hoặc mở Task Scheduler GUI
taskschd.msc
```

---

## 🔄 Cách tắt auto-start

### **Cách 1: Dùng disable script (Khuyến nghị)**
```cmd
# Double-click (hoặc Run as Admin nếu dùng Task Scheduler)
D:\thu-code\disable_autostart.bat

# Script sẽ tự động:
# 1. Xóa shortcut trong Startup folder
# 2. Xóa task trong Task Scheduler
# 3. Kiểm tra Registry và các vị trí khác
```

### **Cách 2: Xóa thủ công**

#### **Xóa Startup shortcut:**
```cmd
# Mở Startup folder
Win + R → shell:startup → Enter

# Xóa file "ComfyUI_AutoStart.lnk"
```

#### **Xóa Task Scheduler task:**
```cmd
# Cách 1: Command line
schtasks /Delete /TN "ComfyUI_AutoStart" /F

# Cách 2: GUI
Win + R → taskschd.msc → Enter
→ Tìm task "ComfyUI_AutoStart" → Click phải → Delete
```

---

## ⚙️ Cấu hình nâng cao

### **Thay đổi script được chạy**

Mở file `enable_autostart_simple.bat` hoặc `enable_autostart_advanced.bat`, tìm dòng:
```batch
set COMFYUI_SCRIPT=D:\ComfyUI_windows_portable\start_comfyui_cpu_boost.bat
```

Đổi thành:
```batch
# Dùng script tối ưu thường
set COMFYUI_SCRIPT=D:\ComfyUI_windows_portable\start_comfyui_optimized.bat

# Hoặc dùng script gốc
set COMFYUI_SCRIPT=D:\ComfyUI_windows_portable\run_nvidia_gpu.bat
```

---

### **Thay đổi delay time (Task Scheduler)**

#### **Sau khi tạo task:**
```cmd
# Mở Task Scheduler
taskschd.msc

# Tìm task "ComfyUI_AutoStart"
# Click phải → Properties
# Tab "Triggers" → Edit
# Thay đổi "Delay task for: 30 seconds" → Số khác
# OK → Save
```

#### **Hoặc xóa task và tạo lại:**
```cmd
# Xóa
disable_autostart.bat

# Tạo lại với delay mới
enable_autostart_advanced.bat
```

---

### **Chạy ẩn (không hiện cửa sổ CMD)**

#### **Phương pháp: Tạo VBScript wrapper**

**Bước 1: Tạo file `start_comfyui_hidden.vbs`**
```vbscript
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "D:\ComfyUI_windows_portable\start_comfyui_cpu_boost.bat", 0, False
Set WshShell = Nothing
```

**Bước 2: Sửa enable script để trỏ đến VBScript**
```batch
# Trong enable_autostart_simple.bat hoặc enable_autostart_advanced.bat
set COMFYUI_SCRIPT=D:\ComfyUI_windows_portable\start_comfyui_hidden.vbs
```

**Bước 3: Chạy enable script lại**

**Kết quả:**
- ✅ ComfyUI chạy ngầm, không hiện cửa sổ
- ⚠️ Khó debug nếu có lỗi (không thấy log)
- ℹ️ Xem process trong Task Manager: `python.exe` hoặc `python_embeded.exe`

---

## 🛠️ Troubleshooting

### **Lỗi 1: "Khong tim thay file: D:\ComfyUI_windows_portable\start_comfyui_cpu_boost.bat"**

**Nguyên nhân:** File không tồn tại hoặc đường dẫn sai

**Giải pháp:**
```cmd
# Kiểm tra file có tồn tại không
dir D:\ComfyUI_windows_portable\start_comfyui_cpu_boost.bat

# Nếu không có, copy từ thu-code
copy D:\thu-code\start_comfyui_cpu_boost.bat D:\ComfyUI_windows_portable\

# Hoặc sửa đường dẫn trong enable script
```

---

### **Lỗi 2: "Script nay can chay voi quyen Administrator"**

**Nguyên nhân:** File `enable_autostart_advanced.bat` cần quyền Admin

**Giải pháp:**
```
1. Click phải vào file enable_autostart_advanced.bat
2. Chọn "Run as Administrator"
3. Chạy lại script
```

---

### **Lỗi 3: ComfyUI không chạy sau khi bật máy**

**Kiểm tra:**

**Bước 1: Xác nhận auto-start đã được cấu hình**
```cmd
# Kiểm tra Startup folder
Win + R → shell:startup → Enter
→ Có file "ComfyUI_AutoStart.lnk" không?

# Kiểm tra Task Scheduler
schtasks /Query /TN "ComfyUI_AutoStart"
→ Có task không?
```

**Bước 2: Kiểm tra script có chạy được thủ công không**
```cmd
# Thử chạy thủ công
D:\ComfyUI_windows_portable\start_comfyui_cpu_boost.bat

# Nếu lỗi → Fix lỗi script trước
# Nếu OK → Auto-start chưa được cấu hình đúng
```

**Bước 3: Xem Event Log**
```cmd
# Mở Event Viewer
Win + R → eventvwr.msc → Enter

# Windows Logs → Application
# Tìm lỗi liên quan đến ComfyUI hoặc Python
```

---

### **Lỗi 4: Task Scheduler task không chạy**

**Nguyên nhân phổ biến:**
1. User account không có quyền đăng nhập
2. Script path sai
3. Delay quá ngắn (Windows chưa boot xong)

**Giải pháp:**
```cmd
# Kiểm tra task properties
taskschd.msc
→ Tìm task "ComfyUI_AutoStart"
→ Click phải → Properties

# Tab "General":
# ✅ "Run whether user is logged on or not" → KHÔNG chọn (nếu muốn thấy cửa sổ)
# ✅ "Run with highest privileges" → Chọn

# Tab "Triggers":
# ✅ Delay: 30 seconds hoặc hơn (khuyến nghị)

# Tab "Actions":
# ✅ Program/script: "D:\ComfyUI_windows_portable\start_comfyui_cpu_boost.bat"
# ✅ Start in: "D:\ComfyUI_windows_portable"

# Tab "Conditions":
# ❌ "Start the task only if the computer is on AC power" → BỎ chọn
# ❌ "Stop if the computer switches to battery power" → BỎ chọn

# Tab "Settings":
# ✅ "Allow task to be run on demand" → Chọn
# ✅ "If the task fails, restart every: 1 minute" → Tùy chọn
```

---

## 📊 Kiểm tra auto-start đã hoạt động chưa

### **Test 1: Restart máy**
```
1. Lưu tất cả công việc
2. Restart máy: Shutdown → Restart
3. Đăng nhập Windows
4. Đợi 30-60 giây (nếu có delay)
5. Mở browser → http://127.0.0.1:8188
6. Nếu thấy ComfyUI UI → ✅ Thành công!
```

### **Test 2: Kiểm tra processes**
```cmd
# Mở Task Manager (Ctrl + Shift + Esc)
# Tab "Details"
# Tìm processes:
#   - python.exe
#   - python_embeded.exe
#   - cmd.exe (running start_comfyui_cpu_boost.bat)

# Nếu thấy → ✅ ComfyUI đang chạy
```

### **Test 3: Kiểm tra port**
```cmd
# Kiểm tra port 8188 có đang được dùng không
netstat -ano | findstr :8188

# Nếu có output → ✅ ComfyUI đang chạy
```

---

## ❓ FAQ

### **Q1: ComfyUI có chạy ngầm ở background không?**
❌ **KHÔNG.** Mặc định ComfyUI sẽ mở cửa sổ Command Prompt.

**Muốn chạy ngầm:** Dùng VBScript wrapper (xem phần "Chạy ẩn" ở trên)

---

### **Q2: Tôi có thể tự động tắt ComfyUI khi shutdown không?**
✅ **CÓ.** Windows sẽ tự động tắt khi shutdown.

Không cần cấu hình gì thêm.

---

### **Q3: Delay 30 giây có đủ không?**
✅ **ĐỦ** cho hầu hết máy.

**Khuyến nghị:**
- SSD nhanh, RAM 16GB+: **30 giây** ✅
- HDD hoặc RAM <8GB: **60 giây** hoặc **2 phút**
- Máy chậm: **2 phút**

---

### **Q4: Tôi có thể chạy nhiều scripts cùng lúc không?**
✅ **CÓ**, nhưng không khuyến nghị.

**Ví dụ:**
- Auto-start ComfyUI
- Auto-start Monitor resources
- Auto-start Batch processor

**Cách làm:**
- Tạo nhiều tasks trong Task Scheduler
- Hoặc tạo 1 master script gọi nhiều scripts

---

### **Q5: File .bat có tự chạy khi bật máy không?**
❌ **KHÔNG.** File `.bat` chỉ chạy khi:
1. Double-click thủ công
2. Thêm vào Startup folder (dùng `enable_autostart_simple.bat`)
3. Tạo Task Scheduler (dùng `enable_autostart_advanced.bat`)

---

## 🎯 Tóm tắt nhanh

### **Muốn ComfyUI tự động chạy khi bật máy:**

**Cách đơn giản (30 giây setup):**
```cmd
1. Double-click: enable_autostart_simple.bat
2. Restart máy để test
3. Xong!
```

**Cách nâng cao (có delay):**
```cmd
1. Click phải enable_autostart_advanced.bat → Run as Admin
2. Chọn delay: 30 giây (khuyến nghị)
3. Restart máy để test
4. Xong!
```

### **Muốn TẮT auto-start:**
```cmd
1. Double-click: disable_autostart.bat
2. Xong!
```

---

## 📞 Kết luận

| Tính năng | Trước | Sau |
|-----------|-------|-----|
| Tự động chạy | ❌ Không | ✅ Có (nếu bật) |
| Delay | - | ✅ 0s / 30s / 60s / 2m |
| Dễ setup | - | ✅ 30 giây |
| Dễ tắt | - | ✅ 1 click |

**Các file quan trọng:**
- `enable_autostart_simple.bat` - Bật auto-start (đơn giản)
- `enable_autostart_advanced.bat` - Bật auto-start (nâng cao + delay)
- `disable_autostart.bat` - Tắt auto-start
- `README_AUTOSTART.md` - File này

**Các file liên quan:**
- `start_comfyui_cpu_boost.bat` - Script được tự động chạy
- `start_comfyui_optimized.bat` - Script tối ưu (không CPU boost)
- `monitor_resources.bat` - Monitor tài nguyên
- `batch_process_workflows.py` - Batch processing

---

**✅ Tạo ngày:** 2025-11-12
**✅ Phiên bản:** 1.0
**✅ Cho máy:** Windows + ComfyUI Portable
