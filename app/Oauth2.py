from jose import JWTError,jwt
from datetime import datetime,timedelta,timezone
from .config import settings
from . import schemas
from fastapi import Depends,HTTPException,status
from fastapi.security.oauth2 import OAuth2PasswordBearer

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

def create_token(data:dict):
    to_encode=data.copy()
    expiry=datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expiry})

    token=jwt.encode(to_encode, settings.JWT_SECRET ,algorithm=ALGORITHM)

    return token

def verify_token(token:str, credentials_exception):

    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data


def get_current_user_id(token: str = Depends(oauth2_scheme)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Couldnt validate credentials", headers={"WWW-Authenticate":"Bearer"})

    return verify_token(token,credentials_exception)
    pass