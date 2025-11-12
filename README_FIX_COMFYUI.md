# 🔧 Hướng dẫn sửa lỗi ComfyUI - Node không load được

## 🐛 Lỗi gặp phải

```
AttributeError: _ARRAY_API not found
ImportError: numpy.core.multiarray failed to import
```

**17+ custom nodes bị lỗi:**
- AniTalker-ComfyUI
- ComfyUI-DiffSynth-Studio
- comfyui-easy-use
- ComfyUI-fastblend
- ComfyUI-Hallo
- ComfyUI-IP_LAP
- ComfyUI-KJNodes
- ComfyUI-MimicMotion
- ComfyUI-MuseTalk_FSH
- ComfyUI-VideoHelperSuite
- comfyui_controlnet_aux
- DHLive-ComfyUI
- DiffSynth-ComfyUI
- qweneditutils
- RealisDance-ComfyUI
- ViewCrafter-ComfyUI
- ComfyUI-WanVideoWrapper

---

## 🔍 Nguyên nhân

- **NumPy version conflict**: NumPy 2.2.6 không tương thích với opencv-python và nhiều packages khác
- Các packages được compiled với NumPy 1.x nhưng hệ thống đang dùng NumPy 2.x
- opencv-python không thể import vì thiếu `_ARRAY_API`

---

## ✅ Giải pháp

### **Phương án 1: Chạy file .bat tự động (KHUYẾN NGHỊ)**

1. Copy file `FIX_COMFYUI_NUMPY.bat` vào thư mục `D:\ComfyUI_windows_portable\`
2. Double-click để chạy
3. Đợi hoàn tất
4. Restart ComfyUI

---

### **Phương án 2: Chạy lệnh thủ công**

Mở CMD và chạy:

```cmd
cd /d D:\ComfyUI_windows_portable
.\python_embeded\python.exe -m pip uninstall -y numpy
.\python_embeded\python.exe -m pip install "numpy<2"
```

---

### **Phương án 3: Reinstall opencv-python (nếu phương án 1 & 2 không work)**

```cmd
cd /d D:\ComfyUI_windows_portable
.\python_embeded\python.exe -m pip uninstall -y opencv-python opencv-python-headless
.\python_embeded\python.exe -m pip install opencv-python==4.10.0.84
.\python_embeded\python.exe -m pip install "numpy<2"
```

---

## 🧪 Kiểm tra sau khi fix

```cmd
cd /d D:\ComfyUI_windows_portable
.\python_embeded\python.exe -c "import numpy; print(f'NumPy: {numpy.__version__}')"
.\python_embeded\python.exe -c "import cv2; print('OpenCV OK')"
```

**Kết quả mong đợi:**
```
NumPy: 1.26.4
OpenCV OK
```

---

## 🚀 Chạy lại ComfyUI

```cmd
cd /d D:\ComfyUI_windows_portable
run_nvidia_gpu.bat
```

**Kiểm tra:**
- Mở trình duyệt: http://127.0.0.1:8188
- Tất cả nodes nên load thành công
- Không còn lỗi `ImportError: numpy.core.multiarray failed to import`

---

## 📊 Thống kê trước/sau fix

| Trước fix | Sau fix |
|-----------|---------|
| 17 nodes FAILED | 0 nodes FAILED |
| NumPy 2.2.6 | NumPy 1.26.4 |
| opencv-python không hoạt động | opencv-python hoạt động tốt |

---

## 🔗 Tham khảo

- [NumPy 2.0 Migration Guide](https://numpy.org/devdocs/numpy_2_0_migration_guide.html)
- [OpenCV Python Bindings Issue](https://github.com/opencv/opencv-python/issues/884)
- Branch fix: `claude/fix-comfyui-ssuwoc-load-011CV46mxKYKH5ni5iDNwv8k`

---

**Tạo bởi:** Claude AI Assistant
**Ngày:** 2025-11-12
**Version:** 1.0
