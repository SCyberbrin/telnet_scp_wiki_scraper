import re
import socket
import sys
from _thread import start_new_thread

from src.web_extractors.scp_wiki_wikidot import scp_wiki_wikidot

PORT = 5001

UNICODE = "ansi"

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

def readline(conn: socket.socket) -> str:
    line = ""
    while True:
        data = conn.recv(8)
        line += data.decode(UNICODE)
        if not data or b"\r\n" in data:
            break
    return line


def ask_command(conn: socket.socket) -> bool:
    conn.send(b"SCP> ")
    command = readline(conn)
    if re.search("quit", command):
        return True
    else:
        temp = re.search(r'\d+', command)
        if temp:
            scp_num = temp.group()
            scp_num = scp_num.replace(" ", "-")
            scp_client = scp_wiki_wikidot()
            text = scp_client.get_scp(scp_num)
            text = text.replace('\n', '\r\n')
            conn.send(text.encode(UNICODE))
        else:
            conn.send("Not a valid SCP\r\n".encode(UNICODE))
        return False


def client_thread(conn: socket.socket): #threader client
    conn.send(LOGO)

    frame_symble = "@"

    warning = frame_symble + " WARNING: THE FOUNDATION DATABASE IS CLASSIFIED! " + frame_symble
    conn.send((frame_symble * len(warning)).encode(UNICODE) + b"\n\r")
    conn.send(warning.encode(UNICODE) + b"\n\r")
    conn.send((frame_symble * len(warning)).encode(UNICODE) + b"\n\r")
    conn.send(b"\n\r")

    message = f"{frame_symble} ACCESS BY UNAUTHORIZED PERSONNEL IS STRICTLY PROHIBITED {frame_symble}"
    message1 = "PERPETRATORS WILL BE TRACKED, LOCATED, AND DETAINED".center(len(message) - 2)
    message1 = frame_symble + message1 + frame_symble

    conn.send((frame_symble * len(message)).encode(UNICODE) + b"\n\r")
    conn.send(message.encode(UNICODE) + b"\n\r")
    conn.send(message1.encode(UNICODE) + b"\n\r")
    conn.send((frame_symble * len(message)).encode(UNICODE) + b"\n\r")
        
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

  
