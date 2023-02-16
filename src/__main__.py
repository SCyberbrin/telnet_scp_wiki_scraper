import re
import socket
import sys, getopt
import logging
import threading

from src import GITHUB, PORT, VERSION
from src.fake_login.fake_login import fake_login
from src.web_extractors.scp_wiki_wikidot import scp_wiki_wikidot
from src.telnet_io import echoOff, readline, sendline
from src.cache_system import scp_cache_system
from src.connection_cooldown import cooldown_system

cold_sys = cooldown_system()
cache = scp_cache_system()

logging.basicConfig(level=logging.INFO,
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(sys.stdout)
    ],
    format='%(asctime)s:%(levelname)s: %(message)s')

def ask_command(conn: socket.socket, is_echo_off: bool) -> bool:
    sendline(conn, "SCP> ", newline="")
    command = readline(conn, is_echo_off)
    if re.search("quit", command):
        return True

    elif re.search("info", command):
        infomessage = f"""The SCP Foundation Telnet Protocol
Version: {VERSION}
Running on: ??????

{GITHUB}
Source: scp-wiki.wikidot.com"""
        
        sendline(conn, infomessage)

    else:
        temp = re.search(r'\d+', command)
        if temp:
            scp_num = temp.group()
            scp_num = scp_num.replace(" ", "-")
            if not cache.exist(scp_num):
                scp_client = scp_wiki_wikidot()
                text = scp_client.get_scp(scp_num)
                cache.add(scp_num, text)
            else:
                text = cache.get(scp_num)
            
            sendline(conn, text)

        else:
            sendline(conn, "Not a valid SCP")
    return False


class ClientThread(threading.Thread):
    def __init__(self, conn: socket.socket):
        threading.Thread.__init__(self)
        self.conn: socket.socket = conn

    def run(self):
        sendline(self.conn, "If nothing happens then press enter!")

        is_echo_off = echoOff(self.conn)

        fake_login(self.conn, is_echo_off)


        sendline(self.conn, "Type the nummber of the SCP your searching.\nType 'info' for information about the client and 'quit' for disconnecting.")


        while True:
            try:
                kill = ask_command(self.conn, is_echo_off)
                if kill:
                    break
            except Exception as e:
                logging.error(e)
                break
        self.conn.close()



def main (argv):
    port = PORT

    try:
        opts, args = getopt.getopt(argv,"td")
    except getopt.GetoptError:
        print('-t debug mode\n-d disable cooldown system (for debug only)')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-t':
            # Test mode
            port = 5002

            logging.getLogger().setLevel(logging.DEBUG)
            logging.debug("Debug mode on")
            logging.debug(f"port changed to {port}")


        if opt == '-d':
            # Disable cooldown_system
            cold_sys.disable()
            logging.debug("cooldown_system is down")




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
            if not cold_sys.valid_user(conn): # Checks if users cooldown limit has reached
                sendline(conn, "Please be patient with your request, you haven't reached your 5 minutes cooldown!\nPlease come back next time.")
                conn.close()
                logging.info(f"{addr[0]}:{str(addr[1])} didn't reach cooldown (Disconnected)")
                continue
            
            thread = ClientThread(conn)
            thread.start()
        except Exception as e:
            logging.error(e)
            break

    server.close()

