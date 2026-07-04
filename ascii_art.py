"""
ASCII Art Generator

Converts an image into ASCII art printed to the terminal (or saved to a file).

Usage:
    python3 ascii_art.py path/to/image.png
    python3 ascii_art.py path/to/image.png --width 120
    python3 ascii_art.py path/to/image.png --output result.txt
    python3 ascii_art.py path/to/image.png --invert   (for light-on-dark terminals)
"""

import os
from PIL import Image

BANNER = r"""
╔══════════════════════════════════════════╗
║          A S C I I   A R T                ║
║             G E N E R A T O R             ║
╚══════════════════════════════════════════╝
"""

# Characters ordered from "lightest" to "darkest" visual density.
# This is the ramp we map brightness values onto.
ASCII_CHARS = " .:-=+*#%@"

# Terminal characters are roughly twice as tall as they are wide.
# Without this correction, output looks vertically stretched.
CHAR_ASPECT_CORRECTION = 0.55


def resize_image(image, new_width=100):
    """Resize the image to new_width columns, adjusting height for
    terminal character aspect ratio so the final art isn't stretched."""
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio * CHAR_ASPECT_CORRECTION)
    return image.resize((new_width, max(new_height, 1)))


def grayify(image):
    """Convert image to grayscale - each pixel becomes one brightness value."""
    return image.convert("L")


def pixels_to_ascii(image):
    """Map each pixel's brightness (0-255) to a character in ASCII_CHARS."""
    pixels = image.get_flattened_data() if hasattr(image, "get_flattened_data") else image.getdata()
    chars = []
    for pixel_value in pixels:
        # Scale 0-255 down to an index into ASCII_CHARS
        index = pixel_value * (len(ASCII_CHARS) - 1) // 255
        chars.append(ASCII_CHARS[index])
    return "".join(chars)


def image_to_ascii(path, width=100, invert=False):
    try:
        image = Image.open(path)
    except Exception as e:
        return f"Error opening image: {e}"

    image = resize_image(image, width)
    image = grayify(image)

    if invert:
        # Flip the ramp for light-text-on-dark-background terminals,
        # where "dark" pixels should map to sparse characters instead.
        global ASCII_CHARS
        ASCII_CHARS = ASCII_CHARS[::-1]

    ascii_str = pixels_to_ascii(image)

    # Break the flat string back into rows matching the resized width.
    img_width = image.width
    ascii_lines = [
        ascii_str[i:i + img_width] for i in range(0, len(ascii_str), img_width)
    ]
    return "\n".join(ascii_lines)


def clean_dropped_path(raw_path):
    """Clean up a file path pasted in by dragging a file into the terminal.

    Terminals wrap dropped paths in quotes, or escape spaces with a
    backslash (e.g. My\\ Photo.png), depending on OS and shell. This
    strips both so the raw drag-and-drop text becomes a usable path.
    """
    path = raw_path.strip()
    if len(path) >= 2 and path[0] == path[-1] and path[0] in ("'", '"'):
        path = path[1:-1]
    path = path.replace("\\ ", " ")
    return os.path.expanduser(path)


def prompt_for_image():
    """Keep asking until we get a path to a file that actually exists."""
    while True:
        raw = input("📂  Drag and drop your image here, then press Enter: ")
        path = clean_dropped_path(raw)
        if os.path.isfile(path):
            return path
        print(f"   Couldn't find a file at: {path}\n   Try again.\n")


def prompt_width():
    raw = input("↔️  Output width in characters (press Enter for 100): ").strip()
    if not raw:
        return 100
    try:
        return max(int(raw), 10)
    except ValueError:
        print("   Not a number, using default width of 100.")
        return 100


def prompt_yes_no(question, default=False):
    suffix = "Y/n" if default else "y/N"
    raw = input(f"{question} ({suffix}): ").strip().lower()
    if not raw:
        return default
    return raw.startswith("y")


def main():
    print(BANNER)
    print("Turn any image into ASCII art. Type 'q' at any image prompt to quit.\n")

    while True:
        image_path = prompt_for_image()
        width = prompt_width()
        invert = prompt_yes_no("🎨  Invert for a dark-background terminal?", default=False)

        print("\nGenerating...\n")
        result = image_to_ascii(image_path, width=width, invert=invert)
        print(result)

        if prompt_yes_no("\n💾  Save this to a text file?", default=False):
            default_name = os.path.splitext(os.path.basename(image_path))[0] + "_ascii.txt"
            out_name = input(f"   File name (press Enter for '{default_name}'): ").strip()
            out_name = out_name or default_name
            with open(out_name, "w") as f:
                f.write(result)
            print(f"   Saved to {out_name}")

        if not prompt_yes_no("\n🔁  Convert another image?", default=True):
            print("\nSee ya! 👋")
            break
        print()


if __name__ == "__main__":
    main()
