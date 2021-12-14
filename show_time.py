import time
import sys
from colorsys import hsv_to_rgb
from PIL import Image, ImageDraw, ImageFont
from unicornhatmini import UnicornHATMini

numbers = numbers = {
    '0': [[0, 0], [1, 0], [2, 0],
          [0, 1],         [2, 1],
          [0, 2],         [2, 2],
          [0, 3],         [2, 3],
          [0, 4],         [2, 4],
          [0, 5],         [2, 5],
          [0, 6], [1, 6], [2, 6]],
    '1': [        [1, 0],
          [0, 1], [1, 1]        ,
                  [1, 2],
                  [1, 3],
                  [1, 4],
                  [1, 5],
          [0, 6], [1, 6], [2, 6]],
    '2': [
       [1,0],
[0,1],        [2,1],
              [2,2],
       [1,3],
[0,4],
[0,5],
[0,6], [1,6],[2,6]
],
    '3':[
[0,0], [1,0], [2,0],
              [2,1],
              [2,2],
[0,3], [1,3], [2,3],
              [2,4],
              [2,5],
[0,6], [1,6], [2,6]],
    '4': [
[0,0],        [2,0],
[0,1],        [2,1],
[0,2],        [2,2],
[0,3], [1,3], [2,3],
              [2,4],
              [2,5],
              [2,6]
    ],
    '5': [
[0,0], [1,0], [2,0],
[0,1],        
[0,2],
[0,3], [1,3], [2,3],
              [2,4],
[0,5],        [2,5],
[0,6], [1,6], [2,6]
],    '6': [
[0,0], [1, 0], [2, 0],
[0,1],
[0,2],
[0,3], [1,3], [2,3],
[0,4],        [2,4],
[0,5],        [2,5],
[0,6], [1,6], [2,6]],
    '7': [[0, 0], [1, 0], [2, 0],
                          [2, 1],
                          [2, 2],
                  [1, 3],
        [0, 4],
        [0, 5],
        [0,6]],
    '8': [[0, 0], [1, 0], [2, 0],
          [0, 1],         [2, 1],
          [0, 2],         [2, 2],
          [0, 3], [1, 3], [2, 3],
          [0, 4],         [2, 4],
          [0, 5],         [2, 5],
          [0, 6], [1, 6], [2, 6]],
    '9': [[0, 0], [1, 0], [2, 0],
          [0, 1],         [2, 1],
          [0, 2],         [2, 2],
          [0, 3], [1, 3], [2, 3],
                          [2, 4],
                          [2, 5],
                          [2, 6]],
    ':': [[1, 2],
    [1, 4]],
    '.': [[1, 6]]
}

clock = UnicornHATMini()

# Rotate text upside down
clock.set_rotation(180)

# # Get clock dimensions
# display_width, display_height = clock.get_shape()
# print('{} x {}'.format(display_width, display_height))

# Set brightness
clock.set_brightness(0.1)

# # Get font
# font = ImageFont.truetype('5x7.ttf', 8)
# text_width, text_height = font.getsize(text)

# # Create image
# img = Image.new('P', (display_width, display_height), 0)
# draw = ImageDraw.Draw(img)

# draw.text((0, -1), text, font=font, fill=255)

# offset_x = 0

# for i in range(1):
#     for y in range(display_height):
#         for x in range(display_width):
#             hue = (time.time() / 10.0) + (x / float(display_width * 2))
#             r, g, b = [int(c * 255) for c in hsv_to_rgb(hue, 1, 1)]
#             if img.getpixel((x + offset_x, y)) == 255:
#                 clock.set_pixel(x, y, r, g, b)
#             else:
#                 clock.set_pixel(x, y, 0, 0, 0)

#     offset_x += 1
#     if offset_x + display_width > img.size[0]:
#         offset_x = 0
#     clock.show()

#n = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
n = ['0', '1','2','3','5','4','6', '7', '8', '9', ':']
for number in n:
    for pixel in numbers[number]:
        x = pixel[0]
        y = pixel[1]
        clock.set_pixel(x,y, 255,0,0)
    clock.show()
    time.sleep(1)
    clock.clear()
# time.sleep(10)
# clock.clear()
# clock.show()
