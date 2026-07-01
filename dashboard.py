from login import signup ,login # import login and signup function from login.py
from database import supabase  # import supabase
from fastapi import HTTPException



def is_id_correct(t_id):
    try:
        result = supabase.table("users").select("id").eq("id",t_id).execute()
        return True
        
    except :
        return False
        



def all_classes(t_id):
    try:
        is_correct = is_id_correct(t_id)
        if is_correct == False:
            raise HTTPException(status_code=400,detail = "your id is not correct")
        else:
            result = supabase.table("classrooms").select("name","join_code").eq("teacher_id",t_id).execute()
            return result.data
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))



def create_class(t_id,class_name):
    is_id_c = is_id_correct(t_id)
    if is_id_c == False:
        raise HTTPException(500,detail="aa ha you are caughed 👻 HACKERR!!")
    is_exist = supabase.table("classrooms").select("name").eq("teacher_id",t_id).eq("name",class_name).execute()
    if is_exist.data:
        raise HTTPException(status_code=400,detail="you already have a class with this name ")
    try:
        result = supabase.table("classrooms").insert({
            "teacher_id":t_id,
            "name":class_name

        }).execute()
        
        return {
            "msg":"your class created sussefully",
            "join_code":result.data[0]["join_code"]
        }
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))