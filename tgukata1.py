"""Напишите код, который получает список названия школ
города Кемерово с помощью библиотеки vk_api
и записывает результаты в файл JSON"""


import requests
import json

ACCESS_TOKEN = "vk1.a._LMiXisBGkw94jiEzp3mxmhIJfv2_A2v3XKKVKKO9Cmo9zIiz3lt6iVEw1hJB_UTbGOpWt0_xioLn_HVPrPctCALADPZvHNOh_QmtDPh7rGWHBgReeXNL4FpVurEiWWSLDYjj4pi5WohLakCs1JMFXDDufsVnxwo3yYyiWy-j7ihzCorvj2FqY1Zbc9uoLmI"


"""city_id"""
METHOD_NAME = 'database.getCities'
URL = f'https://api.vk.com/method/{METHOD_NAME}'

params = {
    "access_token": ACCESS_TOKEN,
    "country_id": 1,
    "q": "Кемерово",
    "count": 1,
    "v": 5.131
}

city = requests.get(URL, params=params).json()
if city.get("response"):
    city_id = city["response"]["items"][0]["id"]
else:
    error_message = city.get("error")
    print(f"Ошибка на стадии нахождения id города: {error_message}")

# print(city)
# print(city_id)


"""список школ"""
METHOD_NAME = 'database.getSchools'
URL = f'https://api.vk.com/method/{METHOD_NAME}'

params = {
    "access_token": ACCESS_TOKEN,
    "country_id": 1,
    "city_id": city_id,
    "v": 5.131
}

res = requests.get(URL, params=params).json()
# print(res)
if res.get("response"):
    result_list = []
    items = res["response"]["items"]
    if items:
        for item in items:
            result_list.append(item['title'])
            """идентификатор школы, название"""

            with open("SchoolsKata1.json", mode="w", encoding="utf-8") as f:
                result = {"result": result_list}
                json.dump(result, f, ensure_ascii=False)
else:
    error_message = res.get("error")
    print(f"ERROR: {error_message}")

