import sys
from pyspark.sql import SQLContext
from pyspark import SparkContext

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
    df_female = df.filter(df.gender == "Female").filter(df.country == "CA").filter(df.zone == "zone7")
    print("number of canadian female from Zone7 : %i" % len(df_female.groupBy("member_id").count().collect()))
