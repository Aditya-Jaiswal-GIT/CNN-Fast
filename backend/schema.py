from pydantic import BaseModel,Field,EmailStr

class Signup(BaseModel):
    email : EmailStr = Field(description="Email of the user")
    username : str = Field(description="Username of User")
    password : str = Field(description="Password of the user")

class Signin(BaseModel):
    username : str
    password : str