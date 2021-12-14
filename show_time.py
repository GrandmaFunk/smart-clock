import time
from unicornhatmini import UnicornHATMini
from datetime import datetime
import threading
import signal

from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials

numbers = {
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
    '2': [        [1,0],
            [0,1],      [2,1],
                        [2,2],
                  [1,3],
            [0,4],
            [0,5],
            [0,6], [1,6],[2,6]],
    '3':[[0,0], [1,0], [2,0],
                       [2,1],
                       [2,2],
         [0,3], [1,3], [2,3],
                       [2,4],
                       [2,5],
        [0,6],[1,6], [2,6]],
    '4': [[0,0],        [2,0],
          [0,1],        [2,1],
          [0,2],        [2,2],
          [0,3], [1,3], [2,3],
                        [2,4],
                        [2,5],
                        [2,6]],

    '5': [[0,0], [1,0], [2,0],
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
    [1, 4]]
}

cred = credentials.Certificate('.secrets/key.json')
firebase_admin.initialize_app(cred)
db = firestore.Client()

clock = UnicornHATMini()

# Rotate text upside down
clock.set_rotation(180)

# Set brightness
clock.set_brightness(0.1)

blink = False
ccr, ccg, ccb = 0, 255, 0

# def display_middle(blink):
#     if blink:
#         pass
#     else:

def on_blink(doc, changes, read_time):
    global ccr, ccb, ccg
    blink = doc[0].to_dict()
    print(blink)
    if blink['status']:
        ccr, ccg, ccb = 0, 255, 0
    else:
        ccr, ccg, ccb = 255, 0, 0
    callback_done.set()
        

def show_middle(middle_on):
    global ccr, ccb, ccg
    if middle_on:
        clock.set_pixel(8, 2, ccr, ccb, ccg)
        clock.set_pixel(8, 4, ccr, ccb, ccg)
        return False
    else:
        clock.set_pixel(8, 2, 0, 0, 0)
        clock.set_pixel(8, 4, 0, 0, 0)
        return True

def show_clock():
    middle_on = True
    while True:
        current_time = datetime.now().strftime('%I%M')
        for pos, val in enumerate(current_time):
            if pos == 0:
                offset = 0
            elif pos == 1:
                offset = 4
            elif pos == 2:
                offset = 10
            elif pos == 3:
                offset = 14
            for pixel in numbers[val]:
                x = pixel[0] + offset
                y = pixel[1]
                clock.set_pixel(x,y, 255,0,0)
        
        middle_on = show_middle(middle_on)
        clock.show()
        time.sleep(.5)
        clock.clear()


clock_thread = threading.Thread(target = show_clock)

callback_done = threading.Event()
blink_ref = db.collection(u'memos').document(u'blink')
blink_watch = blink_ref.on_snapshot(on_blink)

clock_thread.start()


