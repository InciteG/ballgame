# ballgame

Description: Python Webscraper that pulls data from stats.nba.com and stores it in a database. This data will be used for future analysis.

Table of Contents:
1. Installation
2. Usage
3. Licensing

1. Installation:
Currently have not packaged yet, only in raw python files.

2. Usage:

Python Libraries in use:
- BeautifulSoup
- sqlite3
- Selenium
- Pandas/NumPy (in proogress)

Functions:

1) url_set
  takes unique url identifiers for each basketball team and stores it in a table in database.

No input variables.

2) scrape   
  stores each table on a stats.nba.com page and stores it in a database under a unique name.
  
Inputs: 
  scrape(inputurl, year)
    inputurl - url to team stats home page e.g. (https://stats.nba.com/team/1610612738)
    year - year of season desired in (20##-##) format.
 
3) defaultget
  utilizes scrape function to scrape multiple stat pages for a given team. 
  * Chosen stat pages can be modified by changing the strings stored in the tag3 list and in reg list
  
  Inputs:
    defaultget(team, link, year)
      team: team name 
      link: same format as scrape e.g. (https://stats.nba.com/team/1610612738)
      year: same format as scrape (20##-##) format
      
 4) injuryupdate
 takes up-to-date injury information from http://rotoworld.com and stores it in a database.
 
  No input variables

3. Licensing
  
  GNU GPL v3.0 License. 
  




