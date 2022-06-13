import requests
from bs4 import BeautifulSoup, Tag, NavigableString
from typing import Union

class the_scp_foundation:
    URL = "https://the-scp.foundation/object/scp-"

    def get_scp(self, scp_num: int) -> str:
        url = self.URL + str(scp_num).zfill(3)
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        body = soup.find("div", class_="the-content scp-content")
        if not body:
            return "No SCP found\n\r"
        
        containment_procedures = self._get_scp_special_containment_procedures(body)
        description = self._get_scp_description(body)
        sidebar = self._get_scp_sidebar(body)

        if not containment_procedures or not description or not sidebar:
            return "No SCP found\n\r"

        return containment_procedures + "\n\n\r" + sidebar + description + "\n\r"


    def _get_scp_special_containment_procedures(self, content_body: Union[Tag, NavigableString]) -> Union[str, None]:
        containment_procedures = content_body.find("div", class_="scp-special-containment-procedures")
        if not containment_procedures:
            return None
        return containment_procedures.get_text()


    def _get_scp_description(self, content_body: Union[Tag, NavigableString]) -> Union[str, None]:
        description = content_body.find("div", class_="scp-description")
        if not description:
            return None
        return description.get_text()

    def _get_scp_sidebar(self, content_body: Union[Tag, NavigableString]) -> Union[str, None]:
        sidebar = content_body.find("aside", class_="scp-sidebar")
        if not sidebar:
            return None
        tags = ["@    " + i.find("span").get_text() + "\r\n" for i in sidebar.find_all('div', class_="scp-tag")]
        return "".join(tags)