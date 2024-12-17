import mysql.connector

def get_db_connection():
    return mysql.connector.connect(user='root', password='Solarity45sql', host='localhost', database='tastybox_bites')

def get_order_status(orderid: int):
    cnx = get_db_connection()
    cursor = cnx.cursor()

    query = f"SELECT status FROM order_tracking WHERE order_id={orderid}"

    cursor.execute(query)

    status = cursor.fetchone()

    cursor.close()

    return status

def complete_order(order: dict):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()

        max_id_query = "SELECT MAX(order_id) FROM orders"
        cursor.execute(max_id_query)

        order_id = cursor.fetchone()[0] + 1

        for food_item, quantity in order.items():
            try:
                insert_order_item(food_item, quantity, order_id)
            except Exception as e:
                cursor.close()
                raise Exception(f"Order not completed. Error inserting {quantity} of {food_item} into order {order_id}: {e}")
            
        order_total = get_total_order_price(order_id)

        insert_order_tracking(order_id, "in-progress")

        cursor.close()

        return f"Order {order_id} completed. Total bill: ${order_total}"
    except Exception as e:
        cursor.close()
        raise Exception(f"{e}")

def insert_order_item(food_item, quantity, order_id):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()

        cursor.callproc('insert_order_item', [food_item, quantity, order_id])

        cnx.commit()

        cursor.close()

        print(f"Successfully inserted {quantity} of {food_item} into order {order_id}")
    
    except Exception as e:
        raise Exception(f"Error inserting {quantity} of {food_item} into order {order_id}: {e}")
    

def get_total_order_price(order_id):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()

        query = f"SELECT get_total_order_price({order_id})"
        cursor.execute(query)

        total_price = cursor.fetchone()[0]
        cursor.close()

        return total_price
    except Exception as e:
        cursor.close()
        return f"Error getting total price for order {order_id}: {e}"
    

def insert_order_tracking(order_id, status):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()

        insert_query = f"INSERT INTO order_tracking (order_id, status) VALUES ({order_id}, '{status}')"
        cursor.execute(insert_query)

        cnx.commit()

        cursor.close()

        print(f"Successfully inserted order {order_id} with status {status}")

    except Exception as e:
        raise Exception(f"Error inserting order {order_id} with status {status}: {e}")
    
