from DBConnecter import cnx

def charge_type_data():
    if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
            cursor.execute("SELECT * FROM CHARGE_TYPE")
            rows = cursor.fetchall()
            resData = {}
            for row in rows:
                resData["수입 여부"] = row[0]
        cnx.close()
        return resData
    else:
        print("Connection Fail")

def brand_data():
    if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
            cursor.execute("SELECT * FROM CHARGE_TYPE")
            rows = cursor.fetchall()
            for row in rows:
                print('수입 여부:',row[0])
        cnx.close()
    else:
        print("Connection Fail")



def charge_info_search(searchItem):
    query = f"SELECT * FROM CHARGE WHERE CHARGE_ADDRESS like '%{searchItem}%'"
    if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            resData = {}
            for row in rows:
                print(row)
        return resData
    else:
        return "Connection Fail"

