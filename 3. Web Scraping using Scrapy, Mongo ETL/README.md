## Description
---
* This repo provides the ETL pipeline, to populate the books database, in collection:titles.
* It provides the code to scrape from a books listing website, providing the title, price, rating of a book, along with whether it is still in stock and its url.  
* The code in this repository scrapes from: "http://books.toscrape.com/".  
* It then ingests the data into a MongoDB database hosted on localhost, port 27017, into a database called "books" and collection called "titles".

## Running the ETL Pipeline
---
* First, make sure MongoDB is running on port 27017, on localhost
* Next, run ```scrapy crawl books``` from the scrapy project folder "books"
* You can now confirm that the data was stored on MongoDB in books database using MongoDB Compass

![Books](books.PNG)