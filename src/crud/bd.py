from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from tortoise.exceptions import DoesNotExist
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
import os
from src.models.user import User, User_Pydantic
from src.models.user_group_role import UserGroupRole
from src.models.user_group_right import UserGroupRight

# SECRET_KEY = "your-secret-key-change-in-production"
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
ALGORITHM = os.getenv('ALGORITHM')


# проверка прав на выполнение действия
async def checkPermission(group:int, key:str):
    # group = await UserGroupRole.filter(user_group_id=group).first()
    right = await UserGroupRight.filter(key=key).first()
    permission = await UserGroupRole.filter(user_group_id=group, user_group_right_id=right.id).first()
    if not permission:
            raise HTTPException(
                status_code=403,
                # detail = "Недостаточно прав"
            )
    # return permission is not None
    return True





async def getUserRequestToken(request:Request):
    try:
        auth_header = request.headers.get("Authorization") 
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split("Bearer ")[1]
            user = await get_current_user(token)
            return user

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Error getUserRequestToken {error}"
        )



# ПОЛУЧИТЬ ТЕКУЩЕГО ПОЛЬЗОВАТЕЛЯ ПО ТОКЕНУ 
async def get_current_user(token:str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) 
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    try: 
        user = await User.get(username=username)
    except DoesNotExist:
        raise credentials_exception
    
    return user




# CREATE TOKEN
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    print(ACCESS_TOKEN_EXPIRE_MINUTES)
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt




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

async def userCurrent(username:str, password:str): 
    
    

    if username is None or password is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    user = await User.get(username=username)
    
    try:
        if not user.verify_password(password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return user
        
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
