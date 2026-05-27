import jwt
from fastapi import HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import os
import json
from dotenv import load_dotenv
load_dotenv()
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
def load():
    with open(rf"data.json",'r') as f :
        data = json.load(f)
    return data
def store(data:dict):
    with open(rf"data.json",'w') as f :
        store = json.dump(data,f,indent=4)
jwt_secret = os.getenv("JWT_TOKEN")
jwt_algo = "HS256"
oauth = OAuth2PasswordBearer(tokenUrl="signin")

def verify(plainpassword:str,hashpassword:str):
    return pwd_context.verify(plainpassword,hashpassword)

def hash(password:str):
    hashed_pwd = pwd_context.hash(password)
    return hashed_pwd

def create(data:dict):
    jsons = load()
    for json in jsons:
        if data["email"]==json["email"]:
            raise HTTPException(status_code=400,detail="Email already exist")
        if data["username"]==json["username"]:
            raise HTTPException(status_code=400,detail="Username already registerd")
    hash_pwd = hash(data["password"])
    user = {"email" : data["email"],"username":data["username"],"password":hash_pwd}
    print(data)
    print(type(data["password"]))
    print(len(data["password"]))
    jsons.append(user)
    store(jsons)

def authenticate(data:dict):
    jsons = load()
    flag=0
    for json in jsons:
        if json["username"]==data["username"]:
            flag=1
            v = verify(data["password"],json["password"])
            if not v:
                raise HTTPException(status_code=400,detail="Incorrect password")
            user = json
    if flag==0:
        raise HTTPException(status_code=400,detail="Username Does not exist")
    else :
        return user


def encode(data:dict):
    payload = data.copy()
    token = jwt.encode(payload,jwt_secret, algorithm=jwt_algo)
    return token
def decode(token):
    try:
        decoded = jwt.decode(token,jwt_secret,algorithms=[jwt_algo])
        return decoded
    except jwt.ExpiredSignatureError:
        return {'error' : "Token Expired"}
    except jwt.InvalidTokenError:
        return {'error' : "Invalid Token"}
    

async def get_current_user(
    token: str = Depends(oauth)
):
    payload = decode(token)

    if "error" in payload:
        raise HTTPException(
            status_code=401,
            detail=payload["error"]
        )

    return payload