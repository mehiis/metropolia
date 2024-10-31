#LIBRARYS
from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C

#VARIABLES
sw0 = Pin(7, Pin.IN, Pin.PULL_UP) #setting pin on 7 as input. 
sw2 = Pin(9, Pin.IN, Pin.PULL_UP) #setting pin on 9 as input.
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000) #setting i2c screen pins and it's frequancy
oled_width:int = 128 #how many pixels is on screen withing x-axis
oled_height:int = 64 #how many pixels is on screen withing y-axis
oled = SSD1306_I2C(oled_width, oled_height, i2c) #initializing oled

x_pos_unclamped: int = 0 #temp valuable that checks new position and helps to clamp the x_pos to borders
x_pos_clamped:int = 0 #sets UFO:s clamped position

min_x: int = 0 #minimum x-value that ufo can go to.
max_x: int = 128 - (8*3) #maximum x-value that ufo can go to. 128 meaning full width of the screen. - offset the ufo(8px per character) (3 chars)

ufo_speed:int = 8 #how quickly ufo travels through screen

#LOOP
while True:
    oled.fill(0) #fills all pixels on oled screen with input 0 aka clears the screen.
    
    if(x_pos_unclamped <= min_x):
        x_pos_clamped = x_pos_unclamped = min_x # if new_pos is more or equal to min value clamp the value to minimum
    elif(x_pos_unclamped >= max_x):
        x_pos_clamped = x_pos_unclamped = max_x # if new_pos is more or equal to min value clamp the value to maximum
    else:
        x_pos_clamped = x_pos_unclamped #if 'new_pos_x' is within min-max values set it's value to it.
        
    
    if(sw0.value() == 0): #if sw0 button pressed add 'ufo_speed' to x_new_pos
        x_pos_unclamped += ufo_speed
        
    if(sw2.value() == 0): #if sw2 button pressed add 'ufo_speed' to x_new_pos
        x_pos_unclamped -= ufo_speed
    
    oled.text('<=>', x_pos_clamped, 32, 1) #set ufo with xpos of 'x_pos' y: 32 and 1 means active pixels.
    oled.show() #update ufos news position on the screen.
