import serial, colorama
import serial.tools.list_ports


def list_ports():
    all_ports = list(serial.tools.list_ports.comports())
    index = 0
    for port in all_ports:
        index+=1
        
        return [int(index), str(port), all_ports]

class pico_driver():
    def __init__(self, port: str):
        self.ser_connection = serial.Serial(port, 9600, parity=serial.PARITY_EVEN, timeout=1)

    def write_pico(self, val):
        
        
        #if len(val) >= 16:
        len_to_add = 16 - len(val)
        
        for i in range(len_to_add):
            val += " "
         
        self.ser_connection.write(str(val).encode())

    def read_pico(self):
        val = self.ser_connection.readline()
        return val

    def handshake(self):
        self.write_pico("HANDSHAKE") # Send value to pico running counter part script
        callback = self.strip_string(self.listen().decode("utf-8"))
        listend_messages = 0
        
        
        while 1:
            
            if callback == "HANDSHAKE":
                return True
            elif listend_messages == 100:
                return False
            else:
                listend_messages += 1

            

                

            
        
    def strip_string(self, string):
        string = string.strip("\r\n")
        return string
        
    def listen(self):
        data = self.read_pico()
        return data 
    def close(self):
        self.ser_connection.close()
        


# def connect_port(val):
#     return serial.Serial(val, 9600, parity=serial.PARITY_EVEN, timeout=1)

    


