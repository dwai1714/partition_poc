import logging
import sys
from time import sleep
from datetime import datetime

import mysql.connector as mysql

def db_connect(user_name_with_all_privilege, password):
    db = mysql.connect(
    host="localhost",
    user=user_name_with_all_privilege,
    passwd= password,
    database="swap_test",
    auth_plugin='mysql_native_password'
)
    return db

def lock_unlock_user(db, user_names_list, operation):
    cursor = db.cursor()

    ## defining the Query
    for user in user_names_list:
        query = "ALTER USER {}@localhost ACCOUNT {};"
        print(query.format(user, operation))
        cursor.execute(query.format(user, operation))

def get_process_id(db, user_names_list):
    cursor = db.cursor()
    user_names_string = ','.join(['%s'] * len(user_names_list))
    query = 'select ID from information_schema.processlist where INFO is NOT NULL and USER in {};'.format(tuple(user_names_list))
    cursor.execute(query.format(user_names_string))
    records = cursor.fetchall()
    if len(records) > 0:
        return records
    else:
        return None

def kill_process(db, records):
    ## getting records from get_process_id
    cursor = db.cursor()
    for record in records:
        kill_query = "KILL {};"
        exist_query = "select ID from information_schema.processlist where ID = {}"
        cursor.execute(exist_query.format(record[0]))
        records = cursor.fetchall()
        if len(records) > 0:
            cursor.execute(kill_query.format(record[0]))

def rename_table(db, old_table, new_table):
    old_table_suffix = datetime.utcnow().strftime("%s")
    cursor = db.cursor()

    ## defining the Query
    query = "RENAME TABLE {} TO {}_{}, {} To {};"
    ## getting records from the table
    cursor.execute(query.format(old_table, old_table, old_table_suffix, new_table, old_table))

def swap_job(service_user_name_for_reports, old_table, new_table, time_out):
    # Lock User who is executing reporting queries. This is a non blocking operation
    db = db_connect("super_user", "super")
    try:
        lock_unlock_user(db, service_user_name_for_reports, "lock")
        for x in range(2): # Looping just to avoid millisecond locks. It wont happen but still
            records = get_process_id(db, service_user_name_for_reports)
            if records is not None:
                if x ==0:
                    sleep(time_out)
                kill_process(db,records)
        rename_table(db,old_table, new_table)
    except Exception as error:
        logging.error(f'error in main error {error} at {datetime.now()}')
        raise error.with_traceback(sys.exc_info()[2])
    finally:
        lock_unlock_user(db, service_user_name_for_reports, "unlock")
        db.close()


swap_job(["report_user", "b_user"], "big_table", "big_table_temp", 60)