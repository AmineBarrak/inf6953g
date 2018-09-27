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

def parse_time(strTime):
	return time.strptime(strptime, "%Y-%m-%d")

def create_customer_tuple(customer):
	date = customer.date
	isVip = customer.vip
	return (date, isVip)
	
def get_newest(customer1, customer2):
	if customer1[0] < customer2[0]:
		return customer2
	else:
		return customer1

if __name__ == "__main__":
	spark = SparkContext.getOrCreate()
	sqlContext = SQLContext(spark)
	df = sqlContext.read.load(input_path,
            format='com.databricks.spark.csv',
            header='true', inferSchema='true')
	vip_number = df.rdd.map(lambda customer: (customer.member_id, create_customer_tuple(customer))) \
	.reduceByKey(lambda customer1, customer2: get_newest(customer1, customer2))\
	.map(lambda customer : int(customer[1][1]))\
	.reduce( lambda a,b : a + b)
	print(vip_number)
