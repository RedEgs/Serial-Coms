import serial, time
import serial.tools.list_ports
import pico_serial
     
       
opt  = """RedEgs' Serial Communication tool
1. Connect to ports
2. Listen to ports
3. Send command to port
        """
        
pico_serial.list_ports()
driver = pico_serial.pico_driver("COM4")    
       
       
while 1: 
    print(opt)
    opt_input = input("> ")
    
    if opt_input == "1":
        print()
        driver.handshake()
        print()
        
    elif opt_input == "2":
        print()
        while 1:
            print(driver.listen())
            time.sleep(1)
            
    elif opt_input == "3":
        print()
        command = input("Your command: ")#
        driver.write_pico(command)
        print()
