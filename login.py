from h11._abnf import status_code
from database import supabase 
from fastapi import HTTPException

def is_exist(email):
    result = supabase.table("users").select("email").eq("email",email).execute()
    if result.data:
        return True
    return False

def signup (d_name,name,password,role):
    if is_exist(name)==True:
        raise HTTPException(status_code=400,detail="sorry🥹! but this name already exist")
    else :
        try:
            supabase.table("users").insert({
                "name":d_name,
                "email":name,
                "password_hash":password,
                "role":role
            }).execute()
            return {"message":"your account created sussefully🤓"}
        except Exception as e:
            raise HTTPException(status_code=400,detail=str(e))

def login(name,password):
    result = supabase.table("users").select("id","password_hash").eq("email",name).execute()
    if result.data :
        if result.data[0]["password_hash"]==password:
            return {"msg": "welcome 🙃","id":result.data[0]["id"]}
        elif result.data[0]["password_hash"]!=password:
            raise HTTPException(status_code=400,detail="you entered a wrong password 🤨")
    else:
        raise HTTPException(status_code=400,detail="you entered a wrong id ")
        

