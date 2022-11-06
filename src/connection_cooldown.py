from typing import Union
import socket
from datetime import datetime, timedelta


class cooldown_system:
    # USER STANDART: (time: datetime, ip: str)
    __USER_LIST:list[tuple[datetime, str]] = []


    def valid_user(self, conn: socket.socket, time_limit_minuts: int = 5) -> bool:

        conn_ip = conn.getsockname()[0]
        conn_row = self.__read_list(conn_ip)
        
        _time = datetime.now() + timedelta(minutes=time_limit_minuts) # Create time with extra 5 min
        
        if not conn_row: # If user doesnt exist in the list then add him
            self.__USER_LIST.append((_time, conn_ip))
            return True

        elif conn_row[0] <= datetime.now(): # If the user exist but has reached his limit
            self.__USER_LIST.remove(conn_row)
            
            self.__USER_LIST.append((_time, conn_ip))
            return True

    # If the user didnt reached his limit
        return False
            


    def __read_list(self, conn_ip: str) -> Union[tuple[datetime, str], None]:
        for user in self.__USER_LIST:
            if user[1] == conn_ip:
                return user

        return None
