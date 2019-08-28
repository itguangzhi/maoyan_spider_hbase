import requests

class Util:

    def __init__(self):
        pass

    def downloader(self, url):
        res = requests.get(url=url)
        return res.json()

    def getCityList(self):
        city_list_url = ""
        return self.downloader(city_list_url)

    def getCinemaList(self):
        cinema_list_url = ""
        return self.downloader(cinema_list_url)

