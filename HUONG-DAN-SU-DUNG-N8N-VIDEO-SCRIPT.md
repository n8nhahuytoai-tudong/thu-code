# 🎬 Hướng Dẫn Sử Dụng Workflow N8N - Viết Kịch Bản Video

## 📋 Mục Lục
1. [Giới thiệu](#giới-thiệu)
2. [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
3. [Cài đặt](#cài-đặt)
4. [Cấu hình](#cấu-hình)
5. [Sử dụng](#sử-dụng)
6. [Tùy chỉnh](#tùy-chỉnh)
7. [Xử lý lỗi](#xử-lý-lỗi)

---

## 🎯 Giới Thiệu

Workflow này giúp bạn tự động hóa việc viết kịch bản video chuyên nghiệp bằng AI. Workflow sử dụng OpenAI GPT-4 để tạo kịch bản hoàn chỉnh với:

- ✅ Hook hấp dẫn
- ✅ Cấu trúc rõ ràng
- ✅ Gợi ý hình ảnh B-roll
- ✅ Timestamp chi tiết
- ✅ Call-to-action mạnh mẽ

**Output**: Kịch bản được lưu dưới 2 định dạng:
- 📄 **JSON** - Để xử lý tự động hoặc tích hợp với hệ thống khác
- 📝 **Markdown** - Để đọc và chỉnh sửa dễ dàng

---

## 🔧 Yêu Cầu Hệ Thống

### Phần mềm cần thiết:
- **n8n** (phiên bản 1.0.0 trở lên)
  - Cài đặt local: `npm install n8n -g`
  - Hoặc sử dụng n8n Cloud: https://n8n.io
- **OpenAI API Key** (GPT-4 hoặc GPT-3.5-turbo)

### Chi phí dự kiến:
- GPT-4 Turbo: ~$0.01 - $0.04 mỗi kịch bản
- GPT-3.5 Turbo: ~$0.001 - $0.002 mỗi kịch bản

---

## 📥 Cài Đặt

### Bước 1: Import Workflow vào n8n

1. Mở n8n trong trình duyệt (thường là `http://localhost:5678`)
2. Click vào **Workflows** trong menu bên trái
3. Click nút **Import from File** hoặc **Import from URL**
4. Chọn file `n8n-video-script-workflow.json`
5. Click **Import**

### Bước 2: Cài đặt Node cần thiết

Workflow sử dụng các node sau (thường đã được cài sẵn):
- Manual Trigger
- Set (để set variables)
- OpenAI (LangChain)
- Convert to File

Nếu thiếu node nào, n8n sẽ tự động yêu cầu cài đặt khi import.

---

## ⚙️ Cấu Hình

### 1. Cấu hình OpenAI API

**Bước 1**: Lấy API Key từ OpenAI
- Truy cập: https://platform.openai.com/api-keys
- Tạo API key mới hoặc sử dụng key hiện có
- Copy API key (bắt đầu bằng `sk-...`)

**Bước 2**: Thêm Credential vào n8n
1. Click vào node **"OpenAI - Generate Script"**
2. Click vào phần **Credential**
3. Chọn **"Create New Credential"**
4. Nhập tên: `OpenAI API`
5. Paste API key vào field **API Key**
6. Click **Save**

**Bước 3**: Chọn Model
- Mặc định: `gpt-4-turbo-preview` (tốt nhất, đắt hơn)
- Tiết kiệm: `gpt-3.5-turbo` (nhanh, rẻ hơn)
- Nâng cao: `gpt-4` (cân bằng)

### 2. Cấu hình Parameters (Tùy chọn)

Mở node **"Set Video Parameters"** để chỉnh sửa giá trị mặc định:

```javascript
{
  "video_topic": "Hướng dẫn sử dụng AI trong công việc hàng ngày",
  "video_duration": "5-7 phút",
  "target_audience": "Người làm việc văn phòng, độ tuổi 25-45",
  "video_style": "Giáo dục, thân thiện, dễ hiểu",
  "key_points": "3-5 điểm chính cần truyền tải"
}
```

---

## 🚀 Sử Dụng

### Cách 1: Chạy với Parameters Mặc Định

1. Click vào node **"Manual Trigger"**
2. Click nút **"Execute Node"** hoặc **"Test Workflow"**
3. Chờ 20-60 giây để AI tạo kịch bản
4. Kết quả sẽ xuất hiện ở node cuối cùng **"Summary Report"**

### Cách 2: Tùy Chỉnh Parameters Trước Khi Chạy

1. Click vào node **"Set Video Parameters"**
2. Chỉnh sửa các giá trị trong **Values**:
   - `video_topic`: Chủ đề video của bạn
   - `video_duration`: Thời lượng mong muốn (VD: "3-5 phút", "10 phút")
   - `target_audience`: Đối tượng mục tiêu (VD: "Sinh viên đại học", "Doanh nhân trẻ")
   - `video_style`: Phong cách video (VD: "Hài hước", "Chuyên nghiệp", "Cảm động")
   - `key_points`: Số điểm chính muốn truyền tải

3. Save và Execute workflow

### Cách 3: Tích Hợp Với Webhook (Nâng Cao)

Để gọi workflow từ ứng dụng khác:

1. Thay thế node **"Manual Trigger"** bằng **"Webhook"**
2. Cấu hình Webhook với HTTP Method: `POST`
3. Gửi request với body:

```json
{
  "topic": "Cách tạo nội dung viral trên TikTok",
  "duration": "60 giây",
  "audience": "Gen Z, 16-25 tuổi",
  "style": "Năng động, trending",
  "key_points": "5 tips nhanh"
}
```

---

## 🎨 Tùy Chỉnh

### 1. Thay Đổi Prompt AI

Mở node **"Build AI Prompt"** và chỉnh sửa nội dung prompt:

```markdown
Bạn là một chuyên gia viết kịch bản video...

[Tùy chỉnh prompt theo ý bạn]

Ví dụ:
- Thêm yêu cầu về tone giọng cụ thể
- Thêm format đặc biệt (như script cho TikTok, YouTube Shorts)
- Thêm yêu cầu về SEO keywords
- Thêm phần script cho thumbnail, title
```

### 2. Thêm Output Format Khác

Bạn có thể thêm các node để export sang:
- **PDF**: Dùng node "HTML to PDF"
- **Google Docs**: Dùng node "Google Drive"
- **Notion**: Dùng node "Notion"
- **Slack/Discord**: Gửi thông báo khi hoàn thành

### 3. Điều Chỉnh AI Temperature

Trong node **"OpenAI - Generate Script"**, phần **Options**:
- `temperature`: 0.3-0.5 = Bảo thủ, nhất quán
- `temperature`: 0.7-0.9 = Sáng tạo, đa dạng
- `maxTokens`: 2000-8000 (tùy độ dài kịch bản)

### 4. Thêm Ngôn Ngữ Khác

Workflow hỗ trợ đa ngôn ngữ! Chỉ cần:
1. Thay đổi prompt trong node **"Build AI Prompt"** sang ngôn ngữ bạn muốn
2. Hoặc thêm field `language` trong parameters:

```javascript
{
  "language": "English" // hoặc "中文", "日本語", etc.
}
```

---

## 🔍 Ví Dụ Output

### Ví dụ kịch bản được tạo:

```markdown
# KỊCH BẢN VIDEO: Hướng dẫn sử dụng AI trong công việc hàng ngày

## 🎣 HOOK [00:00 - 00:15]
**On Screen**: "Bạn có biết AI có thể giúp bạn tiết kiệm 10 giờ mỗi tuần?"
**Voiceover**: "Nếu bạn vẫn đang làm việc theo cách cũ, bạn đang lãng phí
rất nhiều thời gian. Hôm nay tôi sẽ chỉ cho bạn 5 cách sử dụng AI để tăng
năng suất gấp đôi!"
**B-roll**: Montage người làm việc stress, sau đó thoải mái với AI

## 📖 GIỚI THIỆU [00:15 - 00:45]
...

## 💡 NỘI DUNG CHÍNH

### Phần 1: Tự động hóa Email [00:45 - 02:00]
...

[Tiếp tục các phần khác]
```

---

## 🐛 Xử Lý Lỗi

### Lỗi thường gặp:

#### 1. **Lỗi "OpenAI API Key invalid"**
**Nguyên nhân**: API key không đúng hoặc đã hết hạn
**Giải pháp**:
- Kiểm tra API key tại https://platform.openai.com/api-keys
- Tạo key mới và cập nhật trong n8n credentials
- Đảm bảo tài khoản OpenAI có credits

#### 2. **Lỗi "Rate limit exceeded"**
**Nguyên nhân**: Gọi API quá nhiều lần trong thời gian ngắn
**Giải pháp**:
- Chờ vài phút rồi thử lại
- Nâng cấp plan OpenAI để có rate limit cao hơn
- Thêm node "Wait" giữa các lần gọi

#### 3. **Lỗi "Workflow timeout"**
**Nguyên nhân**: AI mất quá nhiều thời gian tạo kịch bản
**Giải pháp**:
- Tăng timeout trong Settings > Workflow Settings
- Giảm `maxTokens` xuống (ví dụ: 2000 thay vì 4000)
- Rút ngắn prompt

#### 4. **Kịch bản không đúng format**
**Nguyên nhân**: AI không hiểu rõ yêu cầu
**Giải pháp**:
- Chỉnh sửa prompt rõ ràng hơn trong node "Build AI Prompt"
- Thêm ví dụ cụ thể vào prompt
- Tăng temperature lên 0.8-0.9 để AI sáng tạo hơn

---

## 📊 Tips & Best Practices

### 1. **Viết Prompt Tốt**
- Cụ thể: "Video 5 phút về marketing" thay vì "Video về marketing"
- Có ví dụ: Cung cấp mẫu kịch bản bạn thích
- Có context: "Cho kênh YouTube 100K subs" vs "Cho kênh mới"

### 2. **Tối Ưu Chi Phí**
- Dùng GPT-3.5-turbo cho draft đầu tiên
- Dùng GPT-4 cho phiên bản cuối cùng
- Giới hạn maxTokens phù hợp với độ dài video

### 3. **Quy Trình Làm Việc Hiệu Quả**
1. Chạy workflow tạo 3-5 phiên bản kịch bản
2. Chọn phiên bản tốt nhất
3. Chỉnh sửa thủ công các chi tiết
4. Review với team
5. Finalize và bắt đầu sản xuất

### 4. **Version Control**
- Lưu các phiên bản kịch bản với timestamp
- Đặt tên file rõ ràng: `video-script-topic-v1-2025-11-07.md`
- Backup vào Google Drive hoặc Dropbox

---

## 🔗 Tài Nguyên Bổ Sung

### Tài liệu:
- [n8n Documentation](https://docs.n8n.io/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Video Script Writing Guide](https://www.hubspot.com/video-marketing)

### Community:
- [n8n Community Forum](https://community.n8n.io/)
- [n8n Discord](https://discord.gg/n8n)

### Video Tutorials:
- [n8n YouTube Channel](https://www.youtube.com/@n8n-io)
- [AI Video Production Tutorials](https://www.youtube.com/results?search_query=ai+video+production)

---

## 📞 Hỗ Trợ

Nếu bạn gặp vấn đề:
1. Kiểm tra phần [Xử Lý Lỗi](#xử-lý-lỗi) ở trên
2. Tham gia n8n Community để hỏi
3. Mở issue trên GitHub repository này

---

## 📝 License

MIT License - Tự do sử dụng và chỉnh sửa theo nhu cầu của bạn.

---

**Chúc bạn tạo được những kịch bản video tuyệt vời! 🎬✨**
