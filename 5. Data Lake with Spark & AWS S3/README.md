## Description
---
This repo provides the ETL pipeline, to populate the sparkifydb AWS S3 Data Lake using Spark  

![S3](screenshots/s3.PNG)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Spark](screenshots/spark.PNG)
* The purpose of this database is to enable Sparkify to answer business questions it may have of its users, the types of songs they listen to and the artists of those songs using the data that it has in logs and files. The database provides a consistent and reliable source to store this data.

* This source of data will be useful in helping Sparkify reach some of its analytical goals, for example, finding out songs that have highest popularity or times of the day which is high in traffic.

## Dependencies
---
* Note that you will need to have the pyspark library installed. Also, you should have a spark cluster running, either locally or on AWS EMR.

## Database Design and ETL Pipeline
---
* For the schema design, the STAR schema is used as it simplifies queries and provides fast aggregations of data.

![Schema](screenshots/schema.PNG)

* For the ETL pipeline, Python is used as it contains libraries such as pandas, that simplifies data manipulation. It enables reading of files from S3, and data processing using Pyspark.

* There are 2 types of data involved, song and log data. For song data, it contains information about songs and artists, which we extract from and load into users and artists dimension tables

* Log data gives the information of each user session. From log data, we extract and load into time, users dimension tables and songplays fact table.

## Running the ETL Pipeline
---
* Run etl.py to read from the song and logs json files, denormalize the data into fact and dimension tables and gives the output of these tables in S3 in the form of parquet files.