from distutils.filelist import findall
import requests
from bs4 import BeautifulSoup, Tag, NavigableString
from typing import Union

class scp_wiki_wikidot:
    URL = "https://scp-wiki.wikidot.com/scp-"

    def get_scp(self, scp_id: str) -> str:
        scp_id = scp_id.lower()
        
        url = self.URL + scp_id
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")


        title = self.get_title(soup)
        content = self.get_content(soup)

        if not title or not content:
            return "No SCP found\n\r"
        
        return title + "\n\n\r" + content + "\n\r"

    def get_title(self, body: BeautifulSoup) -> Union[str, None]:
        title = body.find("div", id="page-title")
        if not title:
            return None
        return title.get_text(strip=True)

    def get_content(self, body: BeautifulSoup) -> Union[str, None]:
        content = body.find("div", id="page-content")
        if not content or content == NavigableString:
            return None

        for div in content.findChildren("div", recursive=False):
            div.decompose()

        return content.get_text()
