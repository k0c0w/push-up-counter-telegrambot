from datetime import datetime
import time

import database

DaysLeft = (datetime(day=1, month= 9, year= 2022) - datetime.now()).days
def calculate():
    global DaysLeft
    while True:
        print(DaysLeft)
        database.update_users_aim()
        time.sleep(86400)
        DaysLeft = (datetime(day=1, month=9, year=2022) - datetime.now()).days
        if(DaysLeft == 0 ):
            DaysLeft = 1
            break