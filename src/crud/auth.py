from src.models.surgard_event import SurgardEvent
from src.schemas.surgard_event import SurgardEventCreate
from sqlalchemy import desc, distinct, func, or_
from sqlalchemy.orm import Session

from datetime import datetime
from src.core.sqlalchemy_engine import async_session_maker
from src.models.surgard_event_sa import SurgardEventSA
from tortoise.functions import Count

from tortoise import Tortoise
from src.core.db import TORTOISE_ORM


from datetime import datetime, timezone

from src.models.surgard_event import SurgardEvent
from src.models.user import User
from src.models.group_user import GroupUser
from src.models.sites_user import SitesUser
from src.schemas.surgard_event import SurgardEventCreate
from src.schemas.user import CreateUser
from datetime import datetime

from tortoise.exceptions import IntegrityError
from fastapi import HTTPException

from src.crud.customers import getCustomersPhone, getSitesCustomers
from src.crud.sites_of_user import create_site_of_user_reg



# получение пользователя по почте 
async def get_user_email(email:str):
    if not email:
        return False
    user = await User.filter(email = email).first()
    if user is None:
        raise HTTPException(
            status_code=400, 
            detail="Пользователь не найден"
        )
    return user
    


async def crud_create_user(data: CreateUser, password:str ):
    # print(f"Creating SurgardEvent with data: {data}")
    # db = Session
    try:
        usr = data.dict()
        usr['password_hash'] = password
        usr['group_user'] = await GroupUser.filter(id=usr['group_user']).first()
        
        user = await User.create(
            # username=data.username,
            # password_hash=password,  
            # is_active=data.is_active,
            # group_user=data.group_user,
            # email=data.email,
            # tel=data.tel
            **usr
        )
        print(f"creater user {user}")
        return user
    except Exception as error:
        return {"detail":f'crud_create_user user {error}'}



# Создание пользователя при регистрации
async def crud_create_user_reg(data: CreateUser, password:str ):

    try:
        data['password_hash'] = password
        if 'group_user' in data:
            data['group_user_id'] = data.pop('group_user')
        # print(data)
        user = await User.create(
            **data
        )
        # После регистрации пользователю автоматически присваивается объект если сходятся номера
        # Пока решено отключить 07 07 2026
        # включил 24 07 но переделал, чтобы админ утверждал
        if user.id:
            data = await getSitesCustomers(user.tel)
            if data:
                await create_site_of_user_reg(data, user.id)


        raise HTTPException(status_code=200, detail=f"user create")  
    except HTTPException as http_err:
        # Если это уже HTTPException (из CRUD), просто пробрасываем её дальше
        raise http_err
    except Exception as e:
        # Если это какая-то неизвестная ошибка (например, база упала)
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")  
    except IntegrityError:
        raise HTTPException(
            status_code=400, 
            detail="Пользователь уже существует"
        )


# async def crud_get_list_user(pages:dict, userID:int, userGroup:int):
#     dataPage = dict(pages)
#     offset = (dataPage['page'] - 1) * dataPage['number']
#     limit = dataPage['number']
#     search_text = dataPage['search']

#     # 
#     users_query = User.filter(parent = userID).prefetch_related("group_user")

#     # 2
#     if search_text and search_text.strip():
#         users_query = users_query.filter(username__icontains=dataPage['search'])  
    
#     total_count = await users_query.count()

#     users = await users_query.limit(limit).offset(offset)
    
#     # users = await User.filter(parent = userID).all().values()

#     if users is not None:
#         result = []
#         for user in users:
#             user_dict = dict(user)
#             result.append(user_dict)
#         # print(result)
#         # return users
#         return{
#             "total": total_count,
#             "result": result
#         }


# GET USER MANAGER
async def crud_get_list_user(pages:dict, userID:int, userGroup:int):
    dataPage = dict(pages)
    offset = (dataPage['page'] - 1) * dataPage['number']
    limit = dataPage['number']
    search_text = dataPage['search']
    filter = dataPage['filter'] if dataPage['filter'] else 2

    print(filter) 

    # 1
    users_query = User.filter(parent = userID).all().prefetch_related("group_user","user_objects", "user_objects__site").annotate(sites_count=Count("user_objects"))
    if int(filter) == 0:
        users_query = users_query.filter(sites_count=0)
    elif int(filter) == 1:
        users_query = users_query.filter(sites_count__gt=0)
    elif int(filter) == 3: ## активация
        users_query = users_query.filter(is_check=False)
         # фильтр по неактивиованным объектам
    elif int(filter) == 4:
        isActiveSites = await SitesUser.filter(active=False).all().values()
        listObject = []
        if len(isActiveSites) > 0:
            for objID in isActiveSites:
                listObject.append(objID.get('user_id_id'))
        users_query = users_query.filter(id__in = listObject)
            



    # 2
    if search_text and search_text.strip():
        users_query = users_query.filter(username__icontains=dataPage['search'])  

    # total
    total_count = await users_query.count()
    # users = await User.all().prefetch_related("group_user").filter(username__icontains=dataPage['search']).limit(limit).offset(offset)

    # 3 result
    users = await users_query.limit(limit).offset(offset)

   
    
    
    if users is not None:
        result = []
        for user in users:
            sites_list = []
            for user_site in user.user_objects:
                sites_list.append({
                    "active":user_site.active,
                    "name":user_site.site.Name if user_site.site else None,
                })
                # print(f'OFEST {user_site.site.Name}')

            user_dict = dict(user)
            user_dict['sites_count'] = getattr(user, 'sites_count', 0)
            user_dict['sites_list'] = sites_list
            result.append(user_dict)
            # print(result)
        # return users

       
            
        return{
            "total": total_count,
            "result": result
        }
# GET USER MANAGER


# GET USER SUPERUSER
async def crud_get_list_user_su(pages:dict):
    dataPage = dict(pages)
    offset = (dataPage['page'] - 1) * dataPage['number']
    limit = dataPage['number']
    search_text = dataPage['search']
    filter = dataPage['filter'] if dataPage['filter'] else 2

    print(filter) 

    # 1
    users_query = User.all().prefetch_related("group_user","user_objects", "user_objects__site").annotate(sites_count=Count("user_objects"))
    if int(filter) == 0:
        users_query = users_query.filter(sites_count=0)
    elif int(filter) == 1:
        users_query = users_query.filter(sites_count__gt=0)
    elif int(filter) == 3: ## активация
        users_query = users_query.filter(is_check=False)
         # фильтр по неактивиованным объектам
    elif int(filter) == 4:
        isActiveSites = await SitesUser.filter(active=False).all().values()
        listObject = []
        if len(isActiveSites) > 0:
            for objID in isActiveSites:
                listObject.append(objID.get('user_id_id'))
        users_query = users_query.filter(id__in = listObject)
            



    # 2
    if search_text and search_text.strip():
        users_query = users_query.filter(username__icontains=dataPage['search'])  

    # total
    total_count = await users_query.count()
    # users = await User.all().prefetch_related("group_user").filter(username__icontains=dataPage['search']).limit(limit).offset(offset)

    # 3 result
    users = await users_query.limit(limit).offset(offset)

   
    
    
    if users is not None:
        result = []
        for user in users:
            sites_list = []
            for user_site in user.user_objects:
                sites_list.append({
                    "active":user_site.active,
                    "name":user_site.site.Name if user_site.site else None,
                })
                # print(f'OFEST {user_site.site.Name}')

            user_dict = dict(user)
            user_dict['sites_count'] = getattr(user, 'sites_count', 0)
            user_dict['sites_list'] = sites_list
            result.append(user_dict)
            # print(result)
        # return users

       
            
        return{
            "total": total_count,
            "result": result
        }
# GET USER SUPERUSER




async def crud_get_list_user_ids(userIDs:list, fields:list=None):
    try:
        if not fields:
            users = await User.filter(id__in=userIDs).all().values()
        else:
            users = await User.filter(id__in=userIDs).values(*fields)
        if users is not None:
            return users
    except Exception as error:
        raise HTTPException(
            status_code=400, 
            detail=f"Пользователь уже существует {error}"
        )

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



#  обновление пользователя 
async def updateUser(user):
    try:
        if not user:
            return None
        
        userUpdate = User.filter(id=user['id'])
        user.pop("id")
        await userUpdate.update(**user)
        return {"update":"ok"}
        
    except Exception as err:
        return {
            "error":err
        }




#  обновление статуса пользователя
async def isActive(data):
    try:
        if not data:
            return None
        
        user = dict(data)
        # result = await User.filter(id=user['id']).update(is_active=user.get("is_active"))
        userCurrent = await User.get(id=user['id'])
        result = await User.filter(id=user['id']).update(is_active= not userCurrent.is_active )
        return result 
        
    except Exception as err:
        return {
            "error":err
        }