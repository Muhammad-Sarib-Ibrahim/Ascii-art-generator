# ASCII Art Generator

A command-line tool that converts any image into ASCII art, right in your terminal.

Drag and drop an image in, and it renders it using nothing but characters like `@%#*+=-:.` — denser characters for dark areas, sparse ones for light areas.

## Demo

```
📂  Drag and drop your image here, then press Enter: my_photo.png
↔️  Output width in characters (press Enter for 100): 80
🎨  Invert for a dark-background terminal? (y/N): n

<img width="1834" height="2048" alt="WhatsApp Image 2026-07-04 at 19 47 10" src="https://github.com/user-attachments/assets/4ac83a01-8569-417e-a678-e188cbdd5179" />

## Features

- Interactive prompts — no command-line flags to memorize
- Drag-and-drop file input (handles quoted and backslash-escaped paths from macOS/Linux terminals)
- Adjustable output width
- Invert mode for dark-background terminals
- Save output to a `.txt` file
- Convert multiple images in one session

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/ascii-art-generator.git
cd ascii-art-generator
pip install -r requirements.txt
```

## Usage

```bash
python3 ascii_art.py
```

Then follow the prompts: drag an image file into the terminal window, press Enter, and answer a couple of quick questions.

## How it works

1. **Grayscale conversion** — the image is converted so each pixel is a single brightness value (0–255) instead of RGB.
2. **Resize** — the image is scaled down to a manageable character grid. Terminal characters are roughly twice as tall as they are wide, so height is corrected by a `0.55` factor to avoid stretched output.
3. **Brightness-to-character mapping** — each pixel's brightness is mapped to a character in a ramp ordered from sparse (`" "`) to dense (`"@"`). Lookup is a simple scaled index: `pixel_value * (len(ramp) - 1) // 255`.
4. **Reassembly** — the flat string of characters is split back into rows matching the resized image width, and printed.

## Tech

- Python 3
- [Pillow](https://python-pillow.org/) for image loading and processing

## Possible extensions

- Color ASCII output (map RGB instead of grayscale)
- Custom character ramps via a `--charset` option
- Live webcam-to-ASCII mode

## License

MIT
