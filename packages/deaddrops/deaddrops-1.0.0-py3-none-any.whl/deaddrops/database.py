from bs4 import BeautifulSoup
import requests
import html
import re


class DatabaseHelper:
    def __init__(self):
        pass

    def getDatabaseStatistics(self) -> dict:
        database_statistics_dict = {}

        req = requests.get(f"https://deaddrops.com/db/")
        parse = BeautifulSoup(req.text, "lxml")

        database_statistics_dict.update(
            {
                "total_usb_drops": parse.find_all("table")[1]
                .find_all("tr")[1]
                .find_all("td")[1]
                .text
            }
        )
        database_statistics_dict.update(
            {
                "total_usb_storage": parse.find_all("table")[1]
                .find_all("tr")[2]
                .find_all("td")[1]
                .text
            }
        )

        return database_statistics_dict

    def getDatabaseContent(
        self, location: str = "", max_distance: int = 5000, amount: int = 99999
    ) -> dict:
        database_content_dict = {"results": {}}

        req = requests.get(
            f"https://deaddrops.com/db/?location={location}&maxdistance={max_distance}&pagelen={amount}&action=Search"
        )
        parse = BeautifulSoup(req.text, "lxml")

        for elem in parse.find_all("table")[3].find_all("tr"):
            actual_drop = elem.find_all("td")

            # Check if the first element corresponds to a date format, else garbage
            if not re.search(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$", actual_drop[0].text):
                continue

            actual_drop_data = {
                "date": actual_drop[0].text,
                "name": html.unescape(actual_drop[1].text),
                "permalink": "https://deaddrops.com/db/"
                + html.unescape(actual_drop[1].find("a", href=True).attrs["href"]),
                "location": {
                    "street": html.unescape(actual_drop[2].text),
                    "city": html.unescape(actual_drop[3].text),
                    "state": html.unescape(actual_drop[4].text),
                    "country": actual_drop[5].text,
                },
                "size": actual_drop[6].text,
                "status": actual_drop[7].find("div").get("title"),
            }

            actual_drop_id = re.search(
                r"\d+", actual_drop_data.get("permalink")[::-1]
            ).group()[::-1]

            database_content_dict["results"].update(
                {str(actual_drop_id): actual_drop_data}
            )

        return database_content_dict

    def searchTerm(
        self, database_content_dict: str, term: str, case_sensitive: bool = False
    ) -> dict:
        def __extract_dict_values(self, dictionary):
            result_list = ""

            for d in dictionary.items():
                if type(d[1]) is dict:
                    result_list += " " + self.__extract_dict_values(d[1])

                else:
                    result_list += " " + str(d[1])

            return result_list

        result_dict = {}

        for entry in database_content_dict.get("results"):
            content = self.__extract_dict_values(
                database_content_dict.get("results")[entry]
            )

            if (term.lower() if not case_sensitive else term) in (
                content.lower() if not case_sensitive else content
            ):
                result_dict.update(
                    {str(entry): database_content_dict.get("results")[entry]}
                )

        return result_dict
