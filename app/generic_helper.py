import re
import json
from fastapi import Request
from fastapi.responses import JSONResponse

def jsonresponse(text):
    return JSONResponse(content={"fulfillmentResponse": {"messages": [{"text": {"text": [text]}}]}})

def extract_session_id(session: str):
    match = re.search(r'sessions/([a-zA-Z0-9\-]+)', session)
    return match.group(1) if match else None

def get_string_from_food_dict(food_dict: dict):
    return ", ".join([f"\n{k} x {v}" for k, v in food_dict.items()])
