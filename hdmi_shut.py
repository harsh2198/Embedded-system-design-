
import time

import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
from datetime import datetime
import os
import subprocess


button = 2

GPIO.setup(button,GPIO.IN)

lcd_rs        = 21  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en        = 20
lcd_d4        = 16
lcd_d5        = 12
lcd_d6        = 7
lcd_d7        = 8
lcd_backlight = 16


# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,lcd_columns, lcd_rows)


main=True
t1 = datetime.now()
while GPIO.input(button) == False:
        t2 = datetime.now()
        delta = t2 - t1
        time_elapse = delta.total_seconds()
        if time_elapse > 8:
                reset = False
                main = False
                break

if main==True:
        os.system("sudo /tmp/userland/build/bin/tvservice -o")
        subprocess.call('vcgencmd display_power 0',shell=True)
    
elif main==False:
        lcd.clear()
        lcd.show_cursor(False)
        print "program terminated"
        lcd.message('program terminated')
      
