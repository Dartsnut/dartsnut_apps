from pydartsnut import Dartsnut
import time
from PIL import Image, ImageDraw, ImageFont

dartsnut = Dartsnut()

# --- Optimizations ---
# 1. Define constants for dimensions for clarity.
WIDTH, HEIGHT = 128, 64
# 2. Load the font only once outside the loop, as it's a costly operation.
font = ImageFont.load_default(size=30)

def draw_clock():
    # Create a blank image (128x64, black background)
    img = Image.new("RGB", (WIDTH, HEIGHT), "black")
    draw = ImageDraw.Draw(img)

    # Get current time
    digital_time = time.strftime("%H:%M:%S", time.localtime())

    # Calculate text position for centering
    text_bbox = draw.textbbox((0, 0), digital_time, font=font)
    text_w = text_bbox[2] - text_bbox[0]
    text_h = text_bbox[3] - text_bbox[1]
    text_x = (WIDTH - text_w) // 2
    text_y = (HEIGHT - text_h) // 2 - 10
    
    # Draw digital clock text
    draw.text((text_x, text_y), digital_time, fill="white", font=font)

    return img

# display
try:
    while dartsnut.running:
        dartsnut.update_frame_buffer(draw_clock())
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
print("simple_local_digital_clock_128_64 exiting...")