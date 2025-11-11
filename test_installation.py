#!/usr/bin/env python3
"""
Script kiểm tra cài đặt
"""

import sys

def test_installation():
    """Kiểm tra tất cả dependencies"""

    print("🔍 Đang kiểm tra cài đặt...\n")

    errors = []

    # Test Python version
    print("1. Python version:")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✓ Python {version.major}.{version.minor}.{version.micro}")
    else:
        print(f"   ✗ Python {version.major}.{version.minor}.{version.micro} (cần >= 3.8)")
        errors.append("Python version quá cũ")

    # Test opencv
    print("\n2. OpenCV (cv2):")
    try:
        import cv2
        print(f"   ✓ opencv-python {cv2.__version__}")
    except ImportError:
        print("   ✗ Chưa cài opencv-python")
        errors.append("opencv-python missing")

    # Test numpy
    print("\n3. NumPy:")
    try:
        import numpy as np
        print(f"   ✓ numpy {np.__version__}")
    except ImportError:
        print("   ✗ Chưa cài numpy")
        errors.append("numpy missing")

    # Test OpenAI
    print("\n4. OpenAI SDK:")
    try:
        import openai
        print(f"   ✓ openai {openai.__version__}")
    except ImportError:
        print("   ✗ Chưa cài openai")
        errors.append("openai missing")

    # Test yt-dlp
    print("\n5. yt-dlp:")
    try:
        import subprocess
        result = subprocess.run(
            ["yt-dlp", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"   ✓ yt-dlp {version}")
        else:
            print("   ✗ yt-dlp không chạy được")
            errors.append("yt-dlp not working")
    except FileNotFoundError:
        print("   ✗ Chưa cài yt-dlp")
        errors.append("yt-dlp missing")
    except Exception as e:
        print(f"   ✗ Lỗi: {e}")
        errors.append(f"yt-dlp error: {e}")

    # Test .env file
    print("\n6. API Key (.env):")
    try:
        from pathlib import Path
        import os

        env_file = Path('.env')
        if env_file.exists():
            # Try to load
            with open(env_file, 'r') as f:
                content = f.read()

            if 'OPENAI_API_KEY' in content and 'sk-' in content:
                print("   ✓ File .env tồn tại và có API key")
            else:
                print("   ⚠ File .env tồn tại nhưng chưa có API key hợp lệ")
                print("     Hãy thêm: OPENAI_API_KEY=sk-your-key")
        else:
            print("   ⚠ Chưa có file .env")
            print("     Tạo file .env và thêm: OPENAI_API_KEY=sk-your-key")
    except Exception as e:
        print(f"   ✗ Lỗi đọc .env: {e}")

    # Summary
    print("\n" + "="*50)
    if not errors:
        print("✓ TẤT CẢ ĐÃ SẴN SÀNG!")
        print("\nBạn có thể chạy:")
        print("  python youtube_scene_by_scene_analyzer.py")
        return True
    else:
        print("✗ CÒN VẤN ĐỀ CẦN SỬA:")
        for i, err in enumerate(errors, 1):
            print(f"  {i}. {err}")

        print("\nCài đặt thiếu dependencies:")
        print("  pip install -r requirements.txt")

        print("\nHoặc:")
        print("  pip install opencv-python numpy openai yt-dlp")
        return False

if __name__ == "__main__":
    success = test_installation()
    sys.exit(0 if success else 1)
