import time
import serial as pys


board = "Comms"
exp = "GPS-Outside"
portname = "COM10"
baudrate = 9600
epochtime = int(time.time()) 
readable_time = time.strftime("%d-%b-%Y-%H-%M-%S", time.gmtime(epochtime)) 

with pys.Serial(portname, baudrate, timeout = 1) as port:
        while True:
            _line = port.readline()
            if _line:
                with open(f"{board}-{exp}-{readable_time}.txt", 'a') as log:
                    # print("This is working!")
                    log.write(_line.decode(encoding='unicode_escape'))