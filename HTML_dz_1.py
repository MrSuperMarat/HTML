# 1. Посмотреть документацию к API GitHub, разобраться как вывести
# список репозиториев для конкретного пользователя, сохранить
# JSON-вывод в файле *.json.

import requests
import json
from pprint import pprint

path = 'https://api.github.com/users/MrSuperMarat/repos'

response = requests.get(path)
j_data = response.json()
repos = [j_data[i]['name'] for i in range(len(j_data))]
print(repos)

with open('repos.json', 'w', encoding='UTF-8') as f:
    json.dump(j_data, f)

# 2. Изучить список открытых API
# (https://www.programmableweb.com/category/all/apis). Найти среди
# них любое, требующее авторизацию (любого типа). Выполнить запросы к
# нему, пройдя авторизацию. Ответ сервера записать в файл.
# Если нет желания заморачиваться с поиском, возьмите API вконтакте
# (https://vk.com/dev/first_guide). Сделайте запрос, чтобы получить
# список всех сообществ на которые вы подписаны.

path_flickr = f'https://www.flickr.com/services/rest/?method=flickr.' \
         f'galleries.getPhotos&api_key=c473e4cfab72f334511de9ad' \
         f'4f9f09c6&gallery_id=66911286-72157647277042064&forma' \
         f't=json&nojsoncallback=1'

resp_flickr = requests.get(path_flickr)
j_flickr = resp_flickr.json()
print(resp_flickr.text)
pprint(j_flickr)

with open('flickr.json', 'w', encoding='UTF-8') as f:
    json.dump(j_flickr, f)
