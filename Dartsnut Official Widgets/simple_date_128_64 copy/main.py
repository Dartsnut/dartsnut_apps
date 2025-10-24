from pydartsnut import Dartsnut
import time
from PIL import Image, ImageDraw, ImageFont

dartsnut = Dartsnut()

# Load the font once at the beginning of the script
FONT = ImageFont.load_default(size=28)

def draw_clock(font):
    """Draws the date on a 128x64 image."""
    # Create a blank image (128x64, black background)
    img = Image.new("RGB", (128, 64), "black")
    draw = ImageDraw.Draw(img)

    # Get the current time once per function call
    current_time = time.localtime()
    year_str = time.strftime("%Y", current_time)
    month_day_str = time.strftime("%b - %d", current_time)

    # Measure text sizes
    year_bbox = draw.textbbox((0, 0), year_str, font=font)
    month_day_bbox = draw.textbbox((0, 0), month_day_str, font=font)
    year_w = year_bbox[2] - year_bbox[0]
    year_h = year_bbox[3] - year_bbox[1]
    month_day_w = month_day_bbox[2] - month_day_bbox[0]
    month_day_h = month_day_bbox[3] - month_day_bbox[1]

    # Calculate positions to center both lines
    total_h = year_h + month_day_h + 4  # 4 pixels spacing
    year_x = (128 - year_w) // 2
    month_day_x = (128 - month_day_w) // 2
    start_y = (64 - total_h) // 2 - 10
    year_y = start_y
    month_day_y = start_y + year_h + 8

    draw.text((year_x, year_y), year_str, fill="white", font=font)
    draw.text((month_day_x, month_day_y), month_day_str, fill="white", font=font)

    return img

# display
try:
    while dartsnut.running:
        # Pass the pre-loaded font to the drawing function
        frame = draw_clock(FONT)
        dartsnut.update_frame_buffer(frame)
        time.sleep(60)
except KeyboardInterrupt:
    pass
print("simple_date_128_64 exiting...")