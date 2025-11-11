================================================================
    YOUTUBE TO WORD - SORA PROMPTS EXPORTER
    Moi canh = Mieu ta 7 muc + 1 dong prompt sieu chi tiet
================================================================

GIOI THIEU:
-----------
Tool phan tich video YouTube va xuat ra:
- Mieu ta chi tiet 7 muc bang tieng Viet cho moi canh
- Prompt 1 dong sieu chi tiet (250-350 words) bang tieng Anh
- File Word (.docx) voi anh nhung san
- 2 folder anh rieng: FIRST va LAST (danh so tu 0)
- Transcript audio (neu co)

YEU CAU HE THONG:
-----------------
- Python 3.8 tro len
- OpenAI API Key (de dung GPT-4o Vision va Whisper)
- Ket noi Internet
- Windows: Chay file .bat
- Linux/Mac: Chay truc tiep python script

CAI DAT:
--------

WINDOWS (CUC DE):
-----------------
1. Giai nen file ZIP nay
2. Double-click INSTALL.bat
   -> Se tu dong cai dat tat ca dependencies
3. Nhap OpenAI API Key khi duoc hoi
   -> Se tu dong tao file .env

4. Double-click RUN_WORD_EXPORT.bat de chay!


LINUX/MAC:
----------
1. Giai nen ZIP:
   unzip youtube_to_word_export.zip
   cd youtube_to_word_export

2. Cai dat dependencies:
   pip install -r requirements.txt

3. Tao file .env voi API key:
   echo "OPENAI_API_KEY=sk-your-api-key-here" > .env

4. Chay script:
   python youtube_to_word_prompts.py


SU DUNG:
--------
1. Chay RUN_WORD_EXPORT.bat (Windows) hoac python youtube_to_word_prompts.py
2. Nhap YouTube URL
3. Cho xu ly (co the mat vai phut tuy theo video)
4. Ket qua xuat ra folder: output_scenes/


KET QUA OUTPUT:
---------------
output_scenes/
├── [Video_Name]_PROMPTS.txt         (File text)
├── [Video_Name]_PROMPTS.docx        (File Word co anh)
├── [Video_Name]_FIRST/              (Folder anh dau)
│   ├── 0.jpg
│   ├── 1.jpg
│   └── ...
└── [Video_Name]_LAST/               (Folder anh cuoi)
    ├── 0.jpg
    ├── 1.jpg
    └── ...


CAU TRUC MOI CANH:
------------------
SCENE 1 (5.2s | 0.0s - 5.2s)
----------------------------------------

[Anh dau]
[Anh cuoi]

MO TA CHI TIET (7 MUC):
1. **Hanh dong**: [Mo ta hanh dong chinh]
2. **Nhan vat/Doi tuong**: [Mo ta nhan vat, vat the]
3. **Cam xuc**: [Mo ta khong khi cam xuc]
4. **Boi canh**: [Mo ta boi canh, moi truong]
5. **Camera**: [Mo ta camera, goc chup]
6. **Anh sang**: [Mo ta anh sang, mau sac]
7. **Composition**: [Mo ta bo cuc khung hinh]

PROMPT (1 DONG):
[250-350 words prompt sieu chi tiet bang tieng Anh, chua tat ca 8 yeu to: camera specs, characters, animals, lighting, environment, sound design, action, style reference]


FILES TRONG ZIP:
----------------
✅ youtube_to_word_prompts.py   - Script Python chinh
✅ RUN_WORD_EXPORT.bat          - Launcher Windows
✅ INSTALL.bat                  - Auto-installer Windows
✅ TEST.bat                     - Test batch file syntax
✅ requirements.txt             - Python dependencies
✅ .env.example                 - Template API key
✅ YOUTUBE_TO_WORD_README.txt   - File huong dan nay


DEPENDENCIES (tu dong cai boi INSTALL.bat):
-------------------------------------------
- opencv-python>=4.8.0          (Scene detection)
- numpy>=1.24.0                 (Image processing)
- openai>=1.12.0                (GPT-4o Vision + Whisper API)
- yt-dlp>=2024.1.0              (YouTube download)
- python-docx>=1.1.0            (Word export)


TINH NANG:
----------
✅ Phat hien canh tu dong (OpenCV)
✅ Phan tich 7 muc cho moi canh (tieng Viet)
✅ Tao prompt sieu chi tiet 1 dong (250-350 words, tieng Anh)
✅ Xuat Word co anh nhung
✅ Transcript audio (Whisper API)
✅ 2 folder anh rieng (FIRST + LAST)
✅ Retry 5 lan neu API loi
✅ Kiem tra prompt qua ngan


XU LY LOI:
----------
- Neu API loi, script se tu dong retry 5 lan
- Neu canh nao loi, se hien thi ro rang "[ERROR] Failed to analyze..."
- Neu prompt qua ngan, se canh bao "[WARNING: Short prompt...]"


CHI PHI API:
------------
Tool su dung OpenAI API:
- GPT-4o Vision: ~$0.01 per scene (2 API calls)
- Whisper: ~$0.006 per minute audio
- Video 5 phut, 20 canh: ~$0.25 USD


HO TRO:
-------
- GitHub: https://github.com/n8nhahuytoai-tudong/thu-code
- Branch: claude/write-content-011CV1JeX9QX12CT5UswAVpz


PHIEN BAN:
----------
Version: 2.0
Date: 2025-11-11
Update: Add 7-point description + separate image folders

================================================================
