import re
import socket
import sys
from _thread import start_new_thread
from src import PORT, UNICODE, VERSION
from src.fake_login.fake_login import fake_login

from src.web_extractors.scp_wiki_wikidot import scp_wiki_wikidot
from src.uis.uis import readline, textFrame


LOGO = b"""
                       JPYYYYYYYYYYYYYYPJ                       \r
                      :@5..............5@:                      \r
                    :!P@^              ^@P!:                    \r
                .!YPPY7:                :7YPPY!.                \r
              ^YG57:           77           :75GY^              \r
            ~PB?:           ..~@@~..           :?BP~            \r
          :P#7         :!JPB&@@@@@@&BPJ!:         7#P:          \r
         !&5.       :?G@@@#PY??@@??YP#@@@G?:       .5&!         \r
        ?@7       :5&@@P7:    .&&.    :7P@@&5:       7@?        \r
       ?@!       ?&@@Y:       .&&.       :Y@@&?       !@?       \r
      ^@J       Y@@B^       :PG@@GP:       ^B@@Y       J@^      \r
      P#.      ?@@B.         !@@@@!         .B@@?      .#P      \r
     .@Y      .&@@~           ^&&^           ~@@&.      Y@.     \r
     ^@!      ~@@B             ^^             B@@~      !@^     \r
     ^@!      ~@@B     :Y55PPG7  7GPP55Y:     B@@~      7@^     \r
     :@Y      .&@@~   .!#@@@@?    ?@@@@#!.   ~@@&.      Y@:     \r
   :JBP~       ?@@B~?G##57BB^      ^BB75##G?~B@@?       ~PBJ:   \r
  ~@G:         ^#@@@#7^   ..        ..   ^7#@@@#^         :G@~  \r
   !#7        7#GY&@&J:                  :J&@&YG#7        7#!   \r
    ^#Y        .  :5&@@P7:            :7P@@&5:  .        Y#^    \r
     .GG.           :?G@@@#PY?7777?YP#@@@G?:           .GG.     \r
       Y#^             :!JPB&@@@@@@&BPJ!:             ^#Y       \r
        7#!  .:~:           .::::::.           :~:.  !#7        \r
         ~#P5PP5G57:                        :75G5PP5P#~         \r
          :!^.  .!YPPY7^:              :^7YPPY!.  .^!:          \r
                    :!J5PP55YJJ??JJY55PP5J!:                    \r
                         .:^~!!!!!!~^:.                         \r
\n\r
"""



def ask_command(conn: socket.socket) -> bool:
    conn.send(b"SCP> ")
    command = readline(conn)
    if re.search("quit", command):
        return True

    elif re.search("info", command):
        infomessage = f"""The SCP Foundation Telnet Protocol
Version: {VERSION}
Running on: ??????"""
        infomessage = infomessage.replace("\n", "\n\r")
        
        conn.send(bytes(infomessage + "\n\r", UNICODE))

    else:
        temp = re.search(r'\d+', command)
        if temp:
            scp_num = temp.group()
            scp_num = scp_num.replace(" ", "-")
            scp_client = scp_wiki_wikidot()
            text = scp_client.get_scp(scp_num)
            text = text.replace('\n', '\r\n')
            conn.send(text.encode(UNICODE, "replace"))
        else:
            conn.send("Not a valid SCP\r\n".encode(UNICODE))
    return False


def client_thread(conn: socket.socket): #threader client
    conn.send(bytearray([255, 254, 1]))
    conn.recv(1024)


    conn.send(LOGO)

    conn.send(bytes(textFrame("WARNING: THE FOUNDATION DATABASE IS CLASSIFIED!"), UNICODE))

    message = """ACCESS BY UNAUTHORIZED PERSONNEL IS STRICTLY PROHIBITED
PERPETRATORS WILL BE TRACKED, LOCATED, AND DETAINED"""

    conn.send(bytes(textFrame(message), UNICODE))

    fake_login(conn)
        
    while True:
        try:
            kill = ask_command(conn)
            if kill:
                break
        except Exception as e:
            print(e)
            break
    conn.close()



def main ():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("Socket Created")

    try:
        server.bind(("", PORT))
        server.listen(0)
    except socket.error as e:
        print(str(e))
        sys.exit()

    while True:
        try:
            conn, addr = server.accept()
            print("Connected with " + addr[0] + ":" + str(addr[1]))
            start_new_thread(client_thread, (conn, ))
        except Exception as e:
            print(e)
            break

    server.close()

