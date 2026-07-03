from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from login import signup, login
from dashboard import all_classes, create_class, all_assigments, create_assigment
from fastapi.middleware.cors import CORSMiddleware
# FIX: Import typing utilities to prevent server crash
from typing import List, Optional 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for clean local & deployment testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

class show_assignments(BaseModel):
    id:str
    class_name:str
    
@app.post("/signup")
async def signu(detail:signup_detail):
    return signup(detail.d_name, detail.name, detail.password, detail.role)

@app.post("/login")
async def Log(detail:Login_detail):
    return login(detail.name, detail.password)

@app.post("/dashboard")
async def show_cl(detail:Show_classes):
    return all_classes(detail.id)

@app.post("/create_class")
async def c_class(detail:reate_class):
    return create_class(detail.id, detail.class_name)

@app.post("/show_ass")
async def Show_all_assignments(detail:show_assignments):
    return all_assigments(detail.id, detail.class_name)

@app.post("/create_ass")
async def creat_new_assignment(
    t_id: str = Form(...),
    class_name: str = Form(...),
    name: str = Form(...),
    discription: str = Form(...),
    photos: Optional[List[UploadFile]] = File(None)  # Safely optional now
):
    file_bytes_list = []
    
    # Check if files were actually uploaded before loop
    if photos:
        for photo in photos:
            # Skip empty strings or unselected placeholder slots from browser
            if photo.filename: 
                content = await photo.read()
                file_bytes_list.append(content)
        
    return create_assigment(t_id, class_name, name, discription, file_bytes_list)
    
