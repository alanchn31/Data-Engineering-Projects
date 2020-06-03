## Description
---
* This repo contains projects done which applies principles in data engineering. 
* Notes taken during the course can be found in folder `0. Back to Basics`

## Projects
---
1. <ins> Postgres ETL </ins> :heavy_check_mark:
* This project looks at data modelling for a fictitious music startup Sparkify, applying STAR schema to ingest data to simplify queries that answers business questions the product owner may have

2. <ins> Cassandra ETL </ins> :heavy_check_mark:
* Looking at the realm of big data, Cassandra helps to ingest large amounts of data in a NoSQL context. This project adopts a query centric approach in ingesting data into data tables in Cassandra, to answer business questions about a music app

3. <ins> Web Scrapying using Scrapy, MongoDB ETL </ins> :heavy_check_mark:
* In storing semi-structured data, one form to store it in, is in the form of documents. MongoDB makes this possible, with a specific collection containing related documents. Each document contains fields of data which can be queried. 
* In this project, data is scraped from a books listing website using Scrapy. The fields of each book, such as price of a book, ratings, whether it is available is stored in a document in the books collection in MongoDB.

4. <ins> Data Warehousing with AWS Redshift </ins> :heavy_check_mark:
* This project creates a data warehouse, in AWS Redshift. A data warehouse provides a reliable and consistent foundation for users to query and answer some business questions based on requirements.

5. <ins> Data Lake with Spark & AWS S3 </ins> :heavy_check_mark:
* This project creates a data lake, in AWS S3 using Spark. 
* Why create a data lake? A data lake provides a reliable store for large amounts of data, from unstructured to semi-structured and even structured data. In this project, we ingest json files, denormalize them into fact and dimension tables and upload them into a AWS S3 data lake, in the form of parquet files.

6. <ins> Data Pipelining with Airflow </ins> :heavy_check_mark:
* This project schedules data pipelines, to perform ETL from json files in S3 to Redshift using Airflow. 
* Why use Airflow? Airflow allows workflows to be defined as code, they become more maintainable, versionable, testable, and collaborative

7. <ins> Capstone Project </ins> :heavy_check_mark:  
* This project is the finale to Udacity's data engineering nanodegree. Udacity provides a default dataset however I chose to embark on my own project. 
* My project is on building a movies data warehouse, which can be used to build a movies recommendation system, as well as predicting box-office earnings. View the project here: [Movies Data Warehouse](https://github.com/alanchn31/Udacity-Data-Engineering-Capstone)