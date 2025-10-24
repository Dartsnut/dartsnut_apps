from PIL import Image, ImageDraw, ImageFont
import time
from pydartsnut import Dartsnut

# --- Constants and Initialization ---
WIDTH, HEIGHT = 128, 160
MAIN_TEXT_AREA_HEIGHT = 128
SECOND_TEXT_AREA_Y_START = 130
SCROLL_SPEED = 10  # pixels per second

# --- Load fonts once ---
try:
    # Using a slightly larger default font if available can look better
    main_font = ImageFont.truetype("arial.ttf", 14)
    second_font = ImageFont.truetype("arial.ttf", 10)
    main_line_height = 15
    second_line_height = 12
except IOError:
    # Fallback to default bitmap font
    main_font = ImageFont.load_default() # Default size is 10
    second_font = ImageFont.load_default()
    main_line_height = 12
    second_line_height = 12


dartsnut = Dartsnut()
main_text = dartsnut.widget_params.get("main_text", """FROM off a hill whose concave womb reworded
A plaintful story from a sistering vale,
My spirits to attend this double voice accorded,
And down I laid to list the sad-tuned tale;
Ere long espied a fickle maid full pale,
Tearing of papers, breaking rings a-twain,
Storming her world with sorrow's wind and rain.

Upon her head a platted hive of straw,
Which fortified her visage from the sun,
Whereon the thought might think sometime it saw
The carcass of beauty spent and done:
Time had not scythed all that youth begun,
Nor youth all quit; but, spite of heaven's fell rage,
Some beauty peep'd through lattice of sear'd age.
""")
second_text = dartsnut.widget_params.get("second_text", "Shakespeare - A Lover's Complaint")

# --- Text wrapping function (optimized for clarity) ---
def wrap_text(text, font, max_width):
    lines = []
    for para in text.split('\n'):
        if not para.strip():
            lines.append('')  # Preserve empty lines
            continue
        words = para.split()
        current_line = ""
        for word in words:
            # Use getbbox for more accurate width calculation
            if font.getbbox(current_line + word)[2] <= max_width:
                current_line += word + " "
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
    return lines

# --- Pre-calculate wrapped text and dimensions ---
main_lines = wrap_text(main_text, main_font, WIDTH - 10) # Give some margin
second_lines = wrap_text(second_text, second_font, WIDTH - 8)

total_text_height = main_line_height * len(main_lines)
start_time = time.time()

def get_scroll_offset():
    """Calculates the vertical scroll offset for the main text."""
    if total_text_height <= MAIN_TEXT_AREA_HEIGHT:
        return 0
    # Calculate total scrollable distance
    scrollable_height = total_text_height - MAIN_TEXT_AREA_HEIGHT + main_line_height
    elapsed_time = time.time() - start_time
    # Use modulo to create a looping scroll effect
    offset = (elapsed_time * SCROLL_SPEED) % scrollable_height
    return offset

def render():
    """Renders a single frame of the widget."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    # --- Draw scrolling main text ---
    y = -get_scroll_offset()
    for line in main_lines:
        # Only draw lines that are visible on screen
        if y + main_line_height > 0 and y < MAIN_TEXT_AREA_HEIGHT:
            # Shadow
            draw.text((6, int(y) + 6), line, font=main_font, fill=(40, 40, 40))
            # Main text
            draw.text((4, int(y) + 5), line, font=main_font, fill=(255, 255, 255))
            # Red line under text
            line_y = int(y) + 18
            draw.line([(4, line_y), (124, line_y)], fill=(160, 0, 0), width=1)
        y += main_line_height

    # --- Draw second static text area ---
    img.paste((0, 0, 0), (0, 128, 64, 159)) # Clear area
    y_pos = SECOND_TEXT_AREA_Y_START
    for line in second_lines:
        draw.text((4, y_pos), line, font=second_font, fill=(180, 200, 255))
        y_pos += second_line_height

    return img

# Main loop to update and display the widget image
try:
    while dartsnut.running:
        dartsnut.update_frame_buffer(render())
        time.sleep(0.1) # Can potentially use a shorter sleep time now
except KeyboardInterrupt:
    pass
print("simple_letter_128_160 existing...")