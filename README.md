# Sora AI Video Generator 🎬

ManixAI Tools v1.2.3 - AI Video Generation Tool using OpenAI Sora with Browser Automation

## Features

- 🎥 Generate AI videos from text descriptions using Sora
- 🤖 **Browser Automation** - Auto-login with Gmail to sora.chatgpt.com
- 🖥️ Modern PyQt5 graphical interface
- 🔐 Secure Gmail authentication
- 💾 Automatic video download
- 📊 Real-time progress tracking
- 🌐 Works with ChatGPT Plus/Pro accounts

## Requirements

- Python 3.13 or higher
- **ChatGPT Plus** ($20/month) or **ChatGPT Pro** ($200/month) account
- Gmail account for login
- Windows OS (can be adapted for Linux/Mac)
- Chrome/Chromium browser (installed automatically)

## Installation

### Method 1: Using install.bat (Windows)

1. Double-click `install.bat`
2. Wait for installation to complete
3. **Test browser** (recommended): `python test_browser.py`
4. Run the application using `run.bat`

### Method 2: Manual Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Usage

### 1. Login with Gmail

1. Open the application
2. Go to **Tab 1: Login**
3. Enter your Gmail address (the one linked to ChatGPT Plus/Pro)
4. Enter your Gmail password
5. Optional: Check "Headless mode" to hide browser window
6. Click **Login to Sora**
7. Wait for automatic browser login (takes 15-30 seconds)
8. ✅ You'll see "Login successful!" when done

### 2. Generate Video

1. Go to **Tab 2: Generate Video**
2. Enter your video description in the prompt box
   - Example: "A serene sunset over a calm ocean, with gentle waves and seagulls flying"
3. Click **Generate Video**
4. Wait for generation (takes 2-5 minutes depending on complexity)
5. Click **Download Video** when ready

### 3. Access Your Videos

Generated videos are saved to:
- Default: `~/SoraVideos/`
- Files named: `sora_video_YYYYMMDD_HHMMSS.mp4`

## Project Structure

```
thu-code/
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── install.bat                  # Windows installation script
├── run.bat                      # Windows run script
├── README.md                    # This file
└── modules/
    ├── __init__.py              # Module initialization
    ├── app_runner.py            # Application runner with async support
    ├── gui_browser.py           # PyQt5 GUI with browser automation
    ├── browser_automation.py    # Zendriver browser automation
    ├── sora_api.py              # OpenAI Sora API (backup method)
    └── config.py                # Configuration management
```

## Configuration

Configuration is stored in `~/.sora_config.json`:

```json
{
  "api_key": "your-api-key",
  "output_dir": "/path/to/videos",
  "default_resolution": "1920x1080",
  "default_duration": 5
}
```

## Troubleshooting

### "Please login first in the Login tab"
- You must login with Gmail before generating videos
- Go to Tab 1: Login and enter your credentials
- Wait for "Login successful!" message

### "Module not found" error
- Make sure you've run `install.bat` or manually installed requirements
- Activate the virtual environment before running: `venv\Scripts\activate`

### Login fails
- Check your Gmail email and password are correct
- Make sure your Gmail account has ChatGPT Plus or Pro subscription
- Try unchecking "Headless mode" to see what's happening
- Some Gmail accounts require 2FA - you may need an app-specific password

### "Failed to initialize browser"
- **First, run test**: `python test_browser.py`
- Make sure zendriver is installed: `pip install zendriver==0.14.2`
- Zendriver will auto-download Chrome if needed
- Check firewall/antivirus isn't blocking browser
- Try running as Administrator
- Update pip: `python -m pip install --upgrade pip`
- On some systems, you may need to install Chrome manually

### Video generation times out
- Sora generation can take 2-5 minutes, be patient
- Check the browser window (if not headless) for errors
- Verify your ChatGPT account has Sora access

### GUI doesn't open
- Make sure PyQt5 is installed correctly
- Try reinstalling: `pip install -r requirements.txt --force-reinstall`

## Important Notes

⚠️ **Requirements**:
- **ChatGPT Plus** ($20/month) or **ChatGPT Pro** ($200/month) subscription required
- Free ChatGPT accounts cannot access Sora
- Subscribe at: https://chatgpt.com/

🔐 **Security**:
- Your Gmail credentials are NEVER stored or transmitted except to Google
- Browser automation happens locally on your machine
- Credentials only used for login to sora.chatgpt.com

🌐 **How it works**:
- Uses browser automation (Zendriver) to control Chrome
- Automatically logs into sora.chatgpt.com with your Gmail
- Simulates human interaction to generate videos
- Downloads videos directly from the Sora web interface

## License

ManixAI Tools v1.2.3

## Support

For issues and questions:
- Check the Troubleshooting section above
- Review OpenAI Sora documentation
- Ensure your API key has proper permissions

---

Made with ❤️ by ManixAI
