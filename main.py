import pystray
import time
import threading
import os
import re

from PIL import Image, ImageDraw, ImageFont


IMAGE_SIZE = (64, 64)
BACKGROUND_COLOR = '#000000'
FOREGROUND_COLOR = '#ff9900'
FONT = ImageFont.truetype("./Arial.ttf", 50)


def execp(cmd: str) -> str:
    lines = os.popen(cmd).readlines()
    assert lines
    return ''.join(lines)


def create_image(text: str):
    image = Image.new('RGB', IMAGE_SIZE, BACKGROUND_COLOR)
    dc = ImageDraw.Draw(image)
    dc.text(tuple(map(lambda x: x // 2, IMAGE_SIZE)), text, fill=FOREGROUND_COLOR, font=FONT, anchor='mm')
    return image

def create_images():
    output = execp('setxkbmap -query | grep layout:')
    regex_result = re.search(r'((\w+,?)+)$', output.strip())
    assert regex_result
    langs = regex_result.group(1).split(',')

    result = {}
    for lang in langs:
        result[lang] = create_image(lang)
    return result


def update_icon(icon):
    global x

    images = create_images()
    prev = ''
    while 1:
        output = execp(r'xset -q | grep LED | grep -P \\d{8} -o')
        lang_index = int(output) // 1000
        lang = list(images.keys())[lang_index]
        if lang != prev:
            prev = lang
            icon.icon = list(images.values())[int(output) // 1000]
        time.sleep(0.1)

icon = pystray.Icon('keyboard lang', create_image(''))

thread = threading.Thread(target=update_icon, args=(icon,))
thread.start()
icon.run()
