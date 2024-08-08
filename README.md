# gatorevals-scraper

## How to use
run gen_pickle.py, then run scrape.py


## Data
data is stored in CSV format, containing the top 6 data points available on gatorevals, as well as the average of these scores.

Need the data in a JSON map format?
CSV -> JSON:
https://csvjson.com/csv2json

## script workflow
1. pull tableau URL from the official gatorevals page (https://gatorevals.aa.ufl.edu/public-results/)
2. open tableau URL with selenium
3. use selenium to webscrape the data points

## parallelism opportunity
modify the start and end indexes of the main for loop -> run multiple instances of the script.