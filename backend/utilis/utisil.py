from passlib.context import CryptContext
import jwt
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv
load_dotenv()
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

#JWT Requirment
jwt_secret = os.getenv("JWT_TOKEN")
jwt_algo = "HS256"
oauth = OAuth2PasswordBearer(tokenUrl="signin")

#Used to verify the user password
def verify(plainpassword:str,hashpassword:str):
    return pwd_context.verify(plainpassword,hashpassword)

#USed to generate the hash of the user password
def pwd_hash(password:str):
    hashed_pwd = pwd_context.hash(password)
    return hashed_pwd