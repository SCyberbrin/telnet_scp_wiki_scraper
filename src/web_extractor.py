import requests
from bs4 import BeautifulSoup

URL = "https://the-scp.foundation/object/scp-"

def get_scp(scp_num: int):
    url = URL + str(scp_num).zfill(3)
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    body = soup.find("div", class_="the-content scp-content")
    return body.get_text()
