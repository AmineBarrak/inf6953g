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
    df_countries = df.groupby('country').count()
    df_countries = df_countries.sort("count", ascending=False)
    for country in df_countries.head(3):
	print ("country : %s, nb = %s" % (country.country, country["count"]))
