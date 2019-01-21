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
driver.implicitly_wait(8) #allow time for webpage to load

"""Url Setup"""
url = 'https://stats.nba.com/teams/'
base = 'https://stats.nba.com'
teamurltag = []
driver.get(url)
a = driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/div')
source = a.get_attribute('innerHTML')
soup = BeautifulSoup(source,'lxml')
id = soup.find_all('a', href=True)
for item in id:
    teamurltag.append(base + item['href'])

"""Main Class Action"""

class NBAScrape():

    def __init__(self, url, year):
        self.link = url
        self.inputurl = url
        self.tag3 = ['traditional/', 'boxscores/','players-traditional/', 'players-advanced/', 'onoffcourt-traditionl/', 'advanced/', 'four-factors/', 'opponent/', 'onoffcourt-advanced/']
        self.yeartag = ['?Season=2016-17','?Season=2017-18']
        self.seasontype = ['&SeasonType=Regular%20Season','&SeasonType=Playoffs']
        self.permode = ['', '&PerMode=Per100Possessions', '&PerMode=Per36']
        self.soup = ''
        self.teamname = ''
        self.year = year
        self.season = ''
        self.tablename = ''
        self.teamoverall = []
        self.teamHA = []
        self.teamrest = []
        self.playergeneral = []
        self.playeradv = []
        self.playeron = []
        self.playeroff = []
        self.teamboxscore = []
        self.scrape()
        return

    def scrape(self):
        self.getboxscores()
        return

    def getboxscores(self):
        for item in self.yeartag:
            self.inputurl = self.link + self.tag3[1] + item + self.seasontype[0]
            driver.get(self.inputurl)
            city = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[2]/div/div/div[1]/div/div/div[2]/div[1]').text
            team = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[2]/div/div/div[1]/div/div/div[2]/div[2]').text
            self.teamname = city + " " + team


            #boxscore
            a = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div/nba-stat-table/div[2]/div[1]')
            content =  a.get_attribute('innerHTML')
            soup = BeautifulSoup(content,'lxml')
            tag = soup.find('table')
            c = tag.find_all('tr')
            tablecolumn = []
            boxscores = []
            hold = []
            hold1 = []
            for row in c:
                x = row.find_all('td')
                x = [ele.text for ele in x]
                boxscores.append(x)
                y = row.find_all('th')
                for th in y:
                    tablecolumn.append(th.text)
            tablecolumn[0] = 'Opponent'
            tablecolumn.insert(0, 'Date')
            tablecolumn.insert(3, 'H/A')
            boxscores.pop(0)

            seasonstr = ''
            cheese = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div/nba-stat-table/div[2]/div[2]/table/tbody/tr[1]/td/a').text
            l = list(cheese)
            if l[11] == 8:
                seasonstr = '2017-2018'
            elif l[11] == 7:
                seasonstr = '2016-2017'
            driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div/nba-stat-table/div[1]/div/div/a[2]').click()
            a = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div/nba-stat-table/div[2]/div[1]')
            content =  a.get_attribute('innerHTML')
            soup = BeautifulSoup(content,'lxml')
            tag = soup.find('table')
            c = tag.find_all('tr')

            boxscores1 = []
            for row in c:
                x = row.find_all('td')
                x = [ele.text for ele in x]
                boxscores1.append(x)
            boxscores1.pop(0)
            for item in boxscores1:
                boxscores.append(item)

            for item in boxscores:
                list2 = list(item[0])
                matchup = list2[-3:]
                matchupstr = ''.join(matchup)
                if len(list2) == 24:
                    result = ('A')
                else:
                    result = ('H')
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
                item.pop(0)
                item.insert(0, time)
                item.insert(1, matchupstr)
                item.insert(3, result)
            count = 0
            length = len(tablecolumn)-1
            values = ' VALUES ('
            for item in tablecolumn:
                if count == 0 or count == 1:
                    x = "[" + item + "] TEXT, "
                    y = "[" + item + "], "
                    values = values +"?, "
                    count = count + 1
                    hold.append(x)
                    hold1.append(y)
                elif count < length:
                    x = "[" + item + "] REAL, "
                    y = "[" + item + "], "
                    values = values +"?, "
                    hold.append(x)
                    hold1.append(y)
                    count = count + 1
                else:
                    x = "[" + item + "] REAL"
                    y = "[" + item + "])"
                    hold.append(x)
                    hold1.append(y)
                    values = values + "?)"
            str = '' .join(hold)
            str1 = '' .join(hold1)
            tableheader = '(' + str + ')'
            tableheader1 = '(' + str1
            overall = "[" + self.teamname + seasonstr + "Box Scores]"
            executestr = 'CREATE TABLE IF NOT EXISTS ' + overall + tableheader
            cur.execute(executestr)
            cur.execute('DELETE FROM ' + overall)
            cur.executemany('INSERT INTO ' + overall + tableheader1 + values, (boxscores))
            conn.commit()
        return

NBAScrape(teamurltag[1], 2017-18)
driver.quit()
