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
from src.schemas.surgard_event import SurgardEventCreate
from src.schemas.user import CreateUser
from datetime import datetime




async def crud_create_user(data: CreateUser, password:str ):
    # print(f"Creating SurgardEvent with data: {data}")
    # db = Session
    
    usr = data.dict()
    usr['password_hash'] = password
    user = await User.create(
        # username=data.username,
        # password_hash=password,  
        # is_active=data.is_active,
        # group_user=data.group_user,
        # email=data.email,
        # tel=data.tel
        **usr
    )
    
    return user


async def crud_get_list_user(userID:int, userGroup:int):
    if userGroup == 1:
        users = await User.all().values() 
        return users
    elif userGroup == 2:
        users = await User.filter(parent = userID).all().values()
        return users


async def delUser(id:int):
    try:
        
        getLinkObjects = await SitesUser.filter(user_id = id).exists()
        if getLinkObjects:
            raise ValueError("Пользователь имеет связь с объектом. Удалить невозможно")
        getUser = await User.filter(id=id).first()
        if getUser is not None:
            delUser = await User.delete(getUser)
            return {
                "result": "success",
                "text": "Пользователь удален"
            }
    except ValueError as e:
        # Ожидаемые ошибки валидации
        return {
            "result": "error",
            "text": str(e)
        }
    except Exception as error:
        return error


