#LIBRARYS
import time
from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C

#VARIABLES
sw0 = Pin(7, Pin.IN, Pin.PULL_UP) #setting pin on 9 as input.
sw1 = Pin(8, Pin.IN, Pin.PULL_UP) #setting pin on 7 as input.
sw2 = Pin(9, Pin.IN, Pin.PULL_UP) #setting pin on 7 as input.
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000) #setting i2c screen pins and it's frequancy
oled_width:int = 128 #how many pixels is on screen withing x-axis
oled_height:int = 64 #how many pixels is on screen withing y-axis
oled = SSD1306_I2C(oled_width, oled_height, i2c) #initializing oled

#left middle is width=0 and oled_height/2
x_pos: int = 0

y_pos_unclamped:int = 32
y_pos_clamped:int = 32

while True:
    if(sw1.value() == 0):
        x_pos = 0
        y_pos_clamped = y_pos_unclamped = 32 #wrap y_pos back to middle.
        oled.fill(0)
    
    if(y_pos_unclamped <= 0):
        y_pos_clamped = y_pos_unclamped = 0 # if new_pos is more or equal to min value clamp the value to minimum
    elif(y_pos_unclamped >= 63):
        y_pos_clamped = y_pos_unclamped = 63 # if new_pos is more or equal to min value clamp the value to maximum
    else:
        y_pos_clamped = y_pos_unclamped #if 'new_pos_x' is within min-max values set it's value to it.
    
    if(x_pos >= 128):
        x_pos = 0 #wrap x_pos back to left side.
        
    if(sw2.value() == 0):
        y_pos_unclamped += 1
        
    if(sw0.value() == 0):
        y_pos_unclamped -= 1
        
    x_pos += 1
    
    oled.pixel(x_pos, y_pos_clamped, 1) #assign new pixel to a position
    oled.show() #draw new pixel   