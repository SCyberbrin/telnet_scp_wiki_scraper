import socket

from src import UNICODE


def readline(conn: socket.socket, echo: bool = True) -> str:
    buf: str = ""
    while(True):
        mess = conn.recv(1024).decode(UNICODE)

        if echo and len(mess) <= 1:
            conn.send(mess.encode(UNICODE))

        buf += mess.strip()

        if mess.endswith('\r\n') or mess.endswith('\r') or mess.endswith('\n') or mess.endswith('\036'):
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