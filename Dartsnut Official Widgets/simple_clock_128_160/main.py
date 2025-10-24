from PIL import Image, ImageDraw, ImageFont
import math
import time
from pydartsnut import Dartsnut
import zoneinfo
import datetime
import requests

# --- Initialization and API Calls (Optimized) ---
dartsnut = Dartsnut()
city_name = dartsnut.widget_params.get("city", "")
timezone_id = None
city = "Unknown"
tz_info = None

if city_name:
    # Added a retry limit to prevent infinite loops on startup
    for _ in range(3): # Try 3 times
        try:
            # Step 1: Get location data
            geo_resp = requests.get(
                "https://secure.geonames.org/searchJSON",
                params={"q": city_name, "maxRows": 1, "username": "dartsnut"},
                timeout=5 # Added timeout
            )
            geo_resp.raise_for_status()
            geo_data = geo_resp.json()

            if geo_data.get("geonames"):
                geoname = geo_data["geonames"][0]
                lat, lng = geoname["lat"], geoname["lng"]
                city = geoname["name"]

                # Step 2: Get timezone data
                tz_resp = requests.get(
                    "https://secure.geonames.org/timezoneJSON",
                    params={"lat": lat, "lng": lng, "username": "dartsnut"},
                    timeout=5 # Added timeout
                )
                tz_resp.raise_for_status()
                tz_data = tz_resp.json()
                timezone_id = tz_data.get('timezoneId')
                if timezone_id:
                    tz_info = zoneinfo.ZoneInfo(timezone_id)
            break # Success, exit retry loop
        except requests.exceptions.RequestException as e:
            print(f"Error fetching location data: {e}")
            time.sleep(2) # Wait before retrying
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break

# --- Pre-rendering Static Elements ---
def create_background(city_name):
    """Creates the static background image for the clock."""
    img = Image.new("RGB", (128, 160), "black")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    if not tz_info:
        # Display "City not found" message
        msg = "City not found"
        text_bbox = draw.textbbox((0, 0), msg, font_size=16)
        text_w = text_bbox[2] - text_bbox[0]
        text_h = text_bbox[3] - text_bbox[1]
        text_x = (128 - text_w) // 2
        text_y = (128 - text_h) // 2
        draw.text((text_x, text_y), msg, fill="red", font_size=16)
    else:
        # Clock center and radius
        cx, cy, r = 64, 64, 60

        # Draw clock face (white outline and hour marks)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline="white", width=2)
        for i in range(12):
            angle = math.radians(i * 30)
            x1 = cx + int((r - 8) * math.sin(angle))
            y1 = cy - int((r - 8) * math.cos(angle))
            x2 = cx + int(r * math.sin(angle))
            y2 = cy - int(r * math.cos(angle))
            draw.line((x1, y1, x2, y2), fill="white", width=2)

        # Draw bottom panel and city name
        draw.rectangle((0, 128, 63, 159), fill=(32, 32, 32))
        city_bbox = draw.textbbox((0, 0), city_name, font=font)
        city_w = city_bbox[2] - city_bbox[0]
        city_x = (64 - city_w) // 2
        city_y = 128 + 4 + 11 + 4 # Position below where time will be
        draw.text((city_x, city_y), city_name, fill="lightgray", font=font)

    return img

def draw_clock_hands(img, now):
    """Draws the dynamic clock hands and digital time onto the background."""
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    cx, cy, r = 64, 64, 60

    hour = now.hour % 12
    minute = now.minute
    second = now.second

    # Hour hand
    hour_angle = math.radians((hour + minute / 60) * 30 - 90)
    hx = cx + int((r - 28) * math.cos(hour_angle))
    hy = cy + int((r - 28) * math.sin(hour_angle))
    draw.line((cx, cy, hx, hy), fill="white", width=5)

    # Minute hand
    min_angle = math.radians((minute + second / 60) * 6 - 90)
    mx = cx + int((r - 16) * math.cos(min_angle))
    my = cy + int((r - 16) * math.sin(min_angle))
    draw.line((cx, cy, mx, my), fill="gray", width=3)

    # Second hand
    sec_angle = math.radians(second * 6 - 90)
    sx = cx + int((r - 10) * math.cos(sec_angle))
    sy = cy + int((r - 10) * math.sin(sec_angle))
    draw.line((cx, cy, sx, sy), fill="red", width=1)

    # Digital time
    digital_time = now.strftime("%H:%M:%S")
    text_bbox = draw.textbbox((0, 0), digital_time, font=font)
    text_w = text_bbox[2] - text_bbox[0]
    text_x = (64 - text_w) // 2
    text_y = 128 + 4
    # Clear only the area for the digital time before drawing
    draw.rectangle((text_x, text_y, text_x + text_w, text_y + 10), fill=(32, 32, 32))
    draw.text((text_x, text_y), digital_time, fill="white", font=font)

    return img

# --- Main Loop ---
try:
    # Create the static background once
    background = create_background(city)
    while dartsnut.running:
        frame = background.copy() # Start with a copy of the background
        if tz_info:
            now_dt = datetime.datetime.now(tz_info)
            frame = draw_clock_hands(frame, now_dt)

        dartsnut.update_frame_buffer(frame)
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
print("simple_clock_128_160 exiting...")