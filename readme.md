# ITC Data Mining Project

###### Current status: This is an ongoing project. This readme currently details the progress made as of the second checkpoint where data is scraped into a MySQL database.

### Description

This web scraper finds, scrapes and stores details of books from [GoodReads](https://www.goodreads.com/). It works by taking the user's selection of a goodreads list and scraping and storing the details of all books on that list. The data will be stored in a MySQL database (structure detailed below), or into a CSV file if it is unable to make a connection to SQL.

The web scraper was created as a project as part of the Data Science Fellows Program at [ITC](https://www.itc.tech/).

### Usage

`python3 main.py <type argument> <detail argument>`

(Defaults to most read this week in local country if no arguments entered.)

Parameters:


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

### [Database Design](https://lh3.googleusercontent.com/D5EGkiF5it1bV2LLciYL0_Wm5eY3b7XT1TnoBIk1EFqWcHez_m5uyb7rkBzBM-v1vCR5qTFJX8wuKPrupvyfvUkY8GG2kJyg1b9tng7iKE3vFADvLFAh223U2ksS_jfPrcI0qQ8zNy0k1ntXEZBdfDmFq8ox-xKgrH6VgXHxP_IiRTlzTQy1cx2Gn2vYhbxdQtzJOCW1s699-5vPqWdSmwLSYjiZHGACA4F5R6I_7fWp7G1hvu23YzgMCCyx3AZK3a0dzLj9HMCNQ3Mx6Vmmgw7gWd3C43yhvyXXoiMI7UBCeCoMbtUmR7BLB8GOnPrIu4cU7bwChTvnDnJhIUEfH-riW1v0oAZTbewtG_vwmrb8epDt0fjsiMrnxNNuyB7NWRZubmL_B58w3RYLpNu5aDY2qZs-4vcldZPGPFA1fj628tBkj2ScxiUMnvy1vm0M2WGf6DfQGJLfJMu2VzbvUULfoWQLlqaMi7hsWts9iO4-KqburTkyhLQncMLn49ke3j_njIGQXq1Ebq-HHnhj5fsidDa4hlJb7WcJegz_A4rb7Ta_QkTT_NVkt_R7HqQZpThg9jnRdIvVqfAF-urKjzxHWG3f0FZzQeBBnCiebZIJF3BlUM9XQR6Mp7YKLsL44Mo0fgTGfHSjuYhXfzcYDXfy6-rgnelg0Tb9W8kNPfMjQRzaurWzRUkiQMoQaJBn2ULkp54tMijX-r8XzfZXXBhuKA=w1475-h796-no?authuser=0)

<img src="https://lh3.googleusercontent.com/D5EGkiF5it1bV2LLciYL0_Wm5eY3b7XT1TnoBIk1EFqWcHez_m5uyb7rkBzBM-v1vCR5qTFJX8wuKPrupvyfvUkY8GG2kJyg1b9tng7iKE3vFADvLFAh223U2ksS_jfPrcI0qQ8zNy0k1ntXEZBdfDmFq8ox-xKgrH6VgXHxP_IiRTlzTQy1cx2Gn2vYhbxdQtzJOCW1s699-5vPqWdSmwLSYjiZHGACA4F5R6I_7fWp7G1hvu23YzgMCCyx3AZK3a0dzLj9HMCNQ3Mx6Vmmgw7gWd3C43yhvyXXoiMI7UBCeCoMbtUmR7BLB8GOnPrIu4cU7bwChTvnDnJhIUEfH-riW1v0oAZTbewtG_vwmrb8epDt0fjsiMrnxNNuyB7NWRZubmL_B58w3RYLpNu5aDY2qZs-4vcldZPGPFA1fj628tBkj2ScxiUMnvy1vm0M2WGf6DfQGJLfJMu2VzbvUULfoWQLlqaMi7hsWts9iO4-KqburTkyhLQncMLn49ke3j_njIGQXq1Ebq-HHnhj5fsidDa4hlJb7WcJegz_A4rb7Ta_QkTT_NVkt_R7HqQZpThg9jnRdIvVqfAF-urKjzxHWG3f0FZzQeBBnCiebZIJF3BlUM9XQR6Mp7YKLsL44Mo0fgTGfHSjuYhXfzcYDXfy6-rgnelg0Tb9W8kNPfMjQRzaurWzRUkiQMoQaJBn2ULkp54tMijX-r8XzfZXXBhuKA=w1475-h796-no?authuser=0" width="1000">

Details about the database structure can be found in the file: data_dictionary

### Setup Instructions
#### Database Setup:
1. A MySQL database is used to store the data and the database upload process in `SQL_uploader.py` in this project has a few components
   specific to MySQL, so for compatibility MySQL should be installed and used.
   
2. The database and table schema can be created in your MySQL localhost by running the `goodreads_data db and table creation script.sql`
in SQL. The only strictly necessary step here is to create a database named `goodreads_data` in the highest level of your localhost 
   as this is what the script will connect to. If the tables fo not exist, the SQLAlchemy package will recognise this when
    the program is first run and it will create the appropriate schema for you.
   
3. When the scraper is run, it will ask the user for a 'MySQL username' and 'MySQL password'. Enter credentials at this point that 
have read and write access to the `goodreads_data` database you have created on your localhost.

#### Requirements Install:
#### Linux
1. From the directory the requirements.txt file is located in, run command `pip3 install --user -r requirements.txt`
2. If there are issues with the installation of the `mysqlclient` library:
    - If you are on a 64 bit machine ensure that you have the latest 64 bit version of Python3
   - Run commands `sudo apt-get install libmysqlclient-dev`, `sudo apt-get install python3-dev` and `sudo apt-get install gcc`
    to install these packages.
     
#### Windows
1. Run command `pip install -r requirements.txt`.
2. If there are issues with the installation of the `mysqlclient` library:
    - If you are on a 64 bit machine ensure that you have the latest 64 bit version of Python3


### Authors
- Jamie Bamforth <a href="https://github.com/Jamie-B22"> @Jamie-B22 </a>
- Jordan Ribbans <a href="https://github.com/jordanribbans"> @jordanribbans </a>