import re
import socket
import sys, getopt
import logging
from _thread import start_new_thread

from src import GITHUB, PORT, UNICODE, VERSION, LOGO
from src.fake_login.fake_login import fake_login
from src.web_extractors.scp_wiki_wikidot import scp_wiki_wikidot
from src.uis.uis import readline, textFrame, sendCommand
from src.cache_system import scp_cache_system

cache = scp_cache_system()

logging.basicConfig(level=logging.INFO,
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(sys.stdout)
    ],
    format='%(asctime)s:%(levelname)s: %(message)s')

def ask_command(conn: socket.socket) -> bool:
    conn.send(b"SCP> ")
    command = readline(conn)
    if re.search("quit", command):
        return True

    elif re.search("info", command):
        infomessage = f"""The SCP Foundation Telnet Protocol
Version: {VERSION}
Running on: ??????

{GITHUB}"""
        infomessage = infomessage.replace("\n", "\n\r")
        
        conn.send((infomessage + "\n\r").encode(UNICODE))

    else:
        temp = re.search(r'\d+', command)
        if temp:
            scp_num = temp.group()
            scp_num = scp_num.replace(" ", "-")
            if not cache.exist(scp_num):
                scp_client = scp_wiki_wikidot()
                text = scp_client.get_scp(scp_num)
                text = text.replace('\n', '\r\n')
                cache.add(scp_num, text)
            else:
                text = cache.get(scp_num)
            
            conn.send(text.encode(UNICODE, "replace"))
        else:
            conn.send("\r\nNot a valid SCP\r\n".encode(UNICODE))
    return False


def client_thread(conn: socket.socket): #threader client
    conn.send("If nothing happens then press enter!\r\n".encode(UNICODE))

    sendCommand(conn, bytearray([255, 254, 1]))

    conn.send(LOGO)

    conn.send(textFrame("WARNING: THE FOUNDATION DATABASE IS CLASSIFIED!").encode(UNICODE))

    message = """ACCESS BY UNAUTHORIZED PERSONNEL IS STRICTLY PROHIBITED
PERPETRATORS WILL BE TRACKED, LOCATED, AND DETAINED"""

    conn.send(textFrame(message).encode(UNICODE))

    fake_login(conn)

    conn.send("Type the nummber of the SCP your searching. \n Type 'info' for information about the client and 'quit' for disconnecting.\n\r".encode(UNICODE))
        
    while True:
        try:
            kill = ask_command(conn)
            if kill:
                break
        except Exception as e:
            logging.error(e)
            break
    conn.close()



def main (argv):
    port = PORT

    try:
        opts, args = getopt.getopt(argv,"t")
    except getopt.GetoptError:
        print('-t debug mode')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-t':
            # Test mode
            port = 5002

            logging.getLogger().setLevel(logging.DEBUG)
            logging.debug(f"port changed to {port}")




    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    logging.debug("Socket Created")

    try:
        server.bind(("", port))
        server.listen(0)
    except socket.error as e:
        logging.error(str(e))
        sys.exit()

    while True:
        try:
            conn, addr = server.accept()
            logging.info("Connected with " + addr[0] + ":" + str(addr[1]))
            start_new_thread(client_thread, (conn, ))
        except Exception as e:
            logging.error(e)
            break

    server.close()

