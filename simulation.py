from pyspark.sql import SparkSession
import mysql.connector as mysql

def fill_table():
    spark = SparkSession \
        .builder \
        .appName("app_name") \
        .getOrCreate()

    ingest_df = spark.read.option("header", "true").csv(
        "file:///Users/dc/Downloads/majestic_million.csv")
    ingest_df.printSchema()

    ingest_df.write.format('jdbc').options(
        url='jdbc:mysql://localhost/swap_test',
        driver='com.mysql.jdbc.Driver',
        dbtable='big_table_temp',
        user='dc',
        password='pass').mode('overwrite').save()

def db_connect(user_name_with_report_privilege, password):
    db = mysql.connect(
    host="localhost",
    user=user_name_with_report_privilege,
    passwd=password,
    database="swap_test",
    auth_plugin='mysql_native_password'
)
    return db

def execute_a_long_running_query():
    db = db_connect("report_user", "report")
    cursor = db.cursor()

    ## defining the Query
    query = '''select  a.tld, a.Domain, sum(a.GlobalRank) from big_table a        
              join big_table b         
              on a.Domain = b.Domain          
              and a.TLD = b.TLD         
              and a.domain like '%org%' 
              join big_table c
              on a.Domain = c.Domain 
              group by a.tld, a.Domain;
            '''

    ## getting records from the table
    cursor.execute(query)

    ## fetching all records from the 'cursor' object
    records = cursor.fetchall()

    for record in records:
        print(record[0])
    db.close()
execute_a_long_running_query()