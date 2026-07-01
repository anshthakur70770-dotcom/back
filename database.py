from h11._abnf import status_code
import os
from fastapi import HTTPException
from supabase import Client , create_client
from dotenv import load_dotenv
load_dotenv()
url = os.getenv("SUPABASEURL")
key = os.getenv("SUPABASEKEY")

if not url or not key :
    raise HTTPException(status_code=400,detail="an error occured")
else:
    try:
        supabase:Client = create_client(url,key)
        print("connected sussefully")
    except Exception as e :
        raise HTTPException(400,detail=f"connection error:{e}")

