import socket

from src import UNICODE

# telnet commands
IAC = b'\xFF'

WILL = b'\xFB'
WONT = b'\xFC'

DO = b'\xFD'
DONT = b'\xFE'

ECHO = b'\x01'


def readline(conn: socket.socket, echo: bool = True) -> str:
    """There are terminals that return only if the enter button is pressed and
    terminals that return if any button is been pressed."""
    
    buf: str = ""
    while(True): # TODO: Test on windows terminal
        mess = conn.recv(1024)

        str_mess = mess.decode(UNICODE)

        if echo and len(str_mess) <= 1: # TODO: REMOVE LATER IF NOT NEEDED
            conn.send(mess)

        
        buf += str_mess.strip()
        

        if b'\r\n' in mess or b'\r' in mess or b'\n' in mess:
            break
    return buf

def sendline(conn: socket.socket, message: str, newline: str = "\n\r") -> None:
    message = message.replace("\n", "\n\r")
    
    _message = f"\r{message}{newline}"
    
    conn.send(_message.encode(UNICODE))

def echoOff(conn: socket.socket) -> bool:
    conn.send(bytearray([255, 254, 1]))
    mess = conn.recv(1024)
    if WONT in mess:
        return True
    
    return False


def sendCommand(conn: socket.socket, command: bytearray) -> bool:
    conn.send(command)
    mess = conn.recv(1024)
    info = [mess[i:i+3] for i in range(0, len(mess), 3)]
    print(mess)
    print(info)
    if command in mess:
        return True
    return False