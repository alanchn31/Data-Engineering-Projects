import configparser
import os
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, from_unixtime
from pyspark.sql.functions import year, month, dayofmonth, hour, 
                                  weekofyear, dayofweek, date_format
from pyspark.sql.types import StructType, StructField as Fld, DoubleType as Dbl,
                              StringType as Str, IntegerType as Int, DateType as Date,
                              TimestampType as Ts


config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    """
    Description: Creates spark session.

    Returns:
        spark session object
    """
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()

    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key", AWS_ACCESS_KEY_ID)
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key", AWS_SECRET_ACCESS_KEY)
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3n.awsAccessKeyId", AWS_ACCESS_KEY_ID)
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3n.awsSecretAccessKey", AWS_SECRET_ACCESS_KEY)
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "s3.amazonaws.com")
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3n.endpoint", "s3.amazonaws.com")
    return spark


def song_schema():
    """
    Description: Provides the schema for the staging_songs table.

    Returns:
        spark dataframe schema object
    """
    return StructType([
        Fld("num_songs", Int()),
        Fld("artist_id", Str()),
        Fld("artist_latitude", Dbl()),
        Fld("artist_longitude", Dbl()),
        Fld("artist_location", Str()),
        Fld("artist_name", Str()),
        Fld("song_id", Str()),
        Fld("title", Str()),
        Fld("duration", Dbl()),
        Fld("year", Int())
    ])


def process_song_data(spark, input_data, output_data):
    """
    Description: Read in songs data from json files.
                 Outputs songs and artists dimension tables in parquet files in S3.

    Arguments:
        spark: the spark session object. 
        input_data: path to the S3 bucket containing input json files.
        output_data: path to S3 bucket that will contain output parquet files. 

    Returns:
        None
    """
    # get filepath to song data file
    song_data = input_data + 'song_data/*/*/*/*.json'
    
    # read song data file
    df = spark.read.json(song_data, schema=song_schema())

    # extract columns to create songs table
    songs_table = df.select(['song_id', 'title', 'artist_id', 
                             'year', 'duration']).distinct().where(
                             col('song_id').isNotNull())
    
    # write songs table to parquet files partitioned by year and artist
    songs_path = output_data + 'songs'
    songs_table.write.partitionBy('year', 'artist_id').parquet(songs_path)

    # extract columns to create artists table
    artists_table = df.select(['artist_id', 'artist_name', 'artist_location', 
                             'artist_latitude', 'artist_longitude']).distinct().where(
                             col('artist_id').isNotNull())
    
    # write artists table to parquet files
    artists_path = output_data + 'artists'
    artists_table.write.parquet(artists_path)


def process_log_data(spark, input_data, output_data):
    """
    Description: Read in logs data from json files.
                 Outputs time and users dimension tables, songplays fact table
                in parquet files in S3.

    Arguments:
        spark: the spark session object. 
        input_data: path to the S3 bucket containing input json files.
        output_data: path to S3 bucket that will contain output parquet files. 

    Returns:
        None
    """
    # get filepath to log data file
    log_data = input_data + 'log_data/*/*/*.json'

    # read log data file
    df = spark.read.json(log_data)
    
    # filter by actions for song plays
    df = df.filter(df.page == 'NextSong')

    # extract columns for users table
    users_table = df.select(['userId', 'firstName', 'lastName', 
                             'gender', 'level']).distinct().where(
                             col('userId').isNotNull())
    
    # write users table to parquet files
    users_path = output_data + 'users'
    users_table.write.parquet(users_path)
    
    def format_datetime(ts):
        """
        Description: converts numeric timestamp to datetime format.

        Returns:
            timestamp with type datetime
        """
        return datetime.fromtimestamp(ts/1000.0)

    # create timestamp column from original timestamp column
    get_timestamp = udf(lambda x: format_datetime(int(x)), Ts())
    df = df.withColumn("start_time", get_timestamp(df.ts))
    
    # create datetime column from original timestamp column
    get_datetime = udf(lambda x: format_datetime(int(x)), Date())
    df = df.withColumn("datetime", get_datetime(df.ts))
    
    # extract columns to create time table
    time_table = df.select('ts', 'start_time', 'datetime'
                           hour("datetime").alias('hour'),
                           dayofmonth("datetime").alias('day'),
                           weekofyear("datetime").alias('week'),
                           year("datetime").alias('year'),
                           month("datetime").alias('month'),
                           dayofweek("datetime").alias('weekday')
                          ).dropDuplicates()
    
    # write time table to parquet files partitioned by year and month
    time_table_path = output_data + 'time'
    time_table.write.partitionBy('year', 'month').parquet(time_table_path)

    # read in song data to use for songplays table
    songs_path = input_data + 'song_data/*/*/*/*.json'
    song_df = spark.read.json(songs_path, schema=song_schema())

    # extract columns from joined song and log datasets to create songplays table
    df = df.drop_duplicates(subset=['start_time'])
    songplays_table = song_df.alias('s').join(df.alias('l'), 
                                             (song_df.title == df.song) & \
                                             (song_df.artist_name == df.artist)).where(
                                             df.page == 'NextSong').select([
                                             col('l.start_time'),
                                             year("l.datetime").alias('year'),
                                             month("l.datetime").alias('month'),
                                             col('l.userId'),
                                             col('l.level'),
                                             col('s.song_id'),
                                             col('s.artist_id'),
                                             col('l.sessionID'),
                                             col('l.location'),
                                             col('l.userAgent')
                                            ])

    # write songplays table to parquet files partitioned by year and month
    songplays_path = output_data + 'songplays'
    songplays_table.write.partitionBy('year', 'month').parquet(songplays_path)


def main():
    """
    Description: Calls functions to create spark session, read from S3
                 and perform ETL to S3 Data Lake.

    Returns:
        None
    """
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "s3://alanchn31-datalake/"
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
