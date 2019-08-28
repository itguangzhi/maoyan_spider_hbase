import requests
import json
def getCityList():
    # 拿到城市列表信息
    cities_list = []
    city_list_url = "https://maoyan.com/ajax/cities"
    city_list = requests.get(url=city_list_url).json()
    for city_list_A in city_list["letterMap"]:
        cities_list.extend(city_list["letterMap"][city_list_A])
    return cities_list

def getCinemaList(cityid:str):
    m = "http://m.maoyan.com/ajax/cinemaList?day=2019-08-22&offset=0&limit=999&cityId="
    cinema_list_url = m+cityid
    res = requests.get(url=cinema_list_url).json()
    try:
        return res["cinemas"]
    except:
        return []



