from login import signup ,login # import login and signup function from login.py
from database import supabase  # import supabase
from fastapi import HTTPException
import io
import uuid
"""
{
# all functions
[is_id_correct] # check is id correct 
[all classes] # find all classes resistered with the t_id
[create_class] # create a new class for specific id
[all_assigments] # find all assigments resistered with the class
[create_assigment] # create a new assigment with images
}
"""

def is_id_correct(t_id):
    try:
        result = supabase.table("users").select("name").eq("id",t_id).execute()
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

def all_assigments(t_id,class_name):
    is_correc = is_id_correct(t_id)
    if is_correc == False:
        raise HTTPException(500,detail = "id is incorrect")
    try:
        result = supabase.table("Assigment").select("name","discription","photos_url").eq("teacher_id",t_id).eq("class_name",class_name).execute()
        return result.data
    except Exception as e:
        raise HTTPException(400,detail=str(e))

def turn_image_to_url(photos:list[bytes]):
    photo_url = []
    for photo in photos:
        name = uuid.uuid4()
        path = f"images/assigment/{name}.jpg"
        supabase.storage.from_("assigments").upload(path,photo)
        photo_url.append(supabase.storage.from_("assigments").get_public_url(path))
    return photo_url
        
def create_assigment(t_id,class_name,name,discription=None,photos=None):
    try :
        is_i = is_id_correct(t_id)
        if is_i == False:
            raise HTTPException(500,detail="is is incorrect")
        if photos and len(photos) > 4 :
            raise HTTPException(500,detail="too many photos max limit is only 4")
        photos_url = None
        result = {
            "teacher_id":t_id,
            "class_name":class_name,
            "name":name    }
        if photos :
            photos_url = turn_image_to_url(photos)
            result["photos_url"] = photos_url
        if discription:
            result["discription"]=discription
        try:
            supabase.table("Assigment").insert(result).execute()
            return {"msg":"assigment added sussefully"}
        except Exception as e:
            raise HTTPException(400,detail= str(e))
    except Exception as e:
        raise HTTPException(400,detail=str(e))


