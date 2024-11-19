from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("PySpark Test") \
    .master("local[*]") \
    .config("spark.hadoop.security.authentication", "simple") \
    .getOrCreate()


# Create a simple DataFrame
data = [("Alice", 34), ("Bob", 45), ("Cathy", 29)]
columns = ["Name", "Age"]
df = spark.createDataFrame(data, columns)

# Show DataFrame content
df.show()
