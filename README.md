# 🎬 N8N Video Script Generator

> Tự động hóa việc viết kịch bản video chuyên nghiệp bằng AI

[![n8n](https://img.shields.io/badge/n8n-1.0+-brightgreen)](https://n8n.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-blue)](https://openai.com)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 📖 Giới Thiệu

Bộ workflow n8n này giúp bạn tạo kịch bản video hoàn chỉnh chỉ trong vài phút bằng cách sử dụng AI (OpenAI GPT-4). Workflow được thiết kế cho:

- 📺 **YouTubers** - Tạo kịch bản cho video dài
- 📱 **Content Creators** - Kịch bản cho TikTok, Reels, Shorts
- 🎓 **Educators** - Kịch bản video giáo dục
- 💼 **Marketers** - Video marketing, ads
- 🎥 **Video Production Teams** - Streamline script writing process

## ✨ Tính Năng

### Phiên Bản Cơ Bản (`n8n-video-script-workflow.json`)
- ✅ Manual trigger - Chạy workflow khi cần
- ✅ Tùy chỉnh parameters (chủ đề, thời lượng, audience, style)
- ✅ AI-powered script generation với OpenAI GPT-4
- ✅ Export ra JSON và Markdown
- ✅ Báo cáo tóm tắt chi tiết

### Phiên Bản Nâng Cao (`n8n-video-script-advanced.json`)
- 🚀 **Webhook API** - Gọi từ ứng dụng khác
- 🚀 **Multi-platform optimization** - YouTube, TikTok, Instagram, v.v.
- 🚀 **Quality scoring** - Tự động đánh giá chất lượng script
- 🚀 **Smart routing** - Khác nhau giữa long-form và short-form
- 🚀 **SEO optimization** - Tích hợp keywords và metadata
- 🚀 **Multi-language support** - Hỗ trợ nhiều ngôn ngữ

## 📦 Cấu Trúc Files

```
.
├── README.md                                    # File này
├── HUONG-DAN-SU-DUNG-N8N-VIDEO-SCRIPT.md       # Hướng dẫn chi tiết
├── n8n-video-script-workflow.json              # Workflow cơ bản
├── n8n-video-script-advanced.json              # Workflow nâng cao
└── examples/
    ├── example-request.json                     # Ví dụ API request
    ├── example-script-youtube.md                # Ví dụ kịch bản YouTube
    └── example-script-tiktok.md                 # Ví dụ kịch bản TikTok
```

## 🚀 Quick Start

### 1. Cài Đặt n8n

**Option A: Local Installation**
```bash
npm install n8n -g
n8n start
```

**Option B: Docker**
```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

**Option C: n8n Cloud**
Đăng ký tại: https://n8n.io/cloud

### 2. Import Workflow

1. Mở n8n (http://localhost:5678)
2. Click **"Workflows"** → **"Import from File"**
3. Chọn `n8n-video-script-workflow.json` (hoặc phiên bản advanced)
4. Click **"Import"**

### 3. Cấu Hình OpenAI API

1. Lấy API key từ: https://platform.openai.com/api-keys
2. Trong n8n, click vào node **"OpenAI - Generate Script"**
3. Thêm credential mới với API key
4. Save

### 4. Chạy Workflow

**Phiên bản cơ bản:**
- Click node "Manual Trigger"
- Click "Execute Node"
- Chờ kết quả

**Phiên bản advanced (API):**
```bash
curl -X POST http://localhost:5678/webhook/video-script-generator \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Hướng dẫn sử dụng ChatGPT hiệu quả",
    "duration": "10 phút",
    "platform": "YouTube",
    "audience": "Người mới bắt đầu",
    "style": "Giáo dục, thân thiện"
  }'
```

## 📚 Documentation

- [Hướng Dẫn Chi Tiết](HUONG-DAN-SU-DUNG-N8N-VIDEO-SCRIPT.md) - Đọc đầu tiên!
- [Examples & Templates](examples/) - Ví dụ và mẫu sử dụng
- [n8n Documentation](https://docs.n8n.io/)
- [OpenAI API Docs](https://platform.openai.com/docs/)

## 💡 Use Cases

### 1. YouTube Video Scripts
```json
{
  "topic": "10 Thủ Thuật Excel Tiết Kiệm Thời Gian",
  "duration": "8-10 phút",
  "platform": "YouTube",
  "audience": "Dân văn phòng, 25-45 tuổi",
  "style": "Practical, step-by-step tutorial",
  "include_seo": true
}
```

### 2. TikTok/Shorts Scripts
```json
{
  "topic": "3 Cách Làm Đẹp Da Tự Nhiên",
  "duration": "60 giây",
  "platform": "TikTok",
  "audience": "Gen Z, nữ 18-25",
  "style": "Trendy, fast-paced, visual-heavy",
  "tone": "Vui vẻ, năng động"
}
```

### 3. Educational Content
```json
{
  "topic": "Lịch Sử Chiến Tranh Thế Giới Thứ 2",
  "duration": "15 phút",
  "platform": "YouTube",
  "audience": "Học sinh THPT, người yêu lịch sử",
  "style": "Documentary style, serious tone",
  "include_seo": true
}
```

### 4. Product Review
```json
{
  "topic": "Review iPhone 15 Pro Max Sau 30 Ngày Sử Dụng",
  "duration": "12 phút",
  "platform": "YouTube",
  "audience": "Tech enthusiasts, 20-40 tuổi",
  "style": "Honest, detailed, pros & cons",
  "tone": "Professional yet friendly"
}
```

## 🎨 Tùy Chỉnh

### Thay Đổi AI Model

Trong node OpenAI, bạn có thể chọn:
- `gpt-4-turbo-preview` - Tốt nhất, đắt nhất (~$0.01-0.04/script)
- `gpt-4` - Cân bằng (~$0.03-0.06/script)
- `gpt-3.5-turbo` - Nhanh, rẻ (~$0.001-0.002/script)

### Điều Chỉnh AI Temperature

```javascript
// Conservative (consistent, predictable)
temperature: 0.3

// Balanced (recommended)
temperature: 0.7

// Creative (varied, surprising)
temperature: 0.9
```

### Thêm Custom Prompts

Chỉnh sửa node **"Build AI Prompt"** để thêm requirements đặc biệt:
- Brand voice guidelines
- Specific formats
- Industry-specific terminology
- Legal disclaimers

## 🔌 Integrations

Workflow có thể tích hợp với:

### Lưu Trữ
- 📁 **Google Drive** - Tự động save scripts
- 📝 **Notion** - Sync vào Notion database
- ☁️ **Dropbox** - Backup cloud

### Thông Báo
- 💬 **Slack** - Thông báo khi script ready
- 📧 **Email** - Gửi script qua email
- 📱 **Discord** - Post vào Discord channel

### Project Management
- ✅ **Trello** - Tạo card với script
- 📊 **Asana** - Add task với script attached
- 🗂️ **Monday.com** - Update items

## 📊 Performance

### Speed
- Basic workflow: **30-60 giây**
- Advanced workflow: **45-90 giây**

### Cost (với OpenAI GPT-4)
- Short script (< 500 từ): **$0.01-0.02**
- Medium script (500-1500 từ): **$0.02-0.04**
- Long script (> 1500 từ): **$0.04-0.08**

### Quality
- Accuracy: **90-95%** (cần review nhẹ)
- Completeness: **85-90%** (đôi khi thiếu details)
- Creativity: **80-85%** (phụ thuộc temperature)

## 🐛 Troubleshooting

### Lỗi "Invalid API Key"
→ Kiểm tra API key tại https://platform.openai.com/api-keys

### Lỗi "Rate Limit Exceeded"
→ Chờ vài phút hoặc upgrade OpenAI plan

### Script không đúng format
→ Chỉnh prompt rõ ràng hơn, thêm examples

### Workflow timeout
→ Tăng timeout trong Settings, giảm maxTokens

Xem thêm: [HUONG-DAN-SU-DUNG-N8N-VIDEO-SCRIPT.md](HUONG-DAN-SU-DUNG-N8N-VIDEO-SCRIPT.md)

## 🤝 Contributing

Contributions welcome! Để contribute:

1. Fork repo này
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## 📝 License

MIT License - Tự do sử dụng cho mục đích cá nhân và thương mại.

## 🙏 Credits

- **n8n** - Workflow automation platform
- **OpenAI** - GPT-4 API
- **Community** - Thanks to all contributors!

## 📞 Support

- 📖 [Documentation](HUONG-DAN-SU-DUNG-N8N-VIDEO-SCRIPT.md)
- 💬 [n8n Community](https://community.n8n.io/)
- 🐛 [Report Issues](https://github.com/yourusername/repo/issues)

## 🗺️ Roadmap

- [ ] Thêm hỗ trợ Claude AI (Anthropic)
- [ ] Thêm hỗ trợ Gemini (Google)
- [ ] Multi-language templates
- [ ] Voice-over script generation
- [ ] Storyboard generation
- [ ] Video editing timeline export
- [ ] A/B testing title suggestions
- [ ] Thumbnail text generator

---

**Made with ❤️ by [Your Name]**

⭐ Nếu bạn thấy hữu ích, hãy star repo này!
