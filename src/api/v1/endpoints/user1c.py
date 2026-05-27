from typing import List
from fastapi import APIRouter, HTTPException,status, Body
from tortoise.exceptions import DoesNotExist
import datetime as dt

from src.models.serure_objects import SecurityObject, SecurityObject_Pydantic
from src.services.sites import Sites
from pydantic import BaseModel
# from src.crud.sites import crud_create_sites,crud_get_sites,crud_get_sites_user_id,crud_get_sites_search,crud_get_site_id,crud_update_data
from src.crud.loading import loading_file_streem1c
from tortoise.timezone import now

router = APIRouter(prefix="/user1c", tags=["sites"])



testData = [{'Телефон': '79128916406', 'НомерДоговора': '7416-175', 'Баланс': '0', 'СуммаКОплате': '123.40', 'СистемаОплаты': 0, 'Действует': 1}, {'Телефон': '+79655460743', 'НомерДоговора': '639/СП', 'Баланс': '0', 'СуммаКОплате': '', 'СистемаОплаты': 0, 'Действует': 1}, {'Телефон': '2252626', 'НомерДоговора': '7426-968/СБ', 'Баланс': '0', 'СуммаКОплате': '', 'СистемаОплаты': 1, 'Действует': 1}, {'Телефон': '+73514492171', 'НомерДоговора': '7422-556/СБ', 'Баланс': '-4200.00', 'СуммаКОплате': '4200.00', 'СистемаОплаты': 0, 'Действует': 1}, {'Телефон': '+73514492171', 'НомерДоговора': '429/СП', 'Баланс': '-525.00', 'СуммаКОплате': '525.00', 'СистемаОплаты': 0, 'Действует': 1}, {'Телефон': '+79127742849', 'НомерДоговора': '7426-5367', 'Баланс': '-2838.72', 'СуммаКОплате': '2200.00', 'СистемаОплаты': 1, 'Действует': 1}, {'Телефон': '+79995875709', 'НомерДоговора': '7424-620/СБ', 'Баланс': '-15750.00', 'СуммаКОплате': '5250.00', 'СистемаОплаты': 0, 'Действует': 1}, {'Телефон': '+79120519598', 'НомерДоговора': '9626-1735', 'Баланс': '-2668.00', 'СуммаКОплате': '2898.00', 'СистемаОплаты': 1, 'Действует': 1}, {'Телефон': '+73512814204', 'НомерДоговора': '7426-971/СБ', 'Баланс': '0', 'СуммаКОплате': '3150.00', 'СистемаОплаты': 1, 'Действует': 1}, {'Телефон': '+73512236320', 'НомерДоговора': '7426-972/СБ', 'Баланс': '-806.66', 'СуммаКОплате': '', 'СистемаОплаты': 1, 'Действует': 1}, {'Телефон': '+79630787839', 'НомерДоговора': '640/СП', 'Баланс': '0', 'СуммаКОплате': '', 'СистемаОплаты': 1, 'Действует': 1}, {'Телефон': '+73517298484', 'НомерДоговора': '8/2026', 'Баланс': '-2100.00', 'СуммаКОплате': '', 'СистемаОплаты': 0, 'Действует': 1}, {'Телефон': '+79123085111', 'НомерДоговора': '7426-5372', 'Баланс': '0', 'СуммаКОплате': '', 'СистемаОплаты': 1, 'Действует': 1}]


@router.post("/data")
async def get_objects(data = Body()):
    """
    Получить список всех объектов
    """ 
    # print(f"{dt.date.today()} - {dt.datetime.now()}")
    print(data)

    newData = []

    for item in data: 
        if isinstance(item, dict):
            data_c = {}
            def clean_decimal(val):
                if val == '' or val is None:
                    return "0.00"
                return str(val).replace(',', '.')
            data_c['phone'] = item.get('Телефон')
            data_c['dogovor'] = item.get('НомерДоговора')
            data_c['dolg'] = clean_decimal(item.get('Баланс'))
            data_c['pay'] = clean_decimal(item.get('СуммаКОплате'))
            data_c['pre_pay'] = item.get('СистемаОплаты')
            data_c['bill_status'] = item.get('Действует')
            # data_c['date'] = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
            data_c['date'] = now().replace(microsecond=0) 


            newData.append(data_c)


    await loading_file_streem1c(newData)
    # print(newData)


    # for item in data:
    #     print(type(item), item)
    #     print(f"Номер договора {item.get('НомерДоговора')} - Баланс {item.get('Баланс')}")

    # try:
    #     sites = Sites()
    #     data = await sites.getSite()
    #     return data
    # except DoesNotExist:
    #     raise HTTPException(status_code=404, detail="Object not found")


# def transform_1c_data(testData):
#     newData = []
#     for item in testData:
#         if isinstance(item, dict):
#             # Наша логика очистки
#             phone = item.get('Телефон', '')
#             if phone.startswith(('+7', '+8', '8')):
#                 phone = '7' + (phone[2:] if phone.startswith('+') else phone[1:])
            
#             data_c = {
#                 'phone': phone,
#                 'dogovor': item.get('НомерДоговора'),
#                 'dolg': item.get('Баланс') if item.get('Баланс') != '' else '0.00',
#                 # ... остальные поля
#             }
#             newData.append(data_c)
#     return newData