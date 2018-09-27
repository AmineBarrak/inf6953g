from pyspark.sql import SQLContext
from pyspark import SparkContext
import sys

"""
    run me throught ${SPARK_DIRECTORY}/bin/spark-submit
    you can use > to redirect my output, to be more easily read
"""

if (len(sys.argv)<2):
	print("Argument 1: Nom du fichier input")
	exit(1)
input_path = sys.argv[1]

if __name__ == "__main__":
    spark = SparkContext.getOrCreate()
    sqlContext = SQLContext(spark)
    df = sqlContext.read.load(input_path,
            format='com.databricks.spark.csv',
            header='true', inferSchema='true')
    #this also might be a very bad idea as standard output is node dependant
    df_credir = df.select("card_type").distinct()
    for row in df_credir.collect():
	print row.card_type
