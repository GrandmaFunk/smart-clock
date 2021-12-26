import time
from unicornhatmini import UnicornHATMini
from datetime import datetime
import threading
import signal

from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials

import pandas as pd
import pytz
import pickle


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
          [0,6], [1,6], [2,6]],
    '6': [
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

def update_memo(today):

    # Read the CSV file
    df = pd.read_csv('memos.csv')
    df['date'] = pd.to_datetime(df.date, format='%m/%d/%Y')
    df.set_index(df.date, inplace=True)
    df['memo'] = df.memo.ffill()

    # Get today's memo
    #TODO: Error handle this
    memo = df.loc[today.strftime('%Y-%m-%d')].memo

    try:
        last_memo = pickle.load(open('logs/last_memo.p', 'rb'))
    except FileNotFoundError:
        last_memo = None
    
    if last_memo != memo:
        #TODO: Write the memo to Firebase
        print(memo)
        pass

def on_blink(doc, changes, read_time):
    global blink
    blink = doc[0].to_dict()
    print(blink)
    blink = blink['status']
    callback_done.set()
        
def show_blink():

    global blink

    while True:
        if blink:
            # Show a green pixel going up and down the middle of the display
            for i in range(7):
                clock.set_pixel(8, i, 0, 200, 0)
                clock.show()
                time.sleep(.1)
                clock.set_pixel(8, i, 0, 0, 0)
                time.sleep(.1)
            for i in range(5, 0, -1):
                clock.set_pixel(8, i, 0, 200, 0)
                clock.show()
                time.sleep(.1)
                clock.set_pixel(8, i, 0, 0, 0)
                time.sleep(.1)
        else:
            # Show the standard two dots to separate hours and minutes
            clock.set_pixel(8, 2, 70, 0, 0)
            clock.set_pixel(8, 4, 70, 0, 0)
            clock.show()
            time.sleep(.5)
            clock.set_pixel(8, 2, 0, 0, 0)
            clock.set_pixel(8, 4, 0, 0, 0)
            clock.show()
            time.sleep(.5)

def set_time(time_to_set, brightness):
    for pos, val in enumerate(time_to_set):
        if pos == 0:
            offset = 0
        elif pos == 1:
            offset = 4
        elif pos == 2:
            offset = 10
        elif pos == 3:
            offset = 14
        for pixel in numbers[val]:
            if not (pos == 0 and val == '0'):
                x = pixel[0] + offset
                y = pixel[1]
                clock.set_pixel(x,y, brightness,0,0)

def refresh_clock():
    middle_on = True
    est = pytz.timezone('US/Eastern')
    old_date = datetime(2000, 1, 1)
    old_time = '0000'

    while True:
        
        # Get the current time
        current_date = est.localize(datetime.now())
        current_time = datetime.now().strftime('%I%M')

        # Check if the date has changed
        if current_date.date() != old_date.date():
            print('New day...')
            update_memo(current_date)

        #TODO: Remove the leading 0 for times 1 through 9

        # Check if new time
        if current_time != old_time:
            set_time(old_time, 0)
            set_time(current_time, 200)

        # Set old values to compare
        time.sleep(5)
        old_date = current_date
        old_time = current_time


# Connect to Firestore
cred = credentials.Certificate('.secrets/key.json')
firebase_admin.initialize_app(cred)
db = firestore.Client()

# Create display
clock = UnicornHATMini()
clock.set_rotation(180)
clock.set_brightness(0.1)

# Set vars
blink = False

#TODO: Handle buttons
#TODO: Send messages

clock_thread = threading.Thread(target = refresh_clock)

# Start thread to listen to Firestore changes
callback_done = threading.Event()
blink_ref = db.collection(u'memos').document(u'blink')
blink_watch = blink_ref.on_snapshot(on_blink)

# Start thread to show time
clock_thread.start()

# Blink the middle section of the clock
show_blink()

