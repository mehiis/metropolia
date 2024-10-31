#LIBRARYS
from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C

#VARIABLES
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000) #setting i2c screen pins and it's frequancy
oled_width:int = 128 #how many pixels is on screen withing x-axis
oled_height:int = 64 #how many pixels is on screen withing y-axis
oled = SSD1306_I2C(oled_width, oled_height, i2c) #initializing oled

words:list = [] #list variable of written words
max_words_on_screen: int = 64/8 #screen lenght divided by the size of the characters

#LOGIC
while True:
    oled.fill(0) #clears screen
    
    line:int = 0 #null lines
    new_word:string = input("Write a word: ")
    words.append(new_word); #add just writen word to a list.
    
    if(max_words_on_screen < len(words)): #check if there is more words that the screen can handle(8) and remove one if it is the case.
        words.pop(0) #remove the first word typed on the list.
    
    for word in words: #loop through all words in the list and display them on the oled-screen.
        oled.text(word, 0, line, 1) #add word in the list of words
        line += 8 #add offset to next word with lenght of the size of the character 8px.
        
    oled.show() #show words added to oled.text.