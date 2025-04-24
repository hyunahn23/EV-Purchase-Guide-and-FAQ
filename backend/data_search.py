from DBConnecter import cnx

def search_all(table_name):
    if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]

            resData = [column_names] + [list(row) for row in rows]
        return resData
    else:
        return "CONNECTION FAIL"
    

def like_serach(table_name,column_name,search_text):
    if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
            query = f"SELECT * FROM {table_name} WHERE {column_name} LIKE %s LIMIT 100"
            cursor.execute(query, (f"%{search_text}%",))  
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]

            resData = [column_names] + [list(row) for row in rows]
        return resData
    else:
        return "CONNECTION FAIL"
    
def equal_serach(table_name,column_name,search_text):
    if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
            query = f'SELECT * FROM {table_name} WHERE {column_name} = %s LIMIT 100'
            cursor.execute(query, (f"{search_text}",))  
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]

            resData = [column_names] + [list(row) for row in rows]
        return resData
    else:
        return "CONNECTION FAIL"
    
def custom_equal_serach(table_name,search_column,column_name,search_text):
    if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
            query = f'SELECT {search_column} FROM {table_name} WHERE {column_name} = %s'
            cursor.execute(query, (f"{search_text}",))  
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            
            resData = [column_names] + [list(row) for row in rows]
        return resData
    else:
        return "CONNECTION FAIL"
