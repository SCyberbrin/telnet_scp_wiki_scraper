import socket
from src import LOGO

from src.telnet_io import readline, sendline

def textFrame(texts: str, frame_symble: str = "@") -> str:
    maxText: int = 0

    finishedOutput: str

    for text in texts.splitlines():
        if len(text) > maxText:
            maxText = len(text)

    _texts = [f"{frame_symble} {i.center(maxText)} {frame_symble}" for i in texts.splitlines()]
        
    longFrames = f"\n{frame_symble * (maxText + 4)}\n"
    finishedOutput = longFrames + "\n".join(_texts) + longFrames

    return finishedOutput

def fake_login(conn: socket.socket, is_echo_off: bool):
    sendline(conn, LOGO)

    sendline(conn, textFrame("WARNING: THE FOUNDATION DATABASE IS CLASSIFIED!"))


    message = """ACCESS BY UNAUTHORIZED PERSONNEL IS STRICTLY PROHIBITED
PERPETRATORS WILL BE TRACKED, LOCATED, AND DETAINED"""

    sendline(conn, textFrame(message))



    sendline(conn, "LOGIN: ")
    while True:
        sendline(conn, "USER> ", newline="")
        username = readline(conn, is_echo_off)
        
        if username:
            break
        
        sendline(conn, "\r\nPlease enter your Username!")

    while True:
        sendline(conn, "\n\rPASS> ", newline="")
        password = readline(conn, False)
        
        if password:
            sendline(conn, "")
            break
        
        sendline(conn, "\r\nPlease enter a valid Password!")

    sendline(conn, "ACCESS GRANTED")
    sendline(conn, "Welcome")
