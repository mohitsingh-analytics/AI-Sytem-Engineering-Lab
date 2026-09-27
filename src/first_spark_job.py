from pathlib import Path
from pyspark.sql import SparkSession

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_FILE = BASE_DIR / "data/raw/sales.csv"

spark= SparkSession.builder.appName("SalesAnalysis").master("local[*]").getOrCreate()

df = spark.read.option("header", True).option("inferSchema", True).csv(str(CSV_FILE))
##testing df from spark
df.show()
df.printSchema()
df.explain()

## understanding concepts for the partition
print("\n" + "=" * 50)
print("PARTITION EXPERIMENT")
print("=" * 50)

print("Original Partitions", df.rdd.getNumPartitions())
df1 = df.repartition(1)
df4 = df.repartition(4)
df20 = df. repartition(20)

print(f"1 partition :{df1.rdd.getNumPartitions()}")
print(f"4 partition :{df4.rdd.getNumPartitions()}")
print(f"20 partition :{df20.rdd.getNumPartitions()}")

print("Number of partitions:", df.rdd.getNumPartitions())
result = df.groupBy("region").sum("amount")

result.show()
result.explain()

df4 = df.repartition(4)

print("Original partitions:", df.rdd.getNumPartitions())
print("New partitions:", df4.rdd.getNumPartitions())

print("Records per partition: 4")

print(
    df4.rdd
       .mapPartitions(lambda rows: [sum(1 for _ in rows)])
       .collect()
)

print("*******Partitions******* 1 ")

print(
    df.rdd
       .mapPartitions(lambda rows: [sum(1 for _ in rows)])
       .collect()
)
spark.stop()    
