import pystray
import time
import threading

from PIL import Image, ImageDraw


def create_image(width, height, color1, color2):
    # Generate an image and draw a pattern
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)

    return image

img0 = create_image(64, 64, 'black', 'white')
img1 = create_image(64, 64, 'white', 'black')


# In order for the icon to be displayed, you must provide an icon



# To finally show you icon, call run
x = False
def update_icon(icon):
    global x

    while 1:
        x = not x
        icon.icon = img0 if x else img1
        time.sleep(1)

icon = pystray.Icon('test name')
thread = threading.Thread(target=update_icon, args=(icon,))
thread.start()
icon.run()
