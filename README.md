# Sora AI Video Generator 🎬

ManixAI Tools v1.2.3 - AI Video Generation Tool using OpenAI Sora

## Features

- 🎥 Generate AI videos from text descriptions using Sora
- 🖥️ Modern PyQt5 graphical interface
- ⚙️ Configurable video parameters (duration, resolution)
- 💾 Easy video download and management
- 🔑 Secure API key storage
- 📊 Real-time progress tracking

## Requirements

- Python 3.13 or higher
- OpenAI API key with Sora access
- Windows OS (can be adapted for Linux/Mac)

## Installation

### Method 1: Using install.bat (Windows)

1. Double-click `install.bat`
2. Wait for installation to complete
3. Run the application using `run.bat`

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

### 1. Configure API Key

1. Open the application
2. Go to the **Settings** tab
3. Enter your OpenAI API key
4. Click **Save API Key**

### 2. Generate Video

1. Go to the **Generate Video** tab
2. Enter your video description in the prompt box
   - Example: "A serene sunset over a calm ocean, with gentle waves and seagulls flying"
3. Set video parameters:
   - **Duration**: 3-10 seconds
   - **Resolution**: Choose from 1080p, 720p, 4K, or portrait
4. Click **Generate Video**
5. Wait for generation to complete
6. Click **Download Video** to save

### 3. Access Your Videos

Generated videos are saved to:
- Default: `~/SoraVideos/`
- Custom: Configure in Settings tab

## Project Structure

```
thu-code/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── install.bat            # Windows installation script
├── run.bat                # Windows run script
├── README.md              # This file
└── modules/
    ├── __init__.py        # Module initialization
    ├── app_runner.py      # Application runner
    ├── gui.py             # PyQt5 GUI interface
    ├── sora_api.py        # OpenAI Sora API integration
    └── config.py          # Configuration management
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

### "API key not configured"
- Go to Settings tab and enter your OpenAI API key
- Get your API key from: https://platform.openai.com/api-keys

### "Module not found" error
- Make sure you've run `install.bat` or manually installed requirements
- Activate the virtual environment before running

### Video generation fails
- Check your internet connection
- Verify your API key has Sora access
- Ensure you have sufficient API credits

### GUI doesn't open
- Make sure PyQt5 is installed correctly
- Try reinstalling dependencies: `pip install -r requirements.txt --force-reinstall`

## API Notes

⚠️ **Important**:
- Sora API access requires special approval from OpenAI
- Standard OpenAI API keys may not have Sora access
- Apply for access at: https://openai.com/sora

## License

ManixAI Tools v1.2.3

## Support

For issues and questions:
- Check the Troubleshooting section above
- Review OpenAI Sora documentation
- Ensure your API key has proper permissions

---

Made with ❤️ by ManixAI
