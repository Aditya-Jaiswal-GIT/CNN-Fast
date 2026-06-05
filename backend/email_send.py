from fastapi_mail import FastMail, MessageSchema, ConnectionConfig,MessageType
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from dotenv import load_dotenv
import asyncio
import os
load_dotenv()
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_USERNAME"),
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)
async def send_mail(mail):
    html = """<h1>Welcome to LungSense</h1> """

    message = MessageSchema(
        subject="LungSense – AI-Powered Lung Disease Detection System",
        recipients=[mail],
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    print("Sending mail...")
    await fm.send_message(message)
    print("Mail sent!")
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
