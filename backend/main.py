from fastapi import FastAPI, HTTPException, File, UploadFile,Request
from fastapi.responses import JSONResponse
from model import prediction

from io import BytesIO
from PIL import Image
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
app = FastAPI()
limiter = Limiter(key_func=get_remote_address)

# add limiter to app
app.state.limiter = limiter

# middleware
app.add_middleware(SlowAPIMiddleware)

# custom exception
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "error": "Too many requests"
        }
    )

@app.get('/')
@limiter.limit('5/minute')
async def home(request:Request):
    return "API is Running"
@app.get('/health')
@limiter.limit("5/minute")
async def health(request:Request):
    return {
        'status' :'OK'
    }
@app.post('/predict')
@limiter.limit('5/minute')
async def predict(request:Request,file: UploadFile = File(...)):
    try:
        contents = await file.read()
        img = Image.open(BytesIO(contents))
        message = prediction(img)
        return JSONResponse(status_code=200, content={'message': message})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
  