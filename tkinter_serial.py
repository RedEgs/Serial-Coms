import tkinter as tk
from tkinter import ttk
import threading
from tkinter import messagebox
import serial, time
import serial.tools.list_ports
import pico_serial
     
        
class App:
    def __init__(self, root):
        self.root = root
        #setting title
        root.title("Serial Communication Testing Tool")
        #setting window size
        root.geometry("300x320")
        title_label=tk.Label(root, text="Serial Communication Tool", 
                             justify="center", font=("Segoe UI", 14))
        title_label.place(relx=0.5,rely=0.05,width=300,height=20, anchor=tk.CENTER)
        
        ports_label=tk.Label(root, text="List of available ports", 
                             justify="center", font=("Segoe UI", 8))
        ports_label.place(relx=0.5,rely=0.11,width=200,height=20, anchor=tk.CENTER)
        
        connected_label=tk.Label(root, text="Not Connected: None", 
                             justify="center", font=("Segoe UI", 8))
        connected_label.place(relx=0.5,rely=0.57,width=200,height=20, anchor=tk.CENTER)
    
    
        port_index = 0
        self.element_selected = False
        self.ports_list = tk.Listbox(root, selectmode=tk.SINGLE)
        self.ports_list.place(relx=0.5, rely=0.38, width=250, height=150, anchor=tk.CENTER)
        self.reload_list(self.ports_list)
        
        reload_thread = threading.Thread(target=self.reload_thread)
        reload_thread.start()


        select_button = tk.Button(root, text="Select Port", command= lambda: self.on_select_button(self.ports_list))
        self.listen_thread_active = False
        self.listen_thread_exists = False
        #select_button.place(relx=0.5, rely=0.57, width=150, height=20, anchor=tk.CENTER)
        
        self.ports_list.bind("<<ListboxSelect>>", lambda event: self.on_list_select(self.ports_list, select_button))
        
        
        reload_button = tk.Button(root, text="R", command= lambda: self.reload_list(self.ports_list))
        reload_button.place(relx=0.13, rely=0.57, width=16, height=16, anchor=tk.CENTER)
                    
     
     
     
     
    def on_close_button(self):
        try:
            if self.listen_thread_active:
                self.listen_thread_active = False
                self.log_box.place_forget()
                
            self.ports_list.place(relx=0.5, rely=0.38, width=250, height=150, anchor=tk.CENTER)
            self.reload_list(self.ports_list)
            
            self.close_button.place_forget()
            self.connect_button.place_forget()
            self.listen_button.place_forget()
            self.command_button.place_forget()
            self.command_line.place_forget()
            
            
            
        except: pass
        
        
        
        try:
            self.driver.close()
        except AttributeError:
            messagebox.showwarning("NO CONNECTION", "You must connected to a port")
        
        
    def on_select_button(self, list: tk.Listbox):
        port_raw = list.get(self.sel[0])
        port_raw = port_raw[0:4]

        try:
            self.port_raw = port_raw
            self.driver = pico_serial.pico_driver(port_raw)
    
            
            if self.driver.handshake():
           
           
                self.command_button = tk.Button(root, text="Send", command=self.send_command)
                self.command_button.place(relx=0.83, rely=0.67, width=50, height=20, anchor=tk.CENTER)
                
                self.command_line_var = tk.StringVar()
                self.command_line = tk.Entry(root, textvariable=self.command_line_var)
                self.command_line.place(relx=0.4, rely=0.67, width=190, height=20, anchor=tk.CENTER)


                self.listen_button = tk.Button(root, text="Listen For Data", command= lambda: self.on_listen_select(list))
                self.listen_button.place(relx=0.5, rely=0.75, width=250, height=20, anchor=tk.CENTER)

                self.close_button = tk.Button(root, text="Close Connection", command=self.on_close_button)
                self.close_button.place(relx=0.5, rely=0.83, width=250, height=20, anchor=tk.CENTER)
            
                

                self.send_command = tk.Button(root, text="Connect")
     
       
            else:
                messagebox.showwarning("Device Unresponsive", "Device failed handshake")
           
           
           
        except serial.serialutil.SerialException as e:
            messagebox.showwarning("PORT WARNING", e)
        
       
       
    def send_command(self):
        print("hello")
        self.driver.write_pico(self.command_line_var.get())
        
        
        

    def listen_thread(self):
        self.listen_thread_active = True
        while 1:
            if self.listen_thread_active:
                self.log_box.insert(tk.END, self.driver.strip_string(self.driver.listen().decode("utf-8")) + "\n")
                time.sleep(0.5)
            else:
                pass
        
    def reload_thread(self):
        while 1:
            
            ports_list = pico_serial.list_ports()
            time.sleep(0.01)
           
            if ports_list != pico_serial.list_ports():
                self.reload_list(self.ports_list)
                
            
            
        
        
        
            
    def on_listen_select(self, list):
        list.place_forget()  
        
        self.log_box = tk.Text(self.root)
        self.log_box.place(relx=0.5, rely=0.38, width=250, height=150, anchor=tk.CENTER)
        
        time.sleep(.001)        
        
        if self.listen_thread_exists:
            self.listen_thread_active = True
        else:
            self.listen_thread_exists = True
            self.listen_thread = threading.Thread(target=self.listen_thread)
            self.listen_thread.start()
            
    
    
    
       
    def reload_list(self, list: tk.Listbox):
        list.delete(0, list.size())
            
            
        port_index = 0
        for port in pico_serial.list_ports()[2]:
            port_index +=1
            list.insert(port_index, port)
        
    def on_list_select(self, list: tk.Listbox, button):
        self.sel = list.curselection()
        if self.sel:
            button.place(relx=0.5, rely=0.57, width=150, height=20, anchor=tk.CENTER)
        
        
        
        
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
