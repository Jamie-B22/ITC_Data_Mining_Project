# ITC Data Mining Project

###### Current status: This is an ongoing project. This readme currently details the progress made as of the second checkpoint where data is scraped into a MySQL database.

### Description

This web scraper finds, scrapes and stores details of books from Goodreads (https://www.goodreads.com/). It works by taking the user's selection of a goodreads list and scraping and storing the details of all books on that list.

The web scraper was created as a project as part of the Data Science Fellows Program at ITC (https://www.itc.tech/).

### Usage

`python3 main.py <type argument> <detail argument>`

(Defaults to most read this week in local country if no arguments entered.)

Where:


| Type | Detail | Example |
| :--- | :----------- | :-------- |
| `most-popular` | `[YYYYMM]` | `most-popular 202001` |
| `most-read` | `COUNTRYperiod` | `most-read ILm` |
| `new-releases` | `genre` | `new-releases fantasy` |
| `custom-list` | `customID` | `custom-list 121572` |

#### Example:

`python3 main.py most-popular 202001`

#### Points to note:
* To avoid throttling by goodreads, there is a 10 second wait implemented between web requests.  
* The custom lists are made by users, you need to know which list you want to scrape and get the ID from the URL.

### Setup Instructions
#### Database Setup:
1. A MySQL database is used to store the data and the database upload process in `SQL_uploader.py` in this project has a few components
   specific to MySQL, so for compatibility MySQL should be installed and used.
   *Note that to connect to a MySQL database from SQLAlchemy in Python the `mysqlclient` package is used. Users running a 
   32 bit version of Python 3 on a 64 bit machine will have major issues installing and importing `mysql` client unless 
   they install and use a 64 bit version of Python 3.*
   
2. The database and table schema can be created in your MySQL localhost by running the `goodreads_data db and table creation script.sql`
in SQL. The only strictly necessary step here is to create a database named `goodreads_data` in the highest level of your localhost 
   as this is what the script will connect to. If the tables fo not exist, the SQLAlchemy package will recognise this when
    the program is first run and it will create the appropriate schema for you.
   
3. When the scraper is run, it will ask the user for a 'MySQL username' and 'MySQL password'. Enter credentials at this point that 
have read and write access to the `goodreads_data` database you have created on your localhost.

### Authors
- Jamie Bamforth <a href="https://github.com/Jamie-B22"> @Jamie-B22 </a>
- Jordan Ribbans <a href="https://github.com/jordanribbans"> @jordanribbans </a>