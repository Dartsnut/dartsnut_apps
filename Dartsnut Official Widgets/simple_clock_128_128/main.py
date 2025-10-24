from PIL import Image, ImageDraw, ImageFont
import math
import time
from pydartsnut import Dartsnut
import zoneinfo
import datetime
import requests

dartsnut = Dartsnut()
# Read the city from params
city_name = dartsnut.widget_params.get("city", "")
timezone_id = None
city = "Unknown"

if city_name:
    # This block runs only once at the start to get location data.
    # A retry loop is included for robustness.
    for _ in range(3): # Try up to 3 times
        try:
            resp = requests.get(
                "https://secure.geonames.org/searchJSON",
                params={"q": city_name, "maxRows": 1, "username": "dartsnut"},
                timeout=5
            )
            resp.raise_for_status()
            data = resp.json()
            if data.get("geonames"):
                geoname = data["geonames"][0]
                lat, lng = geoname["lat"], geoname["lng"]
                city = geoname["name"]
                
                tz_resp = requests.get(
                    "https://secure.geonames.org/timezoneJSON",
                    params={"lat": lat, "lng": lng, "username": "dartsnut"},
                    timeout=5
                )
                tz_resp.raise_for_status()
                timezone_id = tz_resp.json().get('timezoneId')
            break # Success, exit retry loop
        except requests.RequestException as e:
            print(f"Error fetching location data: {e}")
            time.sleep(2) # Wait before retrying

# Create timezone object once
tz = zoneinfo.ZoneInfo(timezone_id) if timezone_id else None

def create_background(city_name, has_timezone):
    """Creates the static background image for the clock."""
    bg = Image.new("RGB", (128, 128), "black")
    draw = ImageDraw.Draw(bg)

    if not has_timezone:
        # Display "City not found" message
        font = ImageFont.load_default(size=16)
        msg = "City not found"
        draw.text((64, 64), msg, fill="red", font=font, anchor="mm")
        return bg

    # Clock center and radius
    cx, cy, r = 64, 64, 60

    # Draw clock face (white outline)
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline="white", width=2)

    # Draw hour marks (white ticks)
    for i in range(12):
        angle = math.radians(i * 30)
        x1 = cx + int((r - 8) * math.sin(angle))
        y1 = cy - int((r - 8) * math.cos(angle))
        x2 = cx + int(r * math.sin(angle))
        y2 = cy - int(r * math.cos(angle))
        draw.line((x1, y1, x2, y2), fill="white", width=2)

    # Draw the city name at the bottom
    font = ImageFont.load_default()
    draw.text((64, 90), city_name, fill="lightgray", font=font, anchor="mt")
    
    return bg

def draw_clock_hands(img, now):
    """Draws the clock hands on the provided image."""
    draw = ImageDraw.Draw(img)
    cx, cy, r = 64, 64, 60

    hour = now.hour % 12
    minute = now.minute
    second = now.second

    # Hour hand (white)
    hour_angle = math.radians((hour + minute / 60) * 30 - 90)
    hx = cx + int((r - 28) * math.cos(hour_angle))
    hy = cy + int((r - 28) * math.sin(hour_angle))
    draw.line((cx, cy, hx, hy), fill="white", width=5)

    # Minute hand (gray)
    min_angle = math.radians((minute + second / 60) * 6 - 90)
    mx = cx + int((r - 16) * math.cos(min_angle))
    my = cy + int((r - 16) * math.sin(min_angle))
    draw.line((cx, cy, mx, my), fill="gray", width=3)

    # Second hand (red)
    sec_angle = math.radians(second * 6 - 90)
    sx = cx + int((r - 10) * math.cos(sec_angle))
    sy = cy + int((r - 10) * math.sin(sec_angle))
    draw.line((cx, cy, sx, sy), fill="red", width=1)

# --- Main Program ---

# Create the static background image once
background_image = create_background(city, bool(tz))

# Main display loop
try:
    while dartsnut.running:
        frame = background_image.copy()
        
        if tz:
            now = datetime.datetime.now(tz)
            draw_clock_hands(frame, now)

        dartsnut.update_frame_buffer(frame)
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
print("simple_clock_128_128 exiting...")