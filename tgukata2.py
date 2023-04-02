"""С помощью методов API «ВКонтакте» получите 1000 подписчиков группы «Лентач»,
отсортирванных по дате регистрации.
Вам необходимо собрать следующие данные в CSV файл: пол, название город,
семейное положение (ФИО партнера не указывать).
"""

import vk_api
import csv


ACCESS_TOKEN = "vk1.a._LMiXisBGkw94jiEzp3mxmhIJfv2_A2v3XKKVKKO9Cmo9zIiz3lt6iVEw1hJB_UTbGOpWt0_xioLn_HVPrPctCALADPZvHNOh_QmtDPh7rGWHBgReeXNL4FpVurEiWWSLDYjj4pi5WohLakCs1JMFXDDufsVnxwo3yYyiWy-j7ihzCorvj2FqY1Zbc9uoLmI"

# Инициализация сессии с помощью токена доступа
vk_session = vk_api.VkApi(token=ACCESS_TOKEN)
vk = vk_session.get_api()

group_id = vk.groups.search(q='Лентач', count=1)['items'][0]['id']
members_info = vk.groups.getMembers(group_id=group_id, sort='id_asc', fields="sex, city, relation", count=1000)['items']

result = []
for group in members_info:
    # 'id
    id = group['id']
    # 'sex
    if group['sex'] == 0:
        sex = 'пол не указан'
    elif group['sex'] == 1:
        sex = 'пол женский'
    elif group['sex'] == 2:
        sex = 'пол мужской'
    # 'city
    if group.get('city'):
        city = group.get('city', '').get('title')
    else:
        city = 'город не указан'
    # 'relation
    if group.get('relation'):
        relation = group.get('relation')
    else:
        relation = 'данные извлечь невозможно'
    # 'result
    result.append({
        'id': group['id'],
        'пол': sex,
        'город': city,
        'relation': relation
    })


# Запись данных в CSV файл
with open('LentachKata2.csv', mode='w', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=result[0].keys())
    writer.writeheader()
    for row in result:
        writer.writerow(row)


