import utime
import machine
from machine import I2C, Pin
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd



# 25 = LED 
# 39 SCREEN


class lcd():
    def __init__(self):
        I2C_ADDR = self.get_display_pin()
        I2C_NUM_ROWS = 2
        I2C_NUM_COLS = 16
        
        i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
        self.lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
    
    def get_display_pin(self):
        sda = machine.Pin(0)
        scl = machine.Pin(1)
        i2c = machine.I2C(0,sda=sda,scl=scl, freq=400000)
        
        if i2c.scan():
            print(i2c.scan())
            num =  i2c.scan()
            
            full_num = num[0]
            return int(full_num)
        else:
            print(i2c.scan())
            
            
                
    
    def display(self, pos, text: str):
        
        if len(text) > 16:
            
            self.lcd.clear()
            
            self.lcd.move_to(0,0)
            self.lcd.putstr("ERROR")

        else:
            self.lcd.clear()
            
            self.lcd.move_to(0,0)
            self.lcd.putstr(text)
            
program = lcd()
program.display((0,0), "hello")
    
    
    
    
    
    
    
    
    
    
    
    

