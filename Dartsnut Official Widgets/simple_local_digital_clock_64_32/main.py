from pydartsnut import Dartsnut
import time
from PIL import Image, ImageDraw, ImageFont

dartsnut = Dartsnut()

# Load font once outside the loop to improve performance
font = ImageFont.load_default(size=15)

def draw_clock():
    # Create a blank image (64x32, black background)
    img = Image.new("RGB", (64, 32), "black")
    draw = ImageDraw.Draw(img)

    # Get current time
    digital_time = time.strftime("%H:%M:%S", time.localtime())

    # Calculate text position for centering
    text_bbox = draw.textbbox((0, 0), digital_time, font=font)
    text_w = text_bbox[2] - text_bbox[0]
    text_h = text_bbox[3] - text_bbox[1]
    text_x = (64 - text_w) // 2
    text_y = (32 - text_h) // 2 - 5

    # Draw digital clock
    draw.text((text_x, text_y), digital_time, fill="white", font=font)

    return img

# display
try:
    while dartsnut.running:
        dartsnut.update_frame_buffer(draw_clock())
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
print("simple_local_digital_clock_64_32 exiting...")