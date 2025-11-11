#!/bin/bash

echo "========================================="
echo "   Video Analyzer - Installation"
echo "========================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
cd ..
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "✓ Dependencies installed successfully!"
echo ""

# Setup .env
cd video_analyzer
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your ANTHROPIC_API_KEY"
    echo "   Get your key at: https://console.anthropic.com/"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "========================================="
echo "✅ Installation completed!"
echo "========================================="
echo ""
echo "Quick start:"
echo "  python video_analyzer.py --input your_video.mp4"
echo ""
echo "For more info, see README.md"
