# ITC Data Mining Project

###### Current status: This is an ongoing project. This readme currently details the progress made as of the first checkpoint where it only scrapes the data into a CSV file

### Description

This web scraper finds, scrapes and stores details of books from Goodreads (https://www.goodreads.com/). It works by taking the user's selection of a goodreads list and scraping and storing the details of all books on that list.

The web scraper was created as a project as part of the Data Science Pellows Program at ITC (https://www.itc.tech/).

### Usage

`python3 main.py <type argument> <detail argument>`

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
* The custom lists are made by users, you need to know which list you want to scrape and get the ID from the URL

### Authors
- Jamie Bamforth <a href="https://github.com/Jamie-B22"> @Jamie-B22 </a>
- Jordan Ribbans <a href="https://github.com/jordanribbans"> @jordanribbans </a>