from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from typing import Union
from fastapi import Depends, FastAPI, HTTPException, status
from user_auth import AuthHandler
from database_util import database_methods
from aws_s3_copy import s3_copy

app = FastAPI()
auth_handler = AuthHandler()
users = []
db_method=database_methods()
copy_obj=s3_copy()

class UserInput(BaseModel):
    year:int
    month:int
    date:int
    station:Optional [str] = None
    
class UserData(BaseModel):
    username:str
    password: str


@app.get("/fetch_url_nexrad",status_code=status.HTTP_200_OK)
async def fetch_url(userinput: UserInput,username=Depends(auth_handler.auth_wrapper)):
    aws_nexrad_url = f"https://noaa-nexrad-level2.s3.amazonaws.com/index.html#{userinput.year:04}/{userinput.month:02}/{userinput.date:02}/{userinput.station}"
    return {'url': aws_nexrad_url }

@app.get("/fetch_url_goes",status_code=status.HTTP_200_OK)
async def fetch_url(userinput: UserInput,username=Depends(auth_handler.auth_wrapper)):
    aws_nexrad_url = f"https://noaa-goes18.s3.amazonaws.com/index.html#ABI-L1b-RadC/{userinput.year:04}/{userinput.month:02}/{userinput.date:02}"
    return {'url': aws_nexrad_url }



@app.post('/register', status_code=status.HTTP_201_CREATED)
def register(auth_details: UserData):
    user_fetch_status=db_method.fetch_user(auth_details.username)
    if user_fetch_status != 'no_user_found' or user_fetch_status == 'Exception': 
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    user_status=db_method.add_user(auth_details.username,hashed_password)
    if user_status=='failed_insert':
        raise HTTPException(status_code=400, detail='Error')

@app.post('/login',status_code=status.HTTP_200_OK)
def login(auth_details: UserData):
    fetch_user_status=db_method.fetch_user(auth_details.username)
    if (fetch_user_status == 'no_user_found' or not auth_handler.verify_password(auth_details.password, fetch_user_status[0]['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(fetch_user_status[0]['username'])
    return { 'token': token }


@app.get('/geos_get_year',status_code=status.HTTP_200_OK)
def goes_year(username=Depends(auth_handler.auth_wrapper)):
    return db_method.geos_get_year()

@app.get('/geos_get_day/{year}',status_code=status.HTTP_200_OK)
def goes_year(year:int,username=Depends(auth_handler.auth_wrapper)):
    return db_method.geos_get_day(year)

@app.get('/geos_get_hour/{year}/{day}',status_code=status.HTTP_200_OK)
def goes_year(year:int, day:int,username=Depends(auth_handler.auth_wrapper)):
    return db_method.geos_get_hour(year, day)

@app.get('/nexrad_get_year',status_code=status.HTTP_200_OK)
def goes_year(username=Depends(auth_handler.auth_wrapper)):
    return db_method.nexrad_get_year()

@app.get('/nexrad_get_month/{year}',status_code=status.HTTP_200_OK)
def goes_year(year:int,username=Depends(auth_handler.auth_wrapper)):
    return db_method.nexrad_get_month(year)


@app.get('/nexrad_get_day/{year}/{month}',status_code=status.HTTP_200_OK)
def goes_year(year:int, month:int,username=Depends(auth_handler.auth_wrapper)):
    return db_method.nexrad_get_day(year, month)

@app.get('/nexrad_get_sites/{year}/{month}/{day}',status_code=status.HTTP_200_OK)
def goes_year(year:int, month:int, day:int,username=Depends(auth_handler.auth_wrapper)):
    return db_method.nexrad_get_sites(year, month, day)

@app.get('/get_nexrad_sites',status_code=status.HTTP_200_OK)
def goes_year(username=Depends(auth_handler.auth_wrapper)):
    return db_method.get_nexrad_sites()

@app.get('/copy_file_s3/{source_bucket_name}/{key}',status_code=status.HTTP_200_OK)
def copy_file_s3(source_bucket_name:str,key:str,username=Depends(auth_handler.auth_wrapper)):
    status_copy=copy_obj.copy_file_into_s3(source_bucket_name,key)
    if status_copy == False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid request')
    
@app.get("/healthz",status_code=status.HTTP_200_OK)
def hello():
    return {"status": "connected"}

@app.get("/",status_code=status.HTTP_200_OK)
def hello():
    return {"status": "connected"}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)