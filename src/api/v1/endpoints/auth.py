from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from tortoise.exceptions import DoesNotExist
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
from src.models.user import User, User_Pydantic
from src.crud.auth import crud_create_user
from src.crud.auth import crud_get_list_user,delUser
from src.schemas.user import CreateUser
from fastapi import Request

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()

SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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
async def create_user(data:CreateUser):
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



# DELETE START
class UserDel(BaseModel):
    id:int
@router.post("/user/del")
async def user_del(data:UserDel):
    print(data)
    print(data.id)
    if data:
        resultDel = await delUser(data.id)
        return resultDel
    else:
        return False

# DELETE END



def create_access_token_new(pas: str, expires_delta: timedelta = None):
    # Создаем стандартный payload
    to_encode = {
        "sub": pas,  
        "iat": datetime.utcnow(),  
    }
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt




@router.post("/user/get_user_current")
async def get_user_current(data:getUserCurrent): 
    
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
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


# async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
async def get_current_user(token:str):
    # print(f"Received credentials: {token}")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print(f"Decoded payload: {payload}")    
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    try: 
        user = await User.get(username=username)
        # user = await User.filter(username=username).first()
    except DoesNotExist:
        raise credentials_exception
    
    return user

@router.post("/login", response_model=TokenResponse)
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
async def logout():
    return {"message": "Successfully logged out"}


@router.post("/user/get_list_user")
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
    
@router.post("/user/get_current_user_info")
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
