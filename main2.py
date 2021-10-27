from webcam import Webcam
from detection import Detection
import time
import pygame
import thread

import numpy as np
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
from datetime import datetime
import os



def playNotes(cellNo = 0):
    lcd.set_cursor(8,1)
    lcd.message(display_list[cell])
    pianoNotes[cell].play()
    while pygame.mixer.music.get_busy == True:
        continue
    
    
pygame.mixer.init()


# Raspberry Pi pin configuration:
lcd_rs        = 21  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en        = 20
lcd_d4        = 16
lcd_d5        = 12
lcd_d6        = 7
lcd_d7        = 8
lcd_backlight = 16

previousNote = 8

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows)



# musical notes (C, D, E, F, G, A, B)
##NOTES = [262, 294, 330, 350, 393, 441, 494]
c1 = pygame.mixer.Sound('c1.wav')
d1 = pygame.mixer.Sound('d1.wav')
e1 = pygame.mixer.Sound('e1.wav')
f1 = pygame.mixer.Sound('f1.wav')
g1 = pygame.mixer.Sound('g1.wav')
a1 = pygame.mixer.Sound('a1.wav')
b1 = pygame.mixer.Sound('b1.wav')
##pianoNotes = [g1,f1,e1,d1,c1,b1,a1]
pianoNotes = [b1,a1,g1,f1,e1,d1,c1]

# initialise webcam and start thread
webcam = Webcam()
webcam.start()
 
# initialise detection with first webcam frame
image = webcam.get_current_frame()
detection = Detection(image) 
 
# initialise switch
switch = True

lcd.set_backlight(0)
lcd.clear()
lcd.show_cursor(False)
print "Virtual Piano"
lcd.message(' Virtual Piano ')
lcd.set_cursor(0,1)
lcd.message('Note =     ')
display_list=['B','A','G','F','E','D','C']

while True:
 
    # get current frame from webcam
    image = webcam.get_current_frame()
     
    # use motion detection to get active cell
    cell = detection.get_active_cell(image)
    if cell == None: continue
 
    # if switch on, play note
    if switch:
        print cell
        
        if previousNote == cell and ((time.time() - time1) < 0.8):
            print 'Repeat'
        else:
            time1 = time.time()
            previousNote = cell
            thread.start_new_thread(playNotes,(cell,))
##            time.sleep(0.2)
     
    # alternate switch    
    switch = not switch
