import platform, os, csv
from typing import Union
import logging

class scp_cache_system:
    TMP_FOLDER = ""
    if platform.system() == "Linux" or platform.system() == "Darwin":
        TMP_FOLDER = "/tmp"
    elif platform.system() == "Windows":
        TMP_FOLDER = "C:\\TEMP"
    
    TMP_FILE = os.path.join(TMP_FOLDER, "scp_cache.tmp")
    
    def __init__(self) -> None:
        self.__create_exist()

    def exist(self, scp_num: str) -> bool:
        if self.__readLine(scp_num) == None:
            return False
        else:
            return True

    def add(self, scp_num: str, message: str) -> None:
        self.__create_exist()
        with open(self.TMP_FILE, "a", newline="") as f_stream:
            _writer = csv.writer(f_stream, delimiter=',',
                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            _writer.writerow([scp_num, message])

    def get(self, scp_num: str) -> str:
        data = self.__readLine(scp_num)
        if data == None:
            logging.error(f"scp cache {scp_num} not found!")
            raise Exception(f"scp cache {scp_num} not found!")
        return data[1]
            

    def __readLine(self, scp_num: str) -> Union[tuple[str, str], None]:
        self.__create_exist()
        with open(self.TMP_FILE, newline="") as f_stream:
            _reader = csv.reader(f_stream, delimiter=',', quotechar='"')

            for data in _reader:
                if data[0] == scp_num:
                    return (data[0], data[1])
        return None
    
    def __create_exist(self) -> None:
        if not os.path.exists(self.TMP_FILE):
            open(self.TMP_FILE, "x").close()

    def remove(self, scp_num: int) -> None:
        pass