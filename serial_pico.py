import select, sys, time, machine
import lcd_pico
from sys import stdin
import uselect

led =machine.Pin(25, machine.Pin.OUT)
led.value(0)




class pc_driver():
    def __init__(self, handshake_key):
        self.data_length = 16
        
        self.handshake_key = handshake_key
        self.handshake_len = len(self.handshake_key)
    
    def recieve_data(self):
        select_result = uselect.select([stdin], [], [], 0)

        buffer = ''
        return select_result, buffer

    def data_to_string(self):
        recv_result, recv_buffer = self.recieve_data()
            
        while recv_result[0]:
            recv_char = stdin.read(self.data_length)

            return recv_char
                
screen = lcd_pico.lcd()
driver = pc_driver("HANDSHAKE")
while 1:
    data = driver.data_to_string()
    if data:
        screen.display((0,0), data)
        data = None
        break