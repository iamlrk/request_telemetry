import serial as pys
import time

def request_telemetry(port: str, board='CDH', encoding='utf-8'):
    """Send a telemetry request over seerial port to EduCube board

    ## Args:
        port (str): Port Name of the connected USB
        board (str): Name of the connected Board Defaults to 'CDH'
        encoding (str, optional): Type of encoding. Defaults to 'utf-8'.

    ## Returns:
        time, and telemetry values (str): Telemetry
    """
    _cmd = f"[C|{board.upper()}|T]"
    return port.write(_cmd.encode(encoding=encoding))

def record_educube_telmetry(port: str, telemetry_gap=1, encoding='utf-8'):
    """Request and write telemetry from EduCube

    ## Args:
        port (str): Port Name of connected USB
        telemetry_gap (int, optional): Time interval between requests. Defaults to 1.
        encoding (str, optional): Type of encoding. Defaults to 'utf-8'.
    """
    epochtime = int(time.time()) 
    readable_time = time.strftime("%d-%b-%Y-%H-%M-%S", time.gmtime(epochtime)) 
    _last_time = 0
    
    while True:
        _time=time.time()
        if _time - _last_time > telemetry_gap:
            request_telemetry(port)
            _last_time = _time
        
        _line = port.readline()
        if _line:
            with open(f"logs\{board}-{exp}-{readable_time}.txt", 'a') as log:
                log.write(_line.decode(encoding=encoding))

def record_comms(port, encoding='utf-8'):
    epochtime = int(time.time()) 
    readable_time = time.strftime("%d-%b-%Y-%H-%M-%S", time.gmtime(epochtime)) 
    
    with open(f"logs\{board}-{exp}-{readable_time}.txt", 'a') as log:
        while True:
            _line = port.readline()
            if _line:
                log.write(_line.decode(encoding=encoding))


if __name__ == '__main__':
    board = "ADC" 
    exp = "MPU_ACC_Diff_Pos"
    portname = "COM9"
    baudrate = 115200

    
    try:
        with pys.Serial(portname, baudrate, timeout=1) as port:
            record_educube_telmetry(port)
            # record_comms(port)
    except KeyboardInterrupt:
        pass