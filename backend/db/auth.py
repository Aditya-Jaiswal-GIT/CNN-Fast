import jwt
from fastapi import HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import os
import json
from db.crud import get_user_by_username,get_user_by_email,create_user
from dotenv import load_dotenv
from utilis.utisil import pwd_context,pwd_hash,jwt_secret,jwt_algo,oauth,verify
load_dotenv()
#Use to create the user and store in the DB
def register_user(data:dict):
    user_data = data.copy()
    email = get_user_by_email(user_data['email'])
    if email :
        raise HTTPException(status_code=400,detail="Email Already exist")
    username = get_user_by_username(user_data['username'])
    if username :
        raise HTTPException(status_code=400,detail="Username already exist")
    user_data['password'] = pwd_hash(user_data['password'])
    user_id = create_user(user_data)
    return user_id
#Used to authenticate user
def authenticate(data:dict):
    user_data = data.copy()
    user = get_user_by_username(user_data['username'])

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify(
        user_data['password'],
        user["password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    return user

#Create The JWT Token
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