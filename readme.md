# ITC Data Mining Project

###### Current status: This is an ongoing project. This readme currently details the progress made as of the third checkpoint where data is scraped into a MySQL database and can be enriched from the Open Library API and the NYT bestsellers lists API.

### Description

This web scraper finds, scrapes and stores details of books from [GoodReads](https://www.goodreads.com/). It works by taking the user's selection of a goodreads list and scraping and storing the details of all books on that list. The data will be stored in a MySQL database (structure detailed below), or into a CSV file if it is unable to make a connection to the database.

The web scraper was created as a project as part of the Data Science Fellows Program at [ITC](https://www.itc.tech/).

### Usage

`python3 main.py <type argument> <detail argument>`

(Defaults to most read this week in local country if no arguments entered.)

Parameters:


| Type | Detail | Example |
| :--- | :----------- | :-------- |
| `most-popular` | `[YYYYMM]` | `most-popular 202001` |
| `most-read` | `[COUNTRYperiod]` | `most-read ILm` |
| `new-releases` | `[genre]` | `new-releases fantasy` |
| `custom-list` | `[customID]` | `custom-list 121572` |
| `NYT-API-update-all` | `[YYYY-MM-DD or 'current']` | `NYT-API-update-all 20200122` |
| `NYT-API-update-all` | `"[NYT bestsellers list],[YYYY-MM-DD or 'current']"`* | `NYT-API-update-list combined-print-and-e-book-fiction,current` |
| `get-NYT-bestesller-list-names` | *leave blank* | `get-NYT-bestesller-list-names`  |

*All valid `[NYT bestsellers list]` values can printed to sysout by passing the Type `get-NYT-bestesller-list-names`.




#### Example:

`python3 main.py most-popular 202001`

#### Points to note:
* To avoid throttling by goodreads, there is a 10 second wait implemented between web requests.  
* The custom lists are made by users, you need to know which list you want to scrape and get the ID from the URL.

### Database Design

<img src="https://github.com/Jamie-B22/ITC_Data_Mining_Project/blob/497f7430c371978d647f9cda8f873e3f4a9a299a/Reference%20Material/ERD.png" width="1000">

Details about the database structure can be found in the file: [data_dictionary](https://github.com/Jamie-B22/ITC_Data_Mining_Project/blob/497f7430c371978d647f9cda8f873e3f4a9a299a/Reference%20Material/data_dictionary.xlsx)

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