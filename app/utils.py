from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

def hash(password:str)->str:
    return pwd_context.hash(password)

def verify(plain_pwd:str,hashed_pwd)->bool:
    return pwd_context.verify(plain_pwd,hashed_pwd)