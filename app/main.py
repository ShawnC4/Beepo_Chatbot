from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import json
import re

import app.db_helper as db_helper
from app.generic_helper import jsonresponse, extract_session_id, get_string_from_food_dict

app = FastAPI()

inprogess_orders = {}

@app.post("/")
async def webhook(request: Request):
    data = await request.json()
    print(json.dumps(data, indent=4))
    # You can extract parameters or other data from queryResult
    intent = data.get('intentInfo', {}).get('displayName', 'default')
    parameters = data.get('intentInfo', {}).get('parameters', {})
    session = data.get('sessionInfo', {}).get('session', {})
    # Use regex to extract the session ID
    session_id = extract_session_id(session)

    intent_routing = {
        'add.order': add_order,
        'remove.order': remove_order,
        'track.orderid': track_order,
        'complete.order': complete_order
    }

    if intent in intent_routing:
        return intent_routing[intent](parameters, session_id)
    
    return jsonresponse(f"{intent} intent is not handled yet")


def track_order(parameters: dict, session_id: str):
    orderid = parameters.get('orderid').get('resolvedValue')
    status = db_helper.get_order_status(orderid)

    if status:
        return jsonresponse(f"Order status for order {orderid} is: {status[0]}")
    else:
        return jsonresponse(f"Order {orderid} not found")
    
def add_order(parameters: dict, session_id: str):
    fooditem = parameters.get('food-item').get('resolvedValue')
    quantity = parameters.get('quantity', {}).get('resolvedValue', [])
    
    if len(fooditem) != len(quantity):
        return jsonresponse("Mismatch: Ensure you provide both food item and quantity.")
    
    food_dict = dict(zip(fooditem, quantity))
    
    if session_id in inprogess_orders:
        inprogess_orders[session_id].update(food_dict)
    else:
        inprogess_orders[session_id] = food_dict

    new_items_message = "Added: " + get_string_from_food_dict(food_dict)
    total_items_message = "Total Order: " + get_string_from_food_dict(inprogess_orders[session_id])

    return jsonresponse(new_items_message + "\n\n" + total_items_message + "\n\n" + "Anything else?")

def complete_order(parameters: dict, session_id: str):
    if session_id not in inprogess_orders:
        return jsonresponse("No order in progress")
    
    order = inprogess_orders[session_id]

    if len(order.keys()) == 0:
        return jsonresponse("No items in order")
    
    try:
        response = db_helper.complete_order(order)

        del inprogess_orders[session_id]
    except Exception as e:
        response = f"An error occurred while completing the order: {e}"


    return jsonresponse(response)

def remove_order(parameters: dict, session_id: str):
    '''
    step 1: locate sessio id
    step 2: get calue from dict -> {"Laksa": 2, "Nasi Lemak": 1}
    step 3: remove food items from dict -> ["Nasi Lemak"]
    '''
    if session_id not in inprogess_orders:
        return jsonresponse("No order in progress")
    
    current_order = inprogess_orders[session_id]
    fooditem = parameters.get('food-item').get('resolvedValue')

    removed_items = []
    no_such_items = []
    for item in fooditem:
        if item in current_order:
            removed_items.append(item)
            del current_order[item]
        else:
            no_such_items.append(item)
    
    if len(removed_items) > 0:
        response = f"Removed: {', '.join(removed_items)}"

    if len(no_such_items) > 0:
        response += f"\n\n{', '.join(no_such_items)} not found in order"
    
    if len(current_order.keys()) > 0:
        response += f"\n\nTotal Order: {get_string_from_food_dict(current_order)}"
    else:
        response += "\n\nOrder is empty"
    
    return jsonresponse(response)