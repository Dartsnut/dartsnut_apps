import calendar
from pydartsnut import Dartsnut
import time
from PIL import Image, ImageDraw, ImageFont

dartsnut = Dartsnut()

# image size
WIDTH, HEIGHT = 128, 128
# caldendar size
CALENDAR_WIDTH, CALENDAR_HEIGHT = 128, 128
# calendar data
now = time.localtime()
year, month = now.tm_year, now.tm_mon
# week title
weekdays = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
cell_w = CALENDAR_WIDTH // 7 - 1
cell_h = (CALENDAR_HEIGHT - 16) // 7
left_margin = (CALENDAR_WIDTH - cell_w * 7) // 2

# init image
img = Image.new('RGB', (WIDTH, HEIGHT), 'black')
draw = ImageDraw.Draw(img)
# colors
bg_colors = ['#222244', '#223344', '#224455', '#225566', '#226677', '#227788', '#228899']
weekday_colors = ['#FF6666', '#FFCC66', '#66FF66', '#66CCFF', '#6666FF', '#CC66FF', '#FF66CC']

def draw_the_calendar():
    # clear the calendar area
    draw.rectangle((0, 0, CALENDAR_WIDTH-1, CALENDAR_HEIGHT-1), fill='black')
    # background stripe
    for i in range(7):
        draw.rectangle([left_margin + i*cell_w, 0, left_margin + (i+1)*cell_w, CALENDAR_HEIGHT-1], fill=bg_colors[i % len(bg_colors)])
    # dividers
    for i in range(8):
        draw.line([(left_margin + i*cell_w, 16), (left_margin + i*cell_w, CALENDAR_HEIGHT-1)], fill='gray')
    for i in range(8):
        draw.line([(left_margin, 16 + i*cell_h-1), (left_margin + 7*cell_w, 16 + i*cell_h-1)], fill='gray')
    # fonts
    font = ImageFont.load_default()
    #get the time
    now = time.localtime()
    year, month = now.tm_year, now.tm_mon
    # title
    title = f"{year}-{month:02d}"
    draw.text((CALENDAR_WIDTH//2 - len(title)*3, 2), title, fill='white', font=font)

    for i, wd in enumerate(weekdays):
        draw.text((left_margin + i*cell_w + 2, 16), wd, fill='white', font=font)

    # obtain month calendar
    cal = calendar.monthcalendar(year, month)
    today = time.localtime()
    for row, week in enumerate(cal):
        for col, day in enumerate(week):
            if day != 0:
                x = left_margin + col * cell_w + 2
                y = 16 + (row+1) * cell_h
                color = weekday_colors[col % len(weekday_colors)]  # Use weekday color
                # Highlight today
                if day == today.tm_mday and month == today.tm_mon and year == today.tm_year:
                    # Draw a filled ellipse behind today's date
                    ellipse_bbox = [x-2, y-2, x+14, y+12]
                    draw.ellipse(ellipse_bbox, fill="yellow")
                    text_fill = "black"
                    # Draw today's date without outline
                    draw.text((x, y), f"{day:2d}", fill=text_fill, font=font)
                else:
                    text_fill = color
                    # Draw a black outline for better visibility
                    outline_offsets = [(-1,0), (1,0), (0,-1), (0,1)]
                    for ox, oy in outline_offsets:
                        draw.text((x+ox, y+oy), f"{day:2d}", fill="black", font=font)
                    draw.text((x, y), f"{day:2d}", fill=text_fill, font=font)

# display
try:
    while True:
        if now.tm_mday != year or now.tm_mon != month or now.tm_year != year:
            draw_the_calendar()
        dartsnut.update_frame_buffer(img)
        time.sleep(0.5)

except KeyboardInterrupt:
    print("simple_demo exiting...")