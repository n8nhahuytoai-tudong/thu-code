======================================================================
    YOUTUBE TO SORA 2 - HƯỚNG DẪN CHO WINDOWS
======================================================================

🎯 CÁCH SỬ DỤNG NHANH (3 BƯỚC)

Bước 1: CÀI ĐẶT
    → Double-click vào: setup.bat
    → Đợi cài đặt hoàn tất

Bước 2: CHẠY SCRIPT
    Chọn 1 trong 3 cách:

    ✅ CÁCH 1 - ĐƠN GIẢN NHẤT (Khuyến nghị):
        → Double-click: run_youtube_to_sora.bat
        → Nhập YouTube URL
        → Xem kết quả trong folder output_results\

    ✅ CÁCH 2 - CÓ MENU (Nâng cao):
        → Double-click: run_advanced.bat
        → Chọn chức năng từ menu

    ✅ CÁCH 3 - TRỰC TIẾP:
        → Mở Command Prompt
        → Gõ: python youtube_to_sora_advanced.py

Bước 3: XEM KẾT QUẢ
    → Mở folder: output_results\
    → Mở file .txt hoặc .docx mới nhất

======================================================================
    CÁC FILE QUAN TRỌNG
======================================================================

📁 setup.bat
    → Cài đặt tất cả dependencies
    → Chạy file này TRƯỚC KHI SỬ DỤNG LẦN ĐẦU

📁 run_youtube_to_sora.bat
    → Chạy script đơn giản
    → Tự động check dependencies
    → Dễ sử dụng nhất

📁 run_advanced.bat
    → Menu với nhiều tùy chọn
    → Phân tích nhanh/đầy đủ
    → Quản lý cache, xem kết quả

📁 youtube_to_sora_advanced.py
    → Script Python chính
    → Có thể chạy trực tiếp

📁 HUONG_DAN_CHAY.md
    → Hướng dẫn chi tiết đầy đủ
    → Troubleshooting
    → Tùy chỉnh nâng cao

======================================================================
    YÊU CẦU HỆ THỐNG
======================================================================

✅ Python 3.8 trở lên
    → Tải tại: https://www.python.org/downloads/
    → NHỚ CHECK "Add Python to PATH" khi cài!

✅ OpenAI API Key
    → Lấy tại: https://platform.openai.com/api-keys
    → Cần có credit trong account (~$1 cho 1 video 5 phút)

✅ Internet connection
    → Để tải video và gọi API

⚠ ffmpeg (tùy chọn, cho audio analysis)
    → Tải tại: https://ffmpeg.org/download.html
    → Hoặc: choco install ffmpeg

======================================================================
    TROUBLESHOOTING
======================================================================

❌ Lỗi: "Python is not recognized"
    → Cài lại Python và CHECK "Add Python to PATH"
    → Hoặc thêm Python vào PATH thủ công

❌ Lỗi: "pip not found"
    → Chạy: python -m ensurepip
    → Hoặc cài lại Python

❌ Lỗi: "OpenAI API key not found"
    → Chạy setup.bat và nhập API key
    → Hoặc tạo file .env với: OPENAI_API_KEY=sk-your-key

❌ Lỗi: "ffmpeg not found"
    → Cài ffmpeg từ: https://ffmpeg.org/
    → Hoặc BỎ QUA audio analysis (chọn 'n' khi hỏi)

❌ Video không tải được
    → Check internet connection
    → Thử video khác
    → Update yt-dlp: pip install --upgrade yt-dlp

❌ Lỗi API rate limit
    → Đợi 1 phút rồi thử lại
    → Hoặc nâng cấp OpenAI account

======================================================================
    VÍ DỤ SỬ DỤNG
======================================================================

1. Lần đầu tiên sử dụng:
    ✓ Double-click: setup.bat
    ✓ Nhập API key khi được hỏi
    ✓ Đợi cài đặt xong

2. Phân tích video:
    ✓ Double-click: run_youtube_to_sora.bat
    ✓ Nhập URL: https://youtube.com/watch?v=abc123
    ✓ Chọn y cho cache
    ✓ Chọn y cho audio
    ✓ Đợi phân tích xong (2-5 phút)

3. Xem kết quả:
    ✓ Mở folder: output_results\
    ✓ Double-click file .txt hoặc .docx mới nhất
    ✓ Copy Sora prompts và sử dụng!

======================================================================
    KẾT QUẢ BẠN NHẬN ĐƯỢC
======================================================================

✨ File .txt - Report chi tiết:
    - Phân tích tổng thể video
    - Phân tích từng scene (hành động, camera, lighting)
    - Transcript đầy đủ (nếu có audio)
    - 3 phiên bản Sora prompts:
        → Short (50-70 từ)
        → Detailed (120-150 từ)
        → Creative (100-130 từ)

✨ File .json - Data structured:
    - JSON format chuẩn
    - Dễ parse và xử lý
    - Tích hợp vào apps

✨ File .docx - Word document:
    - Format đẹp, dễ đọc
    - Tables, headings
    - Sẵn sàng để chia sẻ

======================================================================
    CHI PHÍ API (DỰ TÍNH)
======================================================================

Video 5 phút, 8 scenes:
    • Vision API (phân tích scenes): ~$0.80
    • Whisper API (transcript):      ~$0.03
    • GPT-4o (tạo prompts):          ~$0.15
    ----------------------------------------
    TỔNG:                            ~$0.98

💡 TIẾT KIỆM với Cache:
    • Lần đầu: ~$0.98
    • Lần sau (từ cache): $0.00 ✅

======================================================================
    LIÊN HỆ & HỖ TRỢ
======================================================================

📖 Xem hướng dẫn đầy đủ: HUONG_DAN_CHAY.md
🐛 Báo lỗi: Mô tả chi tiết lỗi và bước tái hiện
💡 Góp ý: Tính năng mới hoặc cải tiến

======================================================================

                Made with ❤️ for Sora 2 creators
                        Version 2.0 Advanced

======================================================================
