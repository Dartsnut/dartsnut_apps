import calendar
from pydartsnut import Dartsnut
import time
from PIL import Image, ImageDraw, ImageFont

# --- Constants ---
# Image and layout
WIDTH, HEIGHT = 128, 160
CALENDAR_WIDTH, CALENDAR_HEIGHT = 128, 128

# Calendar grid calculation
CELL_W = CALENDAR_WIDTH // 7
CELL_H = (CALENDAR_HEIGHT - 16) // 7
LEFT_MARGIN = (CALENDAR_WIDTH - CELL_W * 7) // 2

# Weekday labels
WEEKDAYS = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']

# Colors
BG_COLORS = ['#222244', '#223344', '#224455', '#225566', '#226677', '#227788', '#228899']
WEEKDAY_COLORS = ['#FF6666', '#FFCC66', '#66FF66', '#66CCFF', '#6666FF', '#CC66FF', '#FF66CC']
CLOCK_BG_COLOR = "#111122"
CLOCK_FG_COLOR = "cyan"
TODAY_BG_COLOR = "yellow"
TODAY_FG_COLOR = "black"

# Fonts (loaded once)
try:
    # Using a specific TrueType font is recommended for better control
    FONT_CALENDAR = ImageFont.truetype("arial.ttf", 10)
    FONT_CLOCK = ImageFont.truetype("arial.ttf", 15)
except IOError:
    # Fallback to default fonts if specific fonts are not found
    FONT_CALENDAR = ImageFont.load_default()
    FONT_CLOCK = ImageFont.load_default(size=15)


def draw_the_calendar(draw, now):
    """Draws the calendar for the given month and year."""
    year, month, today_mday = now.tm_year, now.tm_mon, now.tm_mday

    # Clear the calendar area
    draw.rectangle((0, 0, CALENDAR_WIDTH, CALENDAR_HEIGHT), fill='black')

    # Background stripes and grid lines
    for i in range(7):
        draw.rectangle([LEFT_MARGIN + i*CELL_W, 0, LEFT_MARGIN + (i+1)*CELL_W, CALENDAR_HEIGHT], fill=BG_COLORS[i])
        draw.line([(LEFT_MARGIN + (i+1)*CELL_W, 16), (LEFT_MARGIN + (i+1)*CELL_W, CALENDAR_HEIGHT)], fill='gray')
    for i in range(8):
        draw.line([(LEFT_MARGIN, 16 + i*CELL_H), (LEFT_MARGIN + 7*CELL_W, 16 + i*CELL_H)], fill='gray')

    # Title (e.g., "2023-10")
    title = f"{year}-{month:02d}"
    title_bbox = draw.textbbox((0, 0), title, font=FONT_CALENDAR)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text(((CALENDAR_WIDTH - title_w) // 2, 2), title, fill='white', font=FONT_CALENDAR)

    # Weekday headers
    for i, wd in enumerate(WEEKDAYS):
        draw.text((LEFT_MARGIN + i*CELL_W + 4, 16), wd, fill='white', font=FONT_CALENDAR)

    # Calendar days
    cal = calendar.monthcalendar(year, month)
    for row, week in enumerate(cal):
        for col, day in enumerate(week):
            if day == 0:
                continue

            x = LEFT_MARGIN + col * CELL_W + 2
            y = 16 + (row + 1) * CELL_H
            day_str = f"{day:2d}"

            if day == today_mday:
                # Highlight today
                ellipse_bbox = [x - 2, y - 2, x + 14, y + 12]
                draw.ellipse(ellipse_bbox, fill=TODAY_BG_COLOR)
                draw.text((x, y), day_str, fill=TODAY_FG_COLOR, font=FONT_CALENDAR)
            else:
                # Draw other days with an outline for visibility
                text_fill = WEEKDAY_COLORS[col]
                draw.text((x, y), day_str, fill=text_fill, font=FONT_CALENDAR,
                          stroke_width=1, stroke_fill="black")

def draw_the_clock(draw, now):
    """Draws the digital clock."""
    current_time = time.strftime("%H:%M:%S", now)
    clock_box = (0, 128, 63, 159)
    draw.rectangle(clock_box, fill=CLOCK_BG_COLOR)

    # Center the time text in its box
    bbox = draw.textbbox((0, 0), current_time, font=FONT_CLOCK)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    text_x = clock_box[0] + (clock_box[2] - clock_box[0] - w) // 2
    text_y = clock_box[1] + (clock_box[3] - clock_box[1] - h) // 2
    draw.text((text_x, text_y), current_time, fill=CLOCK_FG_COLOR, font=FONT_CLOCK)

"""Main application loop."""
dartsnut = Dartsnut()
img = Image.new('RGB', (WIDTH, HEIGHT), 'black')
draw = ImageDraw.Draw(img)
last_drawn_day = -1

try:
    while dartsnut.running:
        now = time.localtime()

        # Redraw calendar only when the day changes
        if now.tm_mday != last_drawn_day:
            draw_the_calendar(draw, now)
            last_drawn_day = now.tm_mday

        # Always redraw the clock
        draw_the_clock(draw, now)

        dartsnut.update_frame_buffer(img)
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    print("simple_calendar_128_160 exiting...")
