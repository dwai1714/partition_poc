import mysql.connector as mysql

def db_connect(user_name):
    db = mysql.connect(
    host="localhost",
    user=user_name,
    passwd="pass",
    database="swap_test",
    auth_plugin='mysql_native_password'
)
    return db

def get_process_id(user_name_process):
    db = db_connect("b_user")
    cursor = db.cursor()
    query = "select ID from information_schema.processlist ;"
    cursor.execute(query)
    records = cursor.fetchall()
    if len(records) > 0:
        return records
    else:
        return None

from datetime import datetime
a = datetime.utcnow()
print (datetime.utcnow().strftime("%s"))


# from loc_poc import lock_unlock_user
# query_execute()
#
# python - c 'from loc_poc import query_execute; query_execute()'
# python - c 'from loc_poc import query_execute; lock_unlock_user("dc", "lock")'
# python -c 'from loc_poc import rename_table; rename_table("big_table", "big_table_new", "older")'
# python - c 'from loc_poc import query_execute; kill_process("dc", 40)'
#
#
#

