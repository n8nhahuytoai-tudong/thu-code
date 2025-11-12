# OpenAI Sora API Plus - ComfyUI Custom Nodes

Custom ComfyUI nodes for generating videos using OpenAI's Sora API. Supports text-to-video and image-to-video generation with advanced controls.

## Features

- **Text-to-Video Generation**: Create videos from text prompts
- **Image-to-Video Generation**: Animate reference images with text guidance
- **Multiple Resolutions**: Support for various aspect ratios (16:9, 9:16, 1:1, etc.)
- **Quality Control**: Standard, High, and Ultra quality settings
- **Style Presets**: Cinematic, anime, photographic, digital art, and 3D model styles
- **Seed Control**: Reproducible video generation
- **Automatic Download**: Built-in video downloader node
- **Task Status Monitoring**: Check generation progress

## Installation

### Method 1: ComfyUI Manager (Recommended)

1. Open ComfyUI Manager
2. Search for "OpenAI Sora API Plus"
3. Click Install
4. Restart ComfyUI

### Method 2: Manual Installation

1. Navigate to your ComfyUI custom nodes directory:
   ```bash
   cd ComfyUI/custom_nodes/
   ```

2. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/comfyui-sora-api-node.git
   ```

3. Install dependencies:
   ```bash
   cd comfyui-sora-api-node
   pip install -r requirements.txt
   ```

4. Restart ComfyUI

## Setup

### API Key Configuration

You need an OpenAI API key with Sora API access. Configure it using one of these methods:

**Option 1: Environment Variable (Recommended)**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

**Option 2: In Node**
Enter your API key directly in the `api_key` field of the node.

## Available Nodes

### 1. OpenAI Sora API Plus ⚡

Main node for video generation.

**Inputs:**
- `prompt` (required): Text description of the video to generate
- `api_key` (required): OpenAI API key
- `duration` (required): Video duration (5s, 10s, 15s, 20s)
- `resolution` (required): Output resolution (1920x1080, 1080x1920, etc.)
- `aspect_ratio` (required): Aspect ratio (16:9, 9:16, 1:1, 4:3, 3:4)
- `fps` (required): Frames per second (24, 30, 60)
- `quality` (required): Generation quality (standard, high, ultra)
- `reference_image` (optional): Input image for image-to-video generation
- `negative_prompt` (optional): What to avoid in the generation
- `seed` (optional): Seed for reproducibility (-1 for random)
- `style_preset` (optional): Style preset (none, cinematic, anime, photographic, digital_art, 3d_model)

**Outputs:**
- `video_url`: URL to the generated video
- `task_id`: Unique task identifier
- `status`: Generation status (completed, failed, etc.)

### 2. Sora Video Downloader 📥

Download generated videos to local storage.

**Inputs:**
- `video_url` (required): Video URL from Sora API node
- `output_filename` (required): Output filename (use `%time%` for timestamp)

**Outputs:**
- `file_path`: Local path to downloaded video file

### 3. Sora Task Status 📊

Check the status of a video generation task.

**Inputs:**
- `task_id` (required): Task ID from Sora API node
- `api_key` (required): OpenAI API key

**Outputs:**
- `status`: Current task status
- `video_url`: Video URL (if completed)
- `error_message`: Error details (if failed)

## Usage Examples

### Example 1: Text-to-Video Generation

1. Add **OpenAI Sora API Plus** node
2. Set prompt: "A serene lake at sunset with mountains in the background"
3. Configure duration, resolution, and quality
4. Add **Sora Video Downloader** node
5. Connect `video_url` output to downloader input
6. Run workflow

### Example 2: Image-to-Video Generation

1. Load an image using **Load Image** node
2. Add **OpenAI Sora API Plus** node
3. Connect image to `reference_image` input
4. Set prompt: "Animate this scene with gentle wind and moving clouds"
5. Add **Sora Video Downloader** node
6. Run workflow

### Example 3: Check Task Status

1. Copy `task_id` from a running generation
2. Add **Sora Task Status** node
3. Enter task_id and api_key
4. Run to check status

## Workflow Example

```
[Load Image] → [OpenAI Sora API Plus] → [Sora Video Downloader] → [Output]
                       ↓
                 [Sora Task Status]
```

## Configuration Options

### Duration Options
- `5s` - 5 seconds
- `10s` - 10 seconds
- `15s` - 15 seconds
- `20s` - 20 seconds

### Resolution Options
- `1920x1080` - Full HD (16:9)
- `1080x1920` - Full HD Portrait (9:16)
- `1280x720` - HD (16:9)
- `720x1280` - HD Portrait (9:16)
- `1024x1024` - Square (1:1)

### Quality Options
- `standard` - Fast generation, lower quality
- `high` - Balanced quality and speed
- `ultra` - Best quality, slower generation

### Style Presets
- `none` - No style applied
- `cinematic` - Movie-like cinematography
- `anime` - Anime/manga style
- `photographic` - Realistic photography
- `digital_art` - Digital illustration style
- `3d_model` - 3D rendered look

## Troubleshooting

### API Key Issues
- Ensure your OpenAI API key has Sora API access
- Check that the API key is correctly set in environment or node
- Verify there are no extra spaces in the API key

### Generation Failures
- Check your OpenAI API quota and billing
- Verify prompt follows content policy
- Try reducing quality or duration
- Check internet connection

### Download Issues
- Ensure sufficient disk space
- Check write permissions in output directory
- Verify video URL is valid and accessible

## API Rate Limits

OpenAI Sora API has rate limits. If you encounter rate limit errors:
- Wait before retrying
- Use lower quality settings
- Reduce concurrent generations

## Notes

- Video generation can take 1-10 minutes depending on duration and quality
- The node will automatically poll for completion
- Maximum wait time is 5 minutes (configurable in code)
- Generated videos are MP4 format

## Support

For issues, questions, or contributions:
- GitHub Issues: [Report a bug](https://github.com/yourusername/comfyui-sora-api-node/issues)
- Discussions: [Ask questions](https://github.com/yourusername/comfyui-sora-api-node/discussions)

## License

MIT License

## Credits

Created with assistance from Claude AI (Anthropic)

## Changelog

### Version 1.0.0
- Initial release
- Text-to-video generation
- Image-to-video generation
- Multiple resolution and quality options
- Style presets
- Video downloader
- Task status checker
