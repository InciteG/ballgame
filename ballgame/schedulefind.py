""" BALLGAME SCHEDULE COLLECTION SCRIPT """
"""
Objective: scrape data from stats.nba.com and store in database files
Stats Included:
Team Traditional/Advanced;
Player Traditional/Advanced;
Player On/Off;
Schedule (boxscores);
Roster
"""

# import necessary modules
"""Module Setup"""
from bs4 import BeautifulSoup #html parse with lxml
import requests
import time #delay between page requests, scrape etiquette
import sqlite3 #store database
import datetime # tell updatetime
from selenium import webdriver #access web content - dynamically loaded data
from selenium.webdriver.chrome.options import Options #change selenium settings to use canary - headless

"""Webdriver Setup and SQL Setup"""
chrome_options = Options()
chrome_options.binary_location = r"C:\Users\Gary_Guo\AppData\Local\Google\Chrome SxS\Application\chrome.exe" #access google canary instead of chrome
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-gpu")

conn = sqlite3.connect('Test1.db')
cur = conn.cursor()

driver = webdriver.Chrome(r"C:\Users\Gary_Guo\AppData\Local\Google\Chrome SxS\Application\chromedriver.exe", chrome_options=chrome_options) #call chromedriver
driver.implicitly_wait(2) #allow time for webpage to load

base = 'https://www.basketball-reference.com'
add = ['/leagues/NBA_2019_games-october.html',
        '/leagues/NBA_2019_games-november.html',
        '/leagues/NBA_2019_games-december.html',
        '/leagues/NBA_2019_games-january.html',
        '/leagues/NBA_2019_games-february.html',
        '/leagues/NBA_2019_games-march.html',
        '/leagues/NBA_2019_games-april.html',]
rowdata = []
rowheader = ['Date', 'Start(ET)', 'Visitor', 'Home']
for add in add:
    link = base + add
    driver.get(link)
    a = driver.find_element_by_id('all_schedule')
    source = a.get_attribute('innerHTML')
    soup = BeautifulSoup(source,'lxml')
    c = soup.find('tbody')
    b = c.find_all('tr')
    for row in b:
        x = row.find_all('td')
        x = [ele.text for ele in x]
        y = row.find('th')
        x.insert(0, y.text)
        rowdata.append(x)

for row in rowdata:
    row.pop()
    row.pop()
    row.pop()
    row.pop()
    row.pop()
    row.pop(3)
    list2 = list(row[0])
    list2 = list2[5:]
    if len(list2) == 11:
        da = ''.join(list2[4:5])
        day = '0' + da
        year = ''.join(list2[7:11])
    else:
        day = ''.join(list2[4:6])

        year = ''.join(list2[8:12])
    if list2[0] == 'A':
        month = '04/'
    elif list2[0] == 'M':
        month = '03/'
    elif list2[0] == 'F':
        month = '02/'
    elif list2[0] == 'J':
        month = '01/'
    elif list2[0] == 'D':
        month = '12/'
    elif list2[0] == 'N':
        month = '11/'
    elif list2[0] == 'O':
        month = '10/'
    time = month + day + '/'+ year
    row.pop(0)
    row.insert(0, time)
cur.execute('CREATE TABLE IF NOT EXISTS [NBA 2018-19 Schedule](Date TEXT, Start TEXT, Visitor TEXT, Home TEXT)')
cur.execute('DELETE FROM [NBA 2018-19 Schedule]')
cur.executemany('INSERT INTO [NBA 2018-19 Schedule](Date, Start, Visitor, Home) VALUES (?,?,?,?)', (rowdata))
cur.execute("INSERT INTO [Table Names]([Table Name], Columns, Value) VALUES (?,?,?)", ('NBA 2018-19 Schedule', '(Date, Start, Visitor, Home)', '(?,?,?,?)'))
conn.commit()
driver.quit()
