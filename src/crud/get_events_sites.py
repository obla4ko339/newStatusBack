from src.models.surgard_event import SurgardEvent, EventCodes
from src.schemas.surgard_event import SurgardEventCreate
from sqlalchemy import desc, distinct, func, or_, and_, select
from sqlalchemy.orm import Session


from datetime import datetime
from src.core.sqlalchemy_engine import async_session_maker
from src.models.surgard_event_sa import SurgardEventSA

from tortoise import Tortoise
from src.core.db import TORTOISE_ORM


from datetime import datetime, timezone

# from src.models.surgard_event import SurgardEvent
from src.schemas.surgard_event import SurgardEventCreate
from datetime import datetime

# async def create_surgard_event(data: SurgardEventCreate):
#     print(f"Creating SurgardEvent with data: {data}")
#     try:
#         event_data = data.dict() if hasattr(data, "dict") else data

#         # Убираем tzinfo, если есть
#         if event_data.get("datetime") and isinstance(event_data["datetime"], datetime):
#             if event_data["datetime"].tzinfo is not None:
#                 print("🕓 Удаляю tzinfo у datetime")
#                 event_data["datetime"] = event_data["datetime"].replace(tzinfo=None)

#         async with async_session_maker() as session:
#             event = SurgardEventSA(**event_data)
#             session.add(event)
#             await session.commit()
#             await session.refresh(event)

#         print(f"✅ SurgardEvent created with ID: {event.id}")
#         return event

#     except Exception as e:
#         print(f"❌ Error creating SurgardEvent: {e}")
#         raise
 

async def get_all_events__filter(id:int, filter_obj:object):
    try:
        
        print(f"filter {filter_obj}")

        dataStart = datetime.fromisoformat(filter_obj.get('startDate'))
        stopDate = datetime.fromisoformat(filter_obj.get('stopDate'))
        ectAlarm = filter_obj.get("ectAlarm")
        ectFault = filter_obj.get("ectFault")
        ectTest = filter_obj.get("ectTest")
        ectArm = filter_obj.get("ectArm")
        
        account_str = f"{id:04d}"
       
        async with async_session_maker() as session:
            # Создаем запрос с использованием select()
            query = select(SurgardEventSA).where(
                SurgardEventSA.account_number == account_str
            )
            
            # Добавляем фильтр по датам
            if dataStart and stopDate:
                query = query.where(
                    and_(
                        SurgardEventSA.datetime >= dataStart,
                        SurgardEventSA.datetime <= stopDate
                    )
                )

            
            
            # Выполняем запрос
            result = await session.execute(query)
            events = result.scalars().all()

            
        

        # print(events)
        
        event_codes = list(set([event.event_code for event in events if event.event_code]))
            
        # Получаем описания кодов из Tortoise ORM
        all_codes = await EventCodes.all().values('code', 'description_ru', 'description_en', 'group_category')
        code_map = {item['code']: item for item in all_codes}
        
        # Формируем результат - преобразуем объекты в словари
        result_list = []
        for event in events:
            # Преобразуем SQLAlchemy объект в словарь
            event_dict = {
                'id': event.id,
                'account_number': event.account_number,
                'event_type': event.event_type,
                'event_code': event.event_code,
                'group_code': event.group_code,
                'zone_or_user': event.zone_or_user,
                'datetime': event.datetime.isoformat() if event.datetime else None,
                'raw': event.raw,
                'created_at': event.created_at.isoformat() if event.created_at else None,
            }
            
            # Добавляем описание кода
            code_info = code_map.get(event.event_code)
            if code_info:
                event_dict.update({
                    'description_ru': code_info['description_ru'],
                    'description_en': code_info['description_en'], 
                    'group_category': code_info['group_category'],
                })
            
            result_list.append(event_dict)
        
        # Тревоги
        if ectAlarm == False:
            new_result_list = []
            for filterResult in result_list:
                if filterResult.get("group_category") != "Тревоги":
                    new_result_list.append(filterResult)
            result_list = new_result_list
            
        # Тревоги
        if ectFault == False:
            new_result_list = []
            for filterResult in result_list:
                if filterResult.get("group_category") != "Неисправности":
                    new_result_list.append(filterResult)
            result_list = new_result_list

        # Тестовые
        if ectTest == False:
            new_result_list = []
            for filterResult in result_list:
                if filterResult.get("group_category") != "Тестовые":
                    new_result_list.append(filterResult)
            result_list = new_result_list

        # Снятия/Постановки
        if ectArm == False:
            new_result_list = []
            for filterResult in result_list:
                if filterResult.get("group_category") != "Снятия/Постановки":
                    new_result_list.append(filterResult)
            result_list = new_result_list

        print(f"Returning {len(result_list)} events as dictionaries") 
        return result_list
    except Exception as e:
        print(f"❌ Error get events: {e}") 
        raise


async def get_event_by_account(account_number: str):
    return await SurgardEvent.filter(account_number=account_number).all()