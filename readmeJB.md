# ITC Data Mining Project

### Description

This web scraper finds, scrapes and stores details of books from Goodreads (https://www.goodreads.com/). It works by taking the user's selection of a goodreads list and scraping and storing the details of all books on that list.

The web scraper was created as a project as part of the Data Science Pellows Program at ITC (https://www.itc.tech/).

### Usage

`python3 main.py <type argument> <detail argument>`

Where:


| Type | Detail | Example |
| :--- | :----------- | :-------- |
| `most-popular` | '[YYYYMM]` | `most-popular 202001` |
| `most-read` | 'COUNTRYperiod' | `most-read ILm` |
| `new-releases` | `genre` | `new-releases fantasy` |
| `custom-list` | `customID` | ??? |

#### Example:

`python3 main.py most-popular 202001`

#### Points to note:
* To avoid throttling by goodreads, there is a 10 second wait implemented between web requests.  

### Authors
- Jamie Bamforth <a href="https://github.com/Jamie-B22"> @Jamie-B22 </a>
- Jordan Ribbans <a href="https://github.com/jordanribbans"> @jordanribbans </a>