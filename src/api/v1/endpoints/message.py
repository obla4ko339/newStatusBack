from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from tortoise.exceptions import DoesNotExist
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
from src.models.user import User, User_Pydantic
from src.models.logs import Logs
from src.models.verification_codes import VerificationCode
from src.crud.auth import crud_create_user,crud_create_user_reg,get_user_email
from src.crud.auth import crud_get_list_user,delUser
from src.crud.logs import logs_create, log_event
from src.crud.message import crud_create_message,crud_get_message,crud_get_in_message,crud_is_read_message,crud_check_is_read_message
from src.crud.bd import create_access_token,get_current_user
from src.schemas.user import CreateUser,RegUser,CodeEmail,VerificationData
from src.schemas.logs import SchemaLogsCreate
from src.schemas.notification import CreateMessage,DataMessageApi,IsReadMessageApi,IsReadMessageApiId
from fastapi import Request


# ПОЧТА отправки сообщения
from src.services.mail import MailNewStatus
from src.services.func import generate_numeric_code

import os
from typing import Dict
 
from dotenv import load_dotenv
load_dotenv()



router = APIRouter(prefix="/message", tags=["message"])
security = HTTPBearer()


# Проверка есть ли непрочитаныне сообщения
@router.get("/is_read_message_check")
async def is_read_message(request:Request): 
    try:
        auth_header = request.headers.get("Authorization") 
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split("Bearer ")[1]
            user = await get_current_user(token)

            if user:
                return await crud_check_is_read_message(user.id)

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Error get check message {error}"
        ) 



# is_read_message
@router.post("/is_read_message")
async def is_read_message(data:IsReadMessageApi, request:Request): 
    if not data:
        return False
    try:
        list_message = [ int(item) for item in data.id ]
        result =  await crud_is_read_message(list_message)
        return result 
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Error is_read_message {error}"
        ) 




@router.get("/get_in_message")
async def get_in_message(request:Request):
    try:
        auth_header = request.headers.get("Authorization") 
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split("Bearer ")[1]
            user = await get_current_user(token)

            if user:
                return await crud_get_in_message(user.id)

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Error get_in_message {error}"
        )
 

@router.get("/get_out_message")
async def get_out_message(request:Request):
    try:
        auth_header = request.headers.get("Authorization") 
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split("Bearer ")[1]
            user = await get_current_user(token)

            if user:
                return await crud_get_message(user.id)

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = error
        )



@router.post("/create")
# @log_event(type="user", section="create")
async def create_message(data:DataMessageApi,request:Request):
    try:
        auth_header = request.headers.get("Authorization") 
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split("Bearer ")[1]
            user = await get_current_user(token)

            if user:
                res = dict(data)
                res['user_id_from'] = user.id
                res['create_at'] = datetime.now()
                res['status'] = True 
                await crud_create_message(res)

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = error
        )

