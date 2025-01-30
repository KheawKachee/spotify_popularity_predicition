from pyspark.sql import SparkSession,functions as func
from pyspark.ml.feature import Bucketizer
from pyspark.sql.functions import col

import os

filepath_data= '/opt/airflow/data'
filepath_data_modified= '/opt/airflow/data/modified'

print(f"Checking file: {os.path.abspath(f'{filepath_data}/spotify-2023.csv')}")

spark = SparkSession.builder.appName("spark").getOrCreate()

df = spark.read.option("header", "true").option("inferSchema", "true").csv(f"{filepath_data}/spotify-2023.csv")
                                                    #Automatically infers the data types of each column based on the contents.


df.printSchema()
#df.show(n=3, truncate=10,vertical=True)
#print(df.count())

#binning mode col
df = df.withColumn("is_mode_major", func.when(df["mode"] == "Major", 1).when(df["mode"] == "Minor", 0))
df = df.drop("mode")

#onehot the key col
music_dict = {
    "C": 1,"C#": 2,
    "D": 3,"D#": 4,
    "E": 5,
    "F": 6,"F#": 7,
    "G": 8,"G#": 9,
    "A": 10,"A#": 11
}
#no B cause it not nessesary
for key, value in music_dict.items():
    # Use `when` to check if 'key' is equal to the note, and assign the value from the dict
    df = df.withColumn(f"key_{key}", func.when(df["key"] == key, 1).otherwise(0))
df = df.drop("key")

#binning steams col
df = df.withColumn("streams", col("streams").cast("int"))
bucketizer = Bucketizer(splits=[0, 5e7, 1e8, 6e8, 1e9, float('Inf')],
                        inputCol='streams',
                        outputCol='popularity_score')
df = bucketizer.setHandleInvalid('keep').transform(df)
df = df.withColumn("popularity_score", col("popularity_score").cast("int"))

#mood col
df = df.withColumn("mood_score", col('danceability_%') * col('valence_%') * col('energy_%') * col('liveness_%'))

#dealing with ,
df = df.withColumn("in_shazam_charts", func.regexp_replace("in_shazam_charts", ",", ""))
df = df.withColumn("in_deezer_playlists", func.regexp_replace("in_deezer_playlists", ",", ""))
df = df.withColumn("in_shazam_charts", col("in_shazam_charts").cast("int"))
df = df.withColumn("in_deezer_playlists", col("in_deezer_playlists").cast("int"))

#YYMMDD
df = df.withColumn(
    "date", 
    func.concat(func.col("released_year").cast("string"), 
             func.lpad(func.col("released_month").cast("string"), 2, '0'), 
             func.lpad(func.col("released_day").cast("string"), 2, '0'))
    .cast("int")
)

#relocate cols
rm_cols = [f"key_{i}"for i in music_dict.keys()]+['is_mode_major']
other_cols = [col for col in df.columns if col not in rm_cols]
df = df.select(other_cols[:15]+rm_cols+other_cols[15:]) 


df.printSchema()
df.show(n=3, truncate=10,vertical=True)

df.write.option("header", "true").mode('overwrite').csv(filepath_data_modified)

for filename in os.listdir(filepath_data_modified):
    if filename.startswith("part-") and filename.endswith(".csv"):
        os.rename(os.path.join(filepath_data_modified, filename), f"{filepath_data_modified}/spotify_etl_data.csv")
                            #Forms the full path to the existing file.
    else:os.remove(os.path.join(filepath_data_modified, filename))

spark.stop()