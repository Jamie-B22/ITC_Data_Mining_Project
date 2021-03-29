# ITC Data Mining Project

###### Current status: This is an ongoing project. This readme currently details the progress made as of the third checkpoint where data is scraped into a MySQL database and can be enriched from the Open Library API and the NYT bestsellers lists API.

### Description

This web scraper finds, scrapes and stores details of books from [Goodreads](https://www.goodreads.com/). It works by taking the user's selection of a goodreads list and scraping and storing the details of all books on that list. The data will be stored in a MySQL database (structure detailed below), or into a CSV file if it is unable to make a connection to the database.

The data scraped from Goodreads can be enriched with data from:
* The [New York Times (NYT) Books API](https://developer.nytimes.com/docs/books-product/1/overview), which provides details of books on the current and past NYT bestseller lists.
* The [Open Library Books API](https://openlibrary.org/dev/docs/api/books), which provides data about the various editions of titles that have been published.

The web scraper was created as a project as part of the Data Science Fellows Program at [ITC](https://www.itc.tech/).

### Usage

`python3 main.py <type argument> <detail argument>`

#### Parameters:


| Type | Detail | Example |
| :--- | :----------- | :-------- |
| **Scraping** |
| `most-popular` | `[YYYYMM]` | `most-popular 202001` |
| `most-read` | `[COUNTRYperiod]` | `most-read ILm` |
| `new-releases` | `[genre]` | `new-releases fantasy` |
| `custom-list` | `[customID]` | `custom-list 121572` |
| **Enrichment** |
| `NYT-API-update-all` | `[YYYY-MM-DD or 'current']` | `NYT-API-update-all 20200122` |
| `NYT-API-update-list` | `"[NYT bestsellers list],[YYYY-MM-DD or 'current']"`* | `NYT-API-update-list combined-print-and-e-book-fiction,current` |
| `get-NYT-bestesller-list-names` | *leave blank* | `get-NYT-bestesller-list-names`  |
| `OL-title-search` | `[book title]` | `OL-title-search Harry Potter` |
| `OL-author-search` | `[author name]` | `OL-title-search J K Rowling` |
| `OL-ISBN-search` | `[ISBN]` | `OL-title-search 059035342X` |

*All valid `[NYT bestsellers list]` values can printed to sysout by passing the type argument `get-NYT-bestesller-list-names`.


#### Example:

`python3 main.py most-popular 202001`


#### Parameter descriptions:

| Type | Description |
| :--- | :----------- |
| **Scraping** |
| `most-popular` | Scrapes the most popular books on Goodreads in a given month |
| `most-read` | Scrapes the most read books on Goodreads for a given country in the latest week/month/year |
| `new-releases` | Scrapes Goodreads for the latest releases for a given genre |
| `custom-list` | Scrapes books from custom lists created by Goodreads users |
| **Enrichment** |
| `NYT-API-update-all` | Fetches every NYT bestseller list for the given date |
| `NYT-API-update-list` | Fetches the given NYT bestseller list for that date |
| `get-NYT-bestesller-list-names` | Prints the possible list names you can give above (nothing uploaded to the database) |
| `OL-title-search` | Searches OpenLibrary for all books with the given title (or similar) |
| `OL-author-search` | Searches OpenLibrary for all books with the given author (or similar)|
| `OL-ISBN-search` | Searches OpenLibrary for the book with the given ISBN |



#### Points to note:
* To avoid throttling by Goodreads and the NYT bestseller API, there is a 10 second wait implemented between web requests.  
* The custom lists are made by users, you need to know which list you want to scrape and get the ID from the URL.
* Only run 'main.py' from the terminal, not from a python console. Due to the use of the package 'stdiomask' to mask the SQL user password entered in the command line, any modules that import the 'SQL_classes_tables.py' will not run from the python console and should only be run from the terminal. 

### Database Design

<img src="https://raw.githubusercontent.com/Jamie-B22/ITC_Data_Mining_Project/master/Reference%20Material/ERD.png" width="1000">

**Note:** The `openlibrary_isbn` table is not connected via isbn to the editions tables in the schema, but the database is designed so that they can be joined in queries

Details about the database structure can be found in the file: [data_dictionary](https://github.com/Jamie-B22/ITC_Data_Mining_Project/blob/master/Reference%20Material/data_dictionary.csv)

### Setup Instructions
#### Database Setup:
1. A MySQL database is used to store the data and the database upload process in `SQL_uploader.py` in this project has a few components
   specific to MySQL, so for compatibility MySQL should be installed and used. Installation instructions can be found [here](https://www.mysqltutorial.org/install-mysql-ubuntu/)
   for Ubuntu users (similar steps for other Linux distros), for windows there is an installation wizard that can be downloaded [here](https://dev.mysql.com/downloads/installer/).
   
2. Linux users only: If you are a linux user and to access MySQL using your current user, you need to use `sudo` then you must create a new user that does not require su rights to use mysql to use with the scraper program. Instructions to do this can be found [here](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04#step-3-%E2%80%94-creating-a-dedicated-mysql-user-and-granting-privileges).
If you give the credentials of a user that requires `sudo` to access MySQL in the shell to the program, you will not be able to connect through the program.
   
3. The database and table schema should be created in your MySQL localhost and can be created by running the `goodreads_data db and table creation script.sql`
in SQL. One way to do this is by running the OS independent command `mysql -u <username> -p < "<filepath>goodreads_data db and table creation script.sql"`.
   
4. When the scraper is run, it will ask the user for a 'MySQL username' and 'MySQL password'. Enter credentials at this point that 
have read and write access to the `goodreads_data` database you have created on your localhost.

#### Requirements Install:
#### Linux
1. From the directory the requirements.txt file is located in, run command `pip install --user -r requirements.txt`
2. If there are issues with the installation of the `mysqlclient` library:
    - If you are on a 64 bit machine ensure that you have the latest 64 bit version of Python3.
   - Run commands `sudo apt-get install libmysqlclient-dev`, `sudo apt-get install python3-dev` and `sudo apt-get install gcc`
    to install these packages. Replace `apt-get` with the suitable command for your distro if required.
     
#### Windows
1. Run command `pip install -r requirements.txt`.
2. If there are issues with the installation of the `mysqlclient` library:
    - If you are on a 64 bit machine ensure that you have the latest 64 bit version of Python3.


### Authors
- Jamie Bamforth <a href="https://github.com/Jamie-B22"> @Jamie-B22 </a>
- Jordan Ribbans <a href="https://github.com/jordanribbans"> @jordanribbans </a>