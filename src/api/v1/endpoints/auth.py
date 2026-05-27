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
from src.crud.auth import crud_get_list_user,delUser,crud_get_list_user_ids
from src.crud.logs import logs_create, log_event
from src.crud.bd import create_access_token,get_current_user
from src.schemas.user import CreateUser,RegUser,CodeEmail,VerificationData
from src.schemas.logs import SchemaLogsCreate
from fastapi import Request
from typing import List


# ПОЧТА отправки сообщения
from src.services.mail import MailNewStatus
from src.services.func import generate_numeric_code

import os
from typing import Dict

from dotenv import load_dotenv
load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))


router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()

# SECRET_KEY = "your-secret-key-change-in-production"
# ALGORITHM = "HS256"

class LoginRequest(BaseModel):
    username: str
    password: str



class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    username:str
    group_user:int
    id:int

class getUserCurrent(BaseModel):
    password:str
    username:str

# class createUser(BaseModel):
#     email:str
#     group_user:int
#     password: str
#     tel:str
#     username: str
#     is_active: bool


@router.post("/user/create")
@log_event(type="user", section="create")
async def create_user(data:CreateUser,request:Request):
    try:
        # password = create_access_token_new(data.password)
        password = User.hash_password(data.password)
        result = await crud_create_user(data, password)
        return result
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = error
        )

#  Registration
@router.post("/user/reg_user")
async def reg_user(data:RegUser,request:Request):
    user_dict = dict(data)
    user_dict['group_user'] = 2
    user_dict['is_active'] = True
    user_dict['parent'] = 0
    del user_dict['confirm']
    passd = user_dict.pop('password', None)
    try:
        # password = create_access_token_new(data.password)
        password = User.hash_password(passd)
        result = await crud_create_user_reg(user_dict, password)
        return result
    except Exception as error:
        return error



# DELETE START
class UserDel(BaseModel):
    id:int
@router.post("/user/del")
@log_event(type="user", section="del")
async def user_del(data:UserDel,request:Request):
    if data:
        resultDel = await delUser(data.id)
        return resultDel
    else:
        return False

# DELETE END



# def create_access_token_new(pas: str, expires_delta: timedelta = None):
#     # Создаем стандартный payload
#     to_encode = {
#         "sub": pas,  
#         "iat": datetime.utcnow(),  
#     }
    
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_MINUTES)
    
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# def create_access_token(data: dict, expires_delta: timedelta = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_MINUTES)
    
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


###################################################
# При авторизации 
@router.post("/user/get_user_current")
@log_event(type="auth", section="login")
async def get_user_current(data:getUserCurrent, request:Request): 
    
    user = await User.get(username=data.username)

    
    try:
        if not user.verify_password(data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        # print(user)
        access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            username=user.username,
            id=user.id,
            group_user=user.group_user, 
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
# При авторизации 
###################################################




# async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
# async def get_current_user(token:str):
#     # print(f"Received credentials: {token}")
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         # print(f"Decoded payload: {payload}")    
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except jwt.PyJWTError:
#         raise credentials_exception
    
#     try: 
#         user = await User.get(username=username)
#         # user = await User.filter(username=username).first()
#     except DoesNotExist:
#         raise credentials_exception
    
#     return user

@router.post("/login", response_model=TokenResponse)
# @log_event(type="auth", section="login")
async def login(request: LoginRequest):
    try:
        user = await User.get(username=request.username)
        if not user.verify_password(request.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        
        access_token_expires = timedelta(day=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

@router.get("/me", response_model=User_Pydantic)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/logout")
@log_event(type="user", section="logout")
async def logout(request:Request):
    return {"message": "Successfully logged out"}


@router.post("/user/get_list_user")
@log_event(type="user", section="get_list_user")
async def get_list_user(request:Request):
    auth_header = request.headers.get("Authorization")
    # print(auth_header)
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split("Bearer ")[1]
        user = await get_current_user(token)
        # print(f"Current user: {user.id}")
        # print(token)
        userID = user.id
        userGroup = user.group_user
        data = await crud_get_list_user(userID, userGroup)
        return data



###########################################################################################
# Получитю спользователей по списку IDs
class UserIdsRequest(BaseModel):
    id: List[int]

@router.post("/user/get_list_user_ids")
# @log_event(type="user", section="get_list_user")
async def get_list_user_ids(data:UserIdsRequest,request:Request):
    if not data.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f" Ошибка получения пользователя "
        )
    try:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split("Bearer ")[1]
            user = await get_current_user(token)
            if user:
                users = await crud_get_list_user_ids(data.id, ["id", "username"])
                return users
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail = f" Ошибка получения пользователя ->"
            )
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f" Ошибка получения пользователя {error}"
        )

###########################################################################################
    

###########################################################################################
#  Постоянно срабатывает после  перезагрузки страницы
@router.post("/user/get_current_user_info")
# @log_event(type="user", section="get_current_user_info")
async def get_current_user_info(request:Request):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split("Bearer ")[1]
        user = await get_current_user(token)
        user_info = {}

        if user is not None:
            user_info = {"tel":user.tel, "email":user.email, "username":user.username}
            return user_info
        else:
            return user_info
#  Постоянно срабатывает после  перезагрузки страницы
###########################################################################################






###########################################################################################
# ВЕРИФИКАЦИЯ ЧЕРЕЗ ПОЧТУ 
# Для получения проверочного кода для входа через почта
@router.post("/user/get_code_email")
async def get_code_email(data:CodeEmail, request:Request):
    if not data:
        return False
        
    email = data.email
    checkEmail = await User.filter(email = email).first()
    if checkEmail is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"Почта не найдена"
        )

    ip_address = request.client.host
    used = False
    created_at = datetime.now()
    code =  generate_numeric_code()
    code_hash =  VerificationCode.hash_code(str(code))

    create_code = await VerificationCode.create(
        email=email,
        code_hash = code_hash,
        ip_address = ip_address
    )
    if create_code is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f" Ошибка создания кода "
        )
    
    if create_code:
        testMail = MailNewStatus(os.getenv("HOST"), os.getenv("PORT"), os.getenv("USER"), os.getenv("PASSWORD"))
        testMail.send_message(email, "NEW STATUS Вход в систему. Код", f"Код для входа в систему: {code} ")



# Для получения проверочного кода для входа через почта
###########################################################################################

###########################################################################################
# ВЕРИФИКАЦИЯ ЧЕРЕЗ ПОЧТУ 
# ПОЛУЧЕНИЕ И ПРОВЕРКА КОДА
@router.post("/user/verification_code_email")
async def verification_code_email(data:VerificationData, request:Request):
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f" Код не получен попробуйте еще раз получить проверочный код"
        )
    getCode = await VerificationCode.filter(email=data.email, used=False).first()
    if getCode is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f" Нет активного кода, попробуйте снова отправить проверочный код"
        )
    isCode = getCode.verify_code(data.code)
    if not isCode:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"Код проверки истек, попробуйте снова отправить проверочный код "
        )
    if isCode:
        # Получение пользователя
        user = await get_user_email(data.email)
        if user:
            # Деактивируем код
            getCode.used = True
            await getCode.save()
            # Деактивируем код 
            access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user.username}, expires_delta=access_token_expires
            )
            
            return TokenResponse(
                access_token=access_token,
                token_type="bearer",
                username=user.username,
                id=user.id,
                group_user=user.group_user, 
                expires_in=ACCESS_TOKEN_EXPIRE_MINUTES
            )
        return user

    
# ПОЛУЧЕНИЕ И ПРОВЕРКА КОДА
# ВЕРИФИКАЦИЯ ЧЕРЕЗ ПОЧТУ 
###########################################################################################
