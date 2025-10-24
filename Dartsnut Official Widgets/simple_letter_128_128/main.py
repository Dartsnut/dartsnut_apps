from PIL import Image, ImageDraw, ImageFont
import time
from pydartsnut import Dartsnut

dartsnut = Dartsnut()
main_text = dartsnut.widget_params.get("main_text", "")

# --- Constants and one-time setup ---
FONT_SIZE = 16
MAX_WIDTH = 120
LINE_HEIGHT = 16
SCROLL_SPEED = 10  # pixels per second
SHADOW_COLOR = (40, 40, 40)
TEXT_COLOR = (255, 255, 255)
LINE_COLOR = (160, 0, 0)

# Load font once
font = ImageFont.load_default(FONT_SIZE)

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
                    # If the word itself is longer than max_width, put it on its own line
                    lines.append(words[0])
                    words.pop(0)
        if line:
            lines.append(line.strip())
    return lines

main_lines = wrap_text(main_text, font, MAX_WIDTH)

# Calculate total text height
total_height = LINE_HEIGHT * len(main_lines)

# Scrolling setup
start_time = time.time()

def get_scroll_offset():
    if total_height <= 128:
        return 0
    elapsed = time.time() - start_time
    # The scrollable range
    scroll_range = total_height - 128 + LINE_HEIGHT + 10 # Add padding at the end
    if scroll_range <= 0:
        return 0
    offset = (elapsed * SCROLL_SPEED) % scroll_range
    return offset

def render():
    img = Image.new("RGB", (128, 128), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    y_start = 5 - get_scroll_offset()
    for i, line in enumerate(main_lines):
        y = y_start + (i * LINE_HEIGHT)
        # Shadow
        draw.text((6, int(y)+1), line, font=font, fill=SHADOW_COLOR)
        # Main text
        draw.text((4, int(y)), line, font=font, fill=TEXT_COLOR)
        # Red line under text
        line_y = int(y) + LINE_HEIGHT
        draw.line([(4, line_y), (124, line_y)], fill=LINE_COLOR, width=1)

    return img

# Main loop to update and display the widget image
try:
    while dartsnut.running:
        dartsnut.update_frame_buffer(render())
        time.sleep(0.1) # Can potentially use a shorter sleep time now
except KeyboardInterrupt:
    pass
print("simple_letter_128_128 existing...")