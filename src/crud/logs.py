from sqlalchemy import desc, distinct, func, or_
from sqlalchemy.orm import Session

from datetime import datetime
from src.core.sqlalchemy_engine import async_session_maker


from tortoise import Tortoise
from src.core.db import TORTOISE_ORM

from fastapi import FastAPI, Request


from datetime import datetime, timezone

from src.models.user import User
from src.models.sites_user import SitesUser
from src.models.group_user import GroupUser
from src.models.loading import Loading1c
from src.schemas.surgard_event import SurgardEventCreate
from src.schemas.user import CreateUser
from src.schemas.sites import SitesCreate
from src.schemas.logs import SchemaLogsCreate
from src.schemas.loading import SchemaLoading1c,SchemaGetPhone
from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel
from tortoise.exceptions import IntegrityError
from src.crud.sites_of_user import crud_get_list_all
from tortoise.exceptions import MultipleObjectsReturned
from typing import List
from src.models.logs import Logs
import functools
import os
from src.crud.bd import userCurrent
import json


async def getUser(request:Request):
    from src.api.v1.endpoints.auth import get_current_user
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split("Bearer ")[1]
        user = await get_current_user(token)
        return user



def log_event(type:str, section: str = None):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:

                request: Request = kwargs.get("request") or next(
                    (arg for arg in args if isinstance(arg, Request)), None
                )
                
                filename =  section or os.path.basename(__file__)
                method_name = func.__name__
                client_ip = request.client.host if request else "unknown"
                user_id = await getUser(request) 
                
                try:
                    desc_data = json.dumps({})
                    for kw in kwargs.keys():
                        if kw is not None:
                            if kw == "request":
                                continue
                            print(f' KWARGS {kwargs.get(kw)}' )
                            desc_data = json.dumps(dict(kwargs.get(kw)))
                    print(f'JSON {desc_data}')
                except Exception as error:
                    print(f'ERROR json DUMPS {error}')


               

                if user_id is None:
                    # get id User
                    nameUser = kwargs.get('data')
                    if nameUser is not None:
                        username = nameUser.username
                        password = nameUser.password
                        idUser =  await userCurrent(username, password)
                        idUser = idUser.id
                    # get id User
                else:
                    idUser = user_id.id

                



                await logs_create(
                    request, 
                    SchemaLogsCreate(
                    type=type, 
                    desc=desc_data or "", 
                    ip=request.client.host, 
                    user=idUser, 
                    date_create=datetime.now(), 
                    section=filename
                    )
                )
                return await func(*args, **kwargs) 
            except Exception as error:
                print(f'LOGS log_event {error}')
                return await func(*args, **kwargs)
        return wrapper
    return decorator


async def logs_create(request:Request, data:SchemaLogsCreate):
    try:
        print(f'{data}')
        print(f'{request}')

        if data is not None:
            result = await Logs.create(**data.dict())
            return result
    except Exception as error:
        print(error)
        