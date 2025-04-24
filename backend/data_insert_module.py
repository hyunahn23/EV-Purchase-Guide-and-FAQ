from DBConnecter import cnx

def db_insert_module(table_name,insert_data):
    for i in insert_data:
        query = f"INSERT INTO {table_name} VALUES {i}"
        if cnx and cnx.is_connected():
            with cnx.cursor() as cursor:
                cursor.execute(query)
                cnx.commit()
        cursor.close()

def db_insert_ignore_module(table_name,insert_data):
    for i in insert_data:
        query = f"INSERT IGNORE INTO {table_name} VALUES {i}"
        if cnx and cnx.is_connected():
            with cnx.cursor() as cursor:
                cursor.execute(query)
                cnx.commit()
        cursor.close()



def db_replace_module(table_name,insert_data):
    for i in insert_data:
        query = f"REPLACE INTO {table_name} VALUES {i}"
        if cnx and cnx.is_connected():
            with cnx.cursor() as cursor:
                cursor.execute(query)
                cnx.commit()
        cursor.close()