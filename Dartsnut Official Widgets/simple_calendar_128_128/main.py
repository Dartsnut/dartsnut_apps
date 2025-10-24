import calendar
from pydartsnut import Dartsnut
import time
from PIL import Image, ImageDraw, ImageFont

dartsnut = Dartsnut()

# Image and Calendar dimensions
WIDTH, HEIGHT = 128, 128
CALENDAR_WIDTH, CALENDAR_HEIGHT = 128, 128

# Calendar layout calculations
WEEKDAYS = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
CELL_W = CALENDAR_WIDTH // 7 - 1
CELL_H = (CALENDAR_HEIGHT - 16) // 7
LEFT_MARGIN = (CALENDAR_WIDTH - CELL_W * 7) // 2
HEADER_HEIGHT = 16

# Colors
BG_COLORS = ['#222244', '#223344', '#224455', '#225566', '#226677', '#227788', '#228899']
WEEKDAY_COLORS = ['#FF6666', '#FFCC66', '#66FF66', '#66CCFF', '#6666FF', '#CC66FF', '#FF66CC']

# Initialize Image and Font
img = Image.new('RGB', (WIDTH, HEIGHT), 'black')
draw = ImageDraw.Draw(img)
font = ImageFont.load_default()

def draw_the_calendar(year, month, today_mday):
    """Draws the calendar for the given year and month."""
    # Clear the calendar area and draw background stripes
    draw.rectangle((0, 0, CALENDAR_WIDTH, CALENDAR_HEIGHT), fill='black')
    for i in range(7):
        draw.rectangle([LEFT_MARGIN + i*CELL_W, 0, LEFT_MARGIN + (i+1)*CELL_W, CALENDAR_HEIGHT], fill=BG_COLORS[i])

    # Draw grid lines
    for i in range(8):
        draw.line([(LEFT_MARGIN + i*CELL_W, HEADER_HEIGHT), (LEFT_MARGIN + i*CELL_W, CALENDAR_HEIGHT)], fill='gray')
    for i in range(8):
        draw.line([(LEFT_MARGIN, HEADER_HEIGHT + i*CELL_H - 1), (LEFT_MARGIN + 7*CELL_W, HEADER_HEIGHT + i*CELL_H - 1)], fill='gray')

    # Draw month/year title
    title = f"{year}-{month:02d}"
    title_width = draw.textlength(title, font=font)
    draw.text(((CALENDAR_WIDTH - title_width) // 2, 2), title, fill='white', font=font)

    # Draw weekday headers
    for i, wd in enumerate(WEEKDAYS):
        draw.text((LEFT_MARGIN + i*CELL_W + 2, HEADER_HEIGHT), wd, fill='white', font=font)

    # Draw the days of the month
    cal = calendar.monthcalendar(year, month)
    for row, week in enumerate(cal):
        for col, day in enumerate(week):
            if day == 0:
                continue

            x = LEFT_MARGIN + col * CELL_W + 2
            y = HEADER_HEIGHT + (row + 1) * CELL_H
            
            if day == today_mday:
                # Highlight today
                ellipse_bbox = [x - 2, y - 2, x + 14, y + 12]
                draw.ellipse(ellipse_bbox, fill="yellow")
                draw.text((x, y), f"{day:2d}", fill="black", font=font)
            else:
                # Draw other days with an outline for visibility
                text_fill = WEEKDAY_COLORS[col]
                outline_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                for ox, oy in outline_offsets:
                    draw.text((x + ox, y + oy), f"{day:2d}", fill="black", font=font)
                draw.text((x, y), f"{day:2d}", fill=text_fill, font=font)

# --- Main Loop ---
try:
    while dartsnut.running:
        now = time.localtime()
        draw_the_calendar(now.tm_year, now.tm_mon, now.tm_mday)
        dartsnut.update_frame_buffer(img)
        time.sleep(60)
except KeyboardInterrupt:
    pass

print("simple_calendar_128_128 exiting...")