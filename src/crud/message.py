from src.models.surgard_event import SurgardEvent
from src.schemas.surgard_event import SurgardEventCreate
from sqlalchemy import desc, distinct, func, or_
from sqlalchemy.orm import Session

from datetime import datetime
from src.core.sqlalchemy_engine import async_session_maker
from src.models.surgard_event_sa import SurgardEventSA

from tortoise import Tortoise
from src.core.db import TORTOISE_ORM


from datetime import datetime, timezone

from src.models.surgard_event import SurgardEvent
from src.models.user import User
from src.models.sites_user import SitesUser
from src.models.notification import Notification
from src.models.notification_is_read import NotificationIsRead
from src.schemas.surgard_event import SurgardEventCreate
from src.schemas.user import CreateUser
from src.schemas.notification import CreateMessage,DataMessageApi
from datetime import datetime

from tortoise.exceptions import IntegrityError
from fastapi import HTTPException

from src.crud.customers import getCustomersPhone, getSitesCustomers
from src.crud.sites_of_user import create_site_of_user_reg
from src.crud.auth import crud_get_list_user_ids


async def crud_check_is_read_message(user_id:int):
    if user_id:
        try:
            isMessage = await NotificationIsRead.filter(user_id=user_id, is_read=False).exists()
            
            if isMessage:
                return True
            else:
                return False
        except Exception as error:
            raise HTTPException(
                    status_code=400, 
                    detail=f'Ошибка crud_check_is_read_message {error}'
                )


async def crud_is_read_message(list_message:list):
    if list_message:
        try:
            message = await NotificationIsRead.filter(id__in=list_message).update(is_read=True)
            if message is None:
                raise HTTPException(
                    status_code=400, 
                    detail=f'Ошибка обновлений '
                )
            return message
        except Exception as error:
            raise HTTPException(
                    status_code=400, 
                    detail=f'Ошибка обновлений {error}'
                )


async def crud_get_in_message(user_id:int):
    if id:
        try:
            message = await NotificationIsRead.filter(user_id=user_id).prefetch_related("message_id").order_by("-message_id__create_at")
            if message is None:
                raise HTTPException(
                    status_code=400, 
                    detail=f'Сообщения отсутствуют'
                )
            return message
        except Exception as error:
            raise HTTPException(
                    status_code=400, 
                    detail=f'Сообщений нет Ошибка {error}'
                )


async def crud_get_message(id:int):
    if id:
        try:
            message = await Notification.filter(user_id_from=id).all().values()
            if message is None:
                raise HTTPException(
                    status_code=400, 
                    detail=f'Сообщения отсутствуют'
                )
            for item in message:
                if item['user_id_to']:
                    user = await crud_get_list_user_ids(item['user_id_to'], ["id","username"])
                    item['user'] = user

            return message

        except Exception as error:
            raise HTTPException(
                status_code=400, 
                detail=f'При получении сообщения что то пошло ни так {error}'
            )



# создание сообщения
async def crud_create_message(data:CreateMessage):
    # print(data)
    try:
        if data:
            message = await Notification.create(**data)
            if message:
                for user in message.user_id_to:
                    sendMessage = await NotificationIsRead.create(user_id=user, message_id_id=message.id, is_read=False)
    except Exception as error:
        raise HTTPException(
            status_code=400, 
            detail=f'При создании сообщения что то пошло ни так {error}'
        )
    