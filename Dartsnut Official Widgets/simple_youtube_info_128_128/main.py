from PIL import Image, ImageDraw, ImageFont
from pydartsnut import Dartsnut
import time
import asyncio
import aiohttp

dartsnut = Dartsnut()
# read the youtube channel id from params
youtube_channel_id = dartsnut.widget_params.get("youtube_channel_id", "")
# read the item to be displayed from params
category = dartsnut.widget_params.get("category", "subscribers")
# read the api key from params
api_key = dartsnut.widget_params.get("api_key", "")
if api_key == "":
    # use default api key
    api_key = "AIzaSyCqMz97dRrG3TBXxUGvvEdHFPVolZoaCSA"

# prepare images
current_image = Image.new("RGB", (128, 128), (0, 0, 0))
background_image = Image.open("youtube_bg_128_128.png").convert("RGB")
draw = ImageDraw.Draw(current_image)
font_26 = ImageFont.truetype("./helvetica-compressed.otf", 26)
font_36 = ImageFont.truetype("./helvetica-compressed.otf", 36)

# init values
channel_name, subscriber_count, views_count, concurrent_viewers = None, None, None, None

async def get_live_concurrent_viewers(channel_id):
    global concurrent_viewers
    try:
        search_url = "https://www.googleapis.com/youtube/v3/search"
        search_params = {
            "part": "snippet",
            "channelId": channel_id,
            "eventType": "live",   # only live streams
            "type": "video",
            "maxResults": 1,
            "key": api_key,
        }

        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(search_url, params=search_params) as resp:
                resp.raise_for_status()
                data = await resp.json()

            items = data.get("items", [])
            if items:
                live_video_id = items[0]["id"]["videoId"]

                videos_url = "https://www.googleapis.com/youtube/v3/videos"
                videos_params = {
                    "part": "liveStreamingDetails",
                    "id": live_video_id,
                    "key": api_key,
                }

                async with session.get(videos_url, params=videos_params) as resp2:
                    resp2.raise_for_status()
                    data2 = await resp2.json()

                items2 = data2.get("items", [])
                if not items2:
                    concurrent_viewers = None
                else:
                    live = items2[0].get("liveStreamingDetails", {})
                    viewers = live.get("concurrentViewers")
                    concurrent_viewers = int(viewers) if viewers is not None else None
            else:
                concurrent_viewers = None
    except Exception as e:
        print(f"Error fetching YouTube data: {e}")
        concurrent_viewers = None

async def get_youtube_info(channel_id):
    global channel_name, subscriber_count, views_count
    try:
        url = "https://www.googleapis.com/youtube/v3/channels"
        params = {
            "part": "snippet,statistics",
            "id": channel_id,
            "key": api_key
        }

        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                data = await response.json()

        if "items" in data and len(data["items"]) > 0:
            channel_info = data["items"][0]
            channel_name = channel_info["snippet"]["title"]
            subscriber_count = int(channel_info["statistics"]["subscriberCount"])
            views_count = int(channel_info["statistics"]["viewCount"])
        else:
            channel_name, subscriber_count, views_count = None, None, None
    except Exception as e:
        print(f"Error fetching YouTube data: {e}")
        channel_name, subscriber_count, views_count = None, None, None

def format_number(count):
    if count < 1000000:
        return str(count)
    elif count < 100000000:
        return f"{count // 1000}K"
    elif count < 100000000000:
        return f"{count // 1000000}M"
    else:
        return f"{count // 1000000000}B"
    
async def update_youtube_info_loop():
    while dartsnut.running:
        await get_youtube_info(youtube_channel_id)
        if category == "live_viewers":
            await get_live_concurrent_viewers(youtube_channel_id)
        await asyncio.sleep(10)  # Update every 10 seconds

async def render_loop():
    while dartsnut.running:
        try:
            # draw the background
            current_image.paste(background_image, (0, 0))

            if category in ["subscribers", "views"]:
                if category == "subscribers" and subscriber_count is not None:
                    # draw the number
                    formatted_count = format_number(subscriber_count)
                    draw.text((8, 54), formatted_count, font=font_36, fill=(255, 255, 255))
                    # draw the text
                    draw.text((8, 28), "Subscribers", font=font_26, fill=(175, 171, 171))
                else:
                    if views_count is not None:
                        # draw the number
                        formatted_count = format_number(views_count)
                        draw.text((8, 54), formatted_count, font=font_36, fill=(255, 255, 255))
                        # draw the text
                        draw.text((8, 28), "Total Views", font=font_26, fill=(175, 171, 171))
            elif category == "live_viewers":
                if concurrent_viewers is not None:
                    # draw the number
                    formatted_count = format_number(concurrent_viewers)
                    draw.text((8, 54), formatted_count, font=font_36, fill=(255, 255, 255))
                    # draw the text
                    draw.text((6, 28), "Live Viewers", font=font_26, fill=(175, 171, 171))
                else:
                    draw.text((8, 54), "Offline", font=font_36, fill=(255, 255, 255))
                    draw.text((6, 28), "Live Viewers", font=font_26, fill=(175, 171, 171))

            if channel_name is not None:
                text_bbox = draw.textbbox((0, 0), channel_name, font=font_36)
                text_width = text_bbox[2]
                text_y = 90
                
                if text_width > 128:
                    # Scroll just enough to reveal full text, then bounce back
                    scroll_speed = 20  # pixels per second
                    max_shift = text_width - 128  # amount needed to fully reveal
                    t = (time.time() * scroll_speed) % (2 * max_shift)
                    offset = t if t <= max_shift else (2 * max_shift - t)  # triangle wave 0..max_shift..0
                    text_x = -int(offset)
                    draw.text((text_x, text_y), channel_name, font=font_36, fill=(255, 32, 32))
                else:
                    # Center the text if it fits
                    text_x = (128 - text_width) // 2
                    draw.text((text_x, text_y), channel_name, font=font_36, fill=(255, 32, 32))

            dartsnut.update_frame_buffer(current_image)
        except Exception as e:
            print(f"Error in render loop: {e}")
        
        await asyncio.sleep(0.1)

# Start the async loops
async def main():
    await asyncio.gather(
        update_youtube_info_loop(),
        render_loop()
    )

asyncio.run(main())