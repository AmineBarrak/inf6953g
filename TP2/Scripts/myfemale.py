from pyspark import SparkContext

input_path = "/home/ubuntu/lab/TP2/sanshead"

spark = SparkContext.getOrCreate()

textFile = spark.textFile(input_path)
counts = textFile.map(lambda line: line.split(',')[0]).distinct()
print("Comptage:"+str(counts.count()))

