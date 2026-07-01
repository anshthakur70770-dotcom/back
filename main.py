from fastapi import FastAPI
from pydantic import BaseModel
from login import signup,login
from dashboard import all_classes,create_class

app = FastAPI()
class signup_detail(BaseModel):
    d_name :str
    name:str
    password:str
    role:str

class Login_detail(BaseModel):
    name:str
    password:str

class Show_classes(BaseModel):
    id:str

class reate_class(BaseModel):
    id:str
    class_name:str

@app.post("/signup")
def signu(detail:signup_detail):
    return signup(detail.d_name,detail.name,detail.password,detail.role)


@app.post("/login")
def Log(detail:Login_detail):
    return login(detail.name,detail.password)

@app.post("/dashboard")
def show_cl(detail:Show_classes):
    return all_classes(detail.id)

@app.post("/create_class")
def c_class(detail:reate_class):
    return create_class(detail.id,detail.class_name)



    
