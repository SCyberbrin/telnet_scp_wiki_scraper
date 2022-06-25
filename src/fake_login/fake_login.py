import socket

from src.uis.uis import readline

def fake_login(conn: socket.socket):
    conn.send(b"LOGIN: \n\r")
    while True:
        conn.send(b"USER> ")
        username = readline(conn)
        
        if username:
            break
        
        conn.send(b"\r\nPlease enter your Username!\r\n")

    while True:
        conn.send(b"PASS> ")
        password = readline(conn, False)
        
        if password:
            conn.send(b"\n\r")
            break
        
        conn.send(b"\r\nPlease enter a valid Password!\r\n")

    conn.send(b"ACCESS GRANTED\r\n")
    conn.send(b"Welcome \r\n")
