from PIL import Image, ImageDraw, ImageFont
import time
from pydartsnut import Dartsnut

dartsnut = Dartsnut()
main_text = dartsnut.widget_params.get("main_text", "")

# Text wrapping
def wrap_text(text, font, max_width):
    lines = []
    paragraphs = text.split('\n')
    for para in paragraphs:
        if not para.strip():
            lines.append('')  # Preserve empty lines
            continue
        words = para.split()
        line = ''
        while words:
            if not line:
                test_line = words[0] + ' '
            else:
                test_line = line + words[0] + ' '
            if font.getlength(test_line) <= max_width:
                line = test_line
                words.pop(0)
            else:
                if line:
                    lines.append(line.strip())
                    line = ''
                else:
                    # If the word itself is longer than max_width, put it on its own line and ignore width
                    lines.append(words[0])
                    words.pop(0)
        if line:
            lines.append(line.strip())
    return lines

main_lines = wrap_text(main_text, ImageFont.load_default(16), 108)

# Calculate total text height
line_height = 16
total_height = line_height * len(main_lines)

# Scrolling setup
scroll_speed = 10  # pixels per second
start_time = time.time()

def get_scroll_offset():
    if total_height <= 128:
        return 0
    elapsed = time.time() - start_time
    offset = (elapsed * scroll_speed) % (total_height - 118 + line_height)
    return offset

def render():
    img = Image.new("RGB", (128, 128), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Gradient background
    for y in range(128):
        shade = int(30 + 80 * (y / 128))  # from dark to lighter
        draw.line([(0, y), (127, y)], fill=(shade, shade, shade))

    # Drop shadow for main text
    y = -get_scroll_offset()
    for line in main_lines:
        # Shadow
        draw.text((6, int(y)+6), line, font=ImageFont.load_default(16), fill=(40, 40, 40))
        # Main text
        draw.text((4, int(y)+5), line, font=ImageFont.load_default(16), fill=(255, 255, 255))
        y += line_height

    # Border with rounded corners
    for y in range(8):
        shade = int(30 + 80 * (y / 128))  # from dark to lighter
        draw.line([(0, y), (127, y)], fill=(shade, shade, shade))
    
    for y in range(120,128):
        shade = int(30 + 80 * (y / 128))  # from dark to lighter
        draw.line([(0, y), (127, y)], fill=(shade, shade, shade))
    draw.rounded_rectangle((2, 2, 125, 125), radius=12, outline=(200, 180, 120), width=2)

    return img

# Example usage: update and display the widget image
while True:
    dartsnut.update_frame_buffer(render())
    time.sleep(0.5)