import time
import sys
from colorsys import hsv_to_rgb
from PIL import Image, ImageDraw, ImageFont
from unicornhatmini import UnicornHATMini

text = 'Hello World'

clock = UnicornHATMini()

#TODO: See what this does
clock.set_rotation(0)

display_width, display_height = clock.get_shape()
print('{} x {}'.format(display_width, display_height))

clock.set_brightness(0.1)

font = ImageFont.truetype('5x7.ttf', 8)

text_width, text_height = font.getsize(text)

img = Image.new('P', (text_width + display_width + display_width, display_height), 0)
draw = ImageDraw.Draw(img)

draw.text((display_width, -1), text, font=font, fill=255)

offset_x = 0

while True:
    for y in range(display_height):
        for x in range(display_width):
            hue = (time.time() / 10.0) + (x / float(display_width * 2))
            r, g, b = [int(c * 255) for c in hsv_to_rgb(hue, 1, 1)]
            if img.getpixel((x + offset_x, y)) == 255:
                clock.set_pixel(x, y, r, g, b)
            else:
                clock.set_pixel(x, y, 0, 0, 0)

    offset_x += 1
    if offset_x + display_width > img.size[0]:
        offset_x = 0
    clock.show()
    time.sleep(0.05)
