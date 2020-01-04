import os
import sys

from pyspark.sql import SparkSession


def fill_table():
    spark = SparkSession \
        .builder \
        .appName("app_name") \
        .getOrCreate()

    file_path = sys.modules[__name__].__file__
    project_path = os.path.dirname(os.path.dirname(file_path))

    ingest_df = spark.read.option("header", "true").csv(
        "file:///" + project_path+ "/partition_poc/majestic_million.csv")
    ingest_df.printSchema()

    ingest_df.write.format('jdbc').options(
        url='jdbc:mysql://localhost/swap_test',
        driver='com.mysql.jdbc.Driver',
        dbtable='big_table_temp',
        user='dc',
        password='pass').mode('overwrite').save()

fill_table()