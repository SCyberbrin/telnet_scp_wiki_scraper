import socket

from src import UNICODE

def readline(conn: socket.socket, echo: bool = True) -> str:
    """There are terminals that return only if the enter button is pressed and
    terminals that return if any button is been pressed."""
    
    buf: str = ""
    while(True): # TODO: Test on windows terminal
        mess = conn.recv(1024)

        # print(mess)
        # print(codecs.encode(mess, "hex"))

        str_mess = mess.decode(UNICODE)

        if echo and len(str_mess) <= 1: # TODO: REMOVE LATER IF NOT NEEDED
            pass
            # conn.send(mess.encode(UNICODE))

        
        buf += str_mess.strip()
        

        if b'\r\n' in mess or b'\r' in mess or b'\n' in mess:
            break
    return buf

def sendCommand(conn: socket.socket, command: bytearray) -> bool:
    conn.send(command)
    mess = conn.recv(1024)
    if command in mess:
        return True
    return False

def textFrame(texts: str, frame_symble: str = "@") -> str:
    maxText: int = 0

    finishedOutput: str

    for text in texts.splitlines():
        if len(text) > maxText:
            maxText = len(text)

    _texts = [f"{frame_symble} {i.center(maxText)} {frame_symble}" for i in texts.splitlines()]
        

    longFrames = "\n\r" + (frame_symble * (maxText + 4)) + "\n\r"
    finishedOutput = longFrames + "\n\r".join(_texts) + longFrames

    return finishedOutput