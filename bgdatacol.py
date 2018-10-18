""" BALLGAME DATA COLLECTION SCRIPT """
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
driver.implicitly_wait(8) #allow time for webpage to load

"""Url Setup"""
def url_set():
    url = 'https://stats.nba.com/teams/'
    base = 'https://stats.nba.com'
    teamurltag = []
    teamlist = []
    teamlist2 = []
    driver.get(url)
    a = driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/div')
    source = a.get_attribute('innerHTML')
    soup = BeautifulSoup(source,'lxml')
    id = soup.find_all('a', href=True)
    for item in id:
        teamurltag.append(base + item['href'])
    team = soup.find_all('a')
    for item in team:
        teamlist.append(item.text)
    for item in teamlist:
        itemlist= []
        item2 = list(item)
        item2 = [x for x in item2 if ' ' not in x]
        item2.pop(0)
        item2.pop()
        itemlist.append(item2[0])
        for a in item2[1::]:
            if a.islower() or a == '6':
                itemlist.append(a)
            elif a.isupper():
                itemlist.append(" ")
                itemlist.append(a)
            elif a == '7':
                itemlist.append(" ")
                itemlist.append(a)
        input = "" .join(itemlist)
        teamlist2.append(input)
    cur.execute('CREATE TABLE IF NOT EXISTS [NBA URL Table](Team TEXT, Url TEXT)')
    cur.execute('DELETE FROM [NBA URL Table]')
    cur.executemany('INSERT INTO [NBA URL Table](Team, Url) VALUES (?,?)', zip(teamlist2,teamurltag))
    conn.commit()
    return

"""Main Class Action"""

class NBAScrape():

    def __init__(self, url, team):
        self.link = url
        self.inputurl = url
        self.tag3 = ['traditional/',  'advanced/', 'players-traditional/', 'players-advanced/', 'onoffcourt-advanced/', 'onoffcourt-traditionl/', 'boxscores/', 'boxscores-advanced/', 'four-factors/', 'opponent/']
        self.yeartag = ['?Season=2016-17','?Season=2017-18']
        self.seasontype = ['&SeasonType=Regular%20Season','&SeasonType=Playoffs']
        self.permode = ['', '&PerMode=Per100Possessions', '&PerMode=Per36']
        self.define = ''
        self.teamname = team.upper()
        self.year = ''
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
        cur.execute('CREATE TABLE IF NOT EXISTS [Table Names]([Table Name] TEXT, [Columns] TEXT, [Value] TEXT)')
        cur.execute("SELECT name FROM sqlite_master;")
        tabletuple = cur.fetchall()
        conn.commit()
        tablestr = []
        for item in tabletuple:
            item2 = ''.join(item)
            tablestr.append(item2)
        year = ['2016-17', '2017-18']
        define = ['Team Traditional', 'Team Advanced']
        for year, tag in zip(year, self.yeartag):
            tablename = self.teamname + " "+ year + " " + define[0]
            if tablename in tablestr:
                print('No need teamtrad')
            else:
                self.define = define[0]
                self.inputurl = self.link + self.tag3[0] + tag +  self.seasontype[0]
                self.getteamstat()
            tablename = self.teamname + " "+ year + " " + define[1]
            if tablename in tablestr:
                print('No need teamadv')
            else:
                self.define = define[1]
                self.inputurl = self.link + self.tag3[1] + tag +  self.seasontype[0]
                self.getteamstat()
        year = ['2016-17', '2017-18']
        define = ['Player Traditional', 'Player Advanced']
        for year, tag in zip(year, self.yeartag):
            tablename = self.teamname + " "+ year + " " + define[0]
            if tablename in tablestr:
                print('No need playertrad')
            else:
                self.define = define[0]
                self.inputurl = self.link + self.tag3[2] + tag +  self.seasontype[0]
                self.getplayerstat()
            tablename = self.teamname + " "+ year + " " + define[1]
            if tablename in tablestr:
                print('No need playeradv')
            else:
                self.define = define[1]
                self.inputurl = self.link + self.tag3[3] + tag +  self.seasontype[0]
                self.getplayerstat()
        year = ['2016-17', '2017-18']
        define = 'On Court'
        for year, tag in zip(year, self.yeartag):
            tablename = self.teamname + " "+ year + " " + define
            if tablename in tablestr:
                print('No need onoff')

            else:
                self.inputurl = self.link + self.tag3[4] + tag +  self.seasontype[0]
                self.getplayeronoff()
        year = ['2016-17', '2017-18']
        define = ['Box Scores', 'Box Scores Advanced']
        for yr, tag in zip(year, self.yeartag):
            tablename = self.teamname + " "+ yr + " " + define[0]

            self.year = yr
            if tablename in tablestr:
                print('No need boxscores')
            else:
                self.define = define[0]
                self.inputurl = self.link + self.tag3[6] + tag +  self.seasontype[0]
                self.getboxscores()
            tablename = self.teamname + " "+ yr + " " + define[1]
            if tablename in tablestr:
                print('No need boxscoresadv')
            else:
                self.define = define[1]
                self.inputurl = self.link + self.tag3[7] + tag +  self.seasontype[0]
                self.getboxscores()
        return

    def getteamstat(self):
        driver.get(self.inputurl)
        self.season = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div/nba-stat-table[1]/div[2]/div[2]/table/tbody/tr/td').text
        seasonstr = " " + self.season + " "

        #team traditional overall
        a = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div/nba-stat-table[1]/div[2]')
        content =  a.get_attribute('innerHTML')
        soup = BeautifulSoup(content,'lxml')
        tag = soup.find('table')
        c = tag.find_all('tr')
        tablecolumn = []
        overallteam = []
        HA = []
        rest = []
        hold = []
        hold1 = []
        for row in c:
            x = row.find_all('td')
            for td in x:
                self.teamoverall.append(td.text)
                overallteam.append(td.text)
            y = row.find_all('th')
            for th in y:
                tablecolumn.append(th.text)
        tablecolumn1 = tablecolumn
        tablecolumn[0] = 'CONDITION'
        tablecolumn1[0] = 'Team'
        overallteam[0] = 'Overall'
        count = 0
        length = len(tablecolumn)-1
        values = ' VALUES ('
        for item in tablecolumn:
            if count == 0:
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
        overall = "[" + self.teamname + seasonstr + self.define + "]"
        executestr = 'CREATE TABLE IF NOT EXISTS ' + overall + tableheader
        cur.execute(executestr)
        cur.execute('DELETE FROM ' + overall)
        cur.execute('INSERT INTO ' + overall + tableheader1 + values, (overallteam))

        #team traditional homeaway
        a = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div/nba-stat-table[2]/div[2]/div[1]')
        content =  a.get_attribute('innerHTML')
        soup = BeautifulSoup(content,'lxml')
        tag = soup.find('table')
        c = tag.find_all('tr')
        for row in c:
            x = row.find_all('td')
            x = [ele.text for ele in x]
            self.teamHA.append(x)
            HA.append(x)
            y = row.find_all('th')
            for th in y:
                tablecolumn.append(th.text)
        self.teamHA.pop(0)
        HA.pop(0)
        cur.executemany('INSERT INTO ' + overall + tableheader1 + values, (HA))
        conn.commit()

        #team traditional rest
        a = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div/nba-stat-table[6]/div[2]/div[1]')
        content =  a.get_attribute('innerHTML')
        soup = BeautifulSoup(content,'lxml')
        tag = soup.find('table')
        c = tag.find_all('tr')
        for row in c:
            x = row.find_all('td')
            x = [ele.text for ele in x]
            self.teamrest.append(x)
            rest.append(x)
            y = row.find_all('th')
            for th in y:
                tablecolumn.append(th.text)
        self.teamrest.pop(0)
        rest.pop(0)
        cur.executemany('INSERT INTO ' + overall + tableheader1 + values, (rest))
        cur.execute('INSERT INTO [Table Names]([Table Name], Columns, Value) VALUES (?,?,?)', (overall, tableheader1, values))
        conn.commit()
        return

    def getplayerstat(self):
        driver.get(self.inputurl)
        self.season = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div/nba-stat-table[1]/div[2]/div[2]/table/tbody/tr/td').text
        seasonstr = " " + self.season + " "
        #team advanced overall
        a = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div/nba-stat-table[2]/div[2]')
        content =  a.get_attribute('innerHTML')
        soup = BeautifulSoup(content,'lxml')
        tag = soup.find('table')
        c = tag.find_all('tr')
        tablecolumn = []
        playergen = []
        HA = []
        rest = []
        hold = []
        hold1 = []
        for row in c:
            x = row.find_all('td')
            x = [ele.text for ele in x]
            playergen.append(x)
            y = row.find_all('th')
            for th in y:
                tablecolumn.append(th.text)
        playergen.pop(0)
        count = 0
        length = len(tablecolumn)-1
        values = ' VALUES ('
        for item in tablecolumn:
            if count == 0:
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
        overall = "[" + self.teamname + seasonstr + self.define + "]"
        executestr = 'CREATE TABLE IF NOT EXISTS ' + overall + tableheader
        cur.execute(executestr)
        cur.execute('DELETE FROM ' + overall)
        cur.executemany('INSERT INTO ' + overall + tableheader1 + values, (playergen))
        cur.execute('INSERT INTO [Table Names]([Table Name], Columns, Value) VALUES (?,?,?)', (overall, tableheader1, values))
        conn.commit()
        return

    def getplayeronoff(self):
            driver.get(self.inputurl)
            self.season = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div/nba-stat-table[1]/div[2]/div[2]/table/tbody/tr/td').text
            seasonstr = " " + self.season + " "

            #team advanced overall
            a = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div/nba-stat-table[2]/div[2]/div[1]')
            content =  a.get_attribute('innerHTML')
            soup = BeautifulSoup(content,'lxml')
            tag = soup.find('table')
            c = tag.find_all('tr')
            tablecolumn = []
            playeron = []
            hold = []
            hold1 = []
            for row in c:
                x = row.find_all('td')
                x = [ele.text for ele in x]
                playeron.append(x)
                y = row.find_all('th')
                for th in y:
                    tablecolumn.append(th.text)
            playeron.pop(0)
            tablecolumn[0] = 'Players'
            count = 0
            length = len(tablecolumn)-1
            values = ' VALUES ('
            for item in tablecolumn:
                if count == 0:
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
            overall = "[" + self.teamname + seasonstr + "On Court]"
            executestr = 'CREATE TABLE IF NOT EXISTS ' + overall + tableheader
            cur.execute(executestr)
            cur.execute('DELETE FROM ' + overall)
            cur.executemany('INSERT INTO ' + overall + tableheader1 + values, (playeron))
            cur.execute('INSERT INTO [Table Names]([Table Name], Columns, Value) VALUES (?,?,?)', (overall, tableheader1, values))
            conn.commit()

            a = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div/nba-stat-table[3]/div[2]/div[1]')
            content =  a.get_attribute('innerHTML')
            soup = BeautifulSoup(content,'lxml')
            tag = soup.find('table')
            c = tag.find_all('tr')
            tablecolumn1 = []
            playeroff = []
            hold = []
            hold1 = []
            for row in c:
                x = row.find_all('td')
                x = [ele.text for ele in x]
                playeroff.append(x)
                y = row.find_all('th')
                for th in y:
                    tablecolumn1.append(th.text)
            playeroff.pop(0)
            count = 0
            tablecolumn1[0] = 'Players'
            length = len(tablecolumn)-1
            values = ' VALUES ('
            for item in tablecolumn:
                if count == 0:
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
            overall = "[" + self.teamname + seasonstr + "Off Court]"
            executestr = 'CREATE TABLE IF NOT EXISTS ' + overall + tableheader
            cur.execute(executestr)
            cur.execute('DELETE FROM ' + overall)
            cur.executemany('INSERT INTO ' + overall + tableheader1 + values, (playeroff))
            cur.execute('INSERT INTO [Table Names]([Table Name], Columns, Value) VALUES (?,?,?)', (overall, tableheader1, values))
            conn.commit()
            return
    def getboxscores(self):
        driver.get(self.inputurl)
        seasonstr = " " + self.year + " "

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
            if count < 4:
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
        overall = "[" + self.teamname + seasonstr + self.define + "]"
        executestr = 'CREATE TABLE IF NOT EXISTS ' + overall + tableheader
        cur.execute(executestr)
        cur.execute('DELETE FROM ' + overall)
        cur.executemany('INSERT INTO ' + overall + tableheader1 + values, (boxscores))
        cur.execute('INSERT INTO [Table Names]([Table Name], Columns, Value) VALUES (?,?,?)', (overall, tableheader1, values))
        conn.commit()
        return

"""Main Class Action"""

class NBAUpdate():

    def __init__(self, url, team):
        self.link = url
        self.inputurl = url
        self.tag3 = ['traditional/',  'advanced/', 'players-traditional/', 'players-advanced/', 'onoffcourt-advanced/', 'onoffcourt-traditionl/', 'boxscores/', 'four-factors/', 'opponent/']
        self.yeartag = '?Season=2018-19'
        self.seasontype = ['&SeasonType=Regular%20Season','&SeasonType=Playoffs']
        self.permode = ['', '&PerMode=Per100Possessions', '&PerMode=Per36']
        self.define = ''
        self.teamname = team.upper()
        self.year = '2018-19'
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
        cur.execute("SELECT name FROM sqlite_master;")
        tabletuple = cur.fetchall()
        conn.commit()
        tablestr = []
        for item in tabletuple:
            item2 = ''.join(item)
            tablestr.append(item2)

        define = ['Team Traditional', 'Team Advanced']
        tablename = self.teamname + " "+ self.year + " " + define[0]
        if tablename in tablestr:
            print('No need teamtrad')
        else:
            self.define = define[0]
            self.inputurl = self.link + self.tag3[0] + self.yeartag +  self.seasontype[0]
            self.getteamstat()
        tablename = self.teamname + " "+ self.year + " " + define[1]
        if tablename in tablestr:
            print('No need teamadv')
        else:
            self.define = define[1]
            self.inputurl = self.link + self.tag3[1] + self.yeartag +  self.seasontype[0]
            self.getteamstat()

        define = ['Player Traditional', 'Player Advanced']
        tablename = self.teamname + " "+ self.year + " " + define[0]
        if tablename in tablestr:
            print('No need playertrad')
        else:
            self.define = define[0]
            self.inputurl = self.link + self.tag3[2] + self.yeartag +  self.seasontype[0]
            self.getplayerstat()
        tablename = self.teamname + " "+ self.year + " " + define[1]
        if tablename in tablestr:
            print('No need playeradv')
        else:
            self.define = define[1]
            self.inputurl = self.link + self.tag3[3] + self.yeartag +  self.seasontype[0]
            self.getplayerstat()

        define = 'On Court'
        tablename = self.teamname + " "+ self.year + " " + define
        if tablename in tablestr:
            print('No need onoff')

        else:
            self.inputurl = self.link + self.tag3[4] + self.yeartag +  self.seasontype[0]
            self.getplayeronoff()

        define = 'Box Scores'
        tablename = self.teamname + " "+ self.year + " " + define
        if tablename in tablestr:
            print('No need boxscores')
        else:
            self.inputurl = self.link + self.tag3[6] + self.yeartag +  self.seasontype[0]
            self.getboxscores()
        return

    def getteamstat(self):
        driver.get(self.inputurl)
        self.season = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div/nba-stat-table[1]/div[2]/div[2]/table/tbody/tr/td').text
        seasonstr = " " + self.season + " "

        #team traditional overall
        a = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div/nba-stat-table[1]/div[2]')
        content =  a.get_attribute('innerHTML')
        soup = BeautifulSoup(content,'lxml')
        tag = soup.find('table')
        c = tag.find_all('tr')
        tablecolumn = []
        overallteam = []
        HA = []
        rest = []
        hold = []
        hold1 = []
        for row in c:
            x = row.find_all('td')
            for td in x:
                self.teamoverall.append(td.text)
                overallteam.append(td.text)
            y = row.find_all('th')
            for th in y:
                tablecolumn.append(th.text)
        tablecolumn1 = tablecolumn
        tablecolumn[0] = 'CONDITION'
        tablecolumn1[0] = 'Team'
        overallteam[0] = 'Overall'
        count = 0
        length = len(tablecolumn)-1
        values = ' VALUES ('
        for item in tablecolumn:
            if count == 0:
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
        overall = "[" + self.teamname + seasonstr + self.define + "]"
        executestr = 'CREATE TABLE IF NOT EXISTS ' + overall + tableheader
        cur.execute(executestr)
        cur.execute('DELETE FROM ' + overall)
        cur.execute('INSERT INTO ' + overall + tableheader1 + values, (overallteam))

        #team traditional homeaway
        a = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div/nba-stat-table[2]/div[2]/div[1]')
        content =  a.get_attribute('innerHTML')
        soup = BeautifulSoup(content,'lxml')
        tag = soup.find('table')
        c = tag.find_all('tr')
        for row in c:
            x = row.find_all('td')
            x = [ele.text for ele in x]
            self.teamHA.append(x)
            HA.append(x)
            y = row.find_all('th')
            for th in y:
                tablecolumn.append(th.text)
        self.teamHA.pop(0)
        HA.pop(0)
        cur.executemany('INSERT INTO ' + overall + tableheader1 + values, (HA))
        conn.commit()

        #team traditional rest
        a = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div/nba-stat-table[6]/div[2]/div[1]')
        content =  a.get_attribute('innerHTML')
        soup = BeautifulSoup(content,'lxml')
        tag = soup.find('table')
        c = tag.find_all('tr')
        for row in c:
            x = row.find_all('td')
            x = [ele.text for ele in x]
            self.teamrest.append(x)
            rest.append(x)
            y = row.find_all('th')
            for th in y:
                tablecolumn.append(th.text)
        self.teamrest.pop(0)
        rest.pop(0)
        cur.executemany('INSERT INTO ' + overall + tableheader1 + values, (rest))
        cur.execute('INSERT INTO [Table Names]([Table Name], Columns, Value) VALUES (?,?,?)', (overall, tableheader1, values))
        conn.commit()
        return

    def getplayerstat(self):
        driver.get(self.inputurl)
        self.season = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div/nba-stat-table[1]/div[2]/div[2]/table/tbody/tr/td').text
        seasonstr = " " + self.season + " "
        #team advanced overall
        a = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div/nba-stat-table[2]/div[2]')
        content =  a.get_attribute('innerHTML')
        soup = BeautifulSoup(content,'lxml')
        tag = soup.find('table')
        c = tag.find_all('tr')
        tablecolumn = []
        playergen = []
        HA = []
        rest = []
        hold = []
        hold1 = []
        for row in c:
            x = row.find_all('td')
            x = [ele.text for ele in x]
            playergen.append(x)
            y = row.find_all('th')
            for th in y:
                tablecolumn.append(th.text)
        playergen.pop(0)
        count = 0
        length = len(tablecolumn)-1
        values = ' VALUES ('
        for item in tablecolumn:
            if count == 0:
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
        overall = "[" + self.teamname + seasonstr + self.define + "]"
        executestr = 'CREATE TABLE IF NOT EXISTS ' + overall + tableheader
        cur.execute(executestr)
        cur.execute('DELETE FROM ' + overall)
        cur.executemany('INSERT INTO ' + overall + tableheader1 + values, (playergen))
        cur.execute('INSERT INTO [Table Names]([Table Name], Columns, Value) VALUES (?,?,?)', (overall, tableheader1, values))
        conn.commit()
        return

    def getplayeronoff(self):
            driver.get(self.inputurl)
            self.season = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div/nba-stat-table[1]/div[2]/div[2]/table/tbody/tr/td').text
            seasonstr = " " + self.season + " "

            #team advanced overall
            a = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div/nba-stat-table[2]/div[2]/div[1]')
            content =  a.get_attribute('innerHTML')
            soup = BeautifulSoup(content,'lxml')
            tag = soup.find('table')
            c = tag.find_all('tr')
            tablecolumn = []
            playeron = []
            hold = []
            hold1 = []
            for row in c:
                x = row.find_all('td')
                x = [ele.text for ele in x]
                playeron.append(x)
                y = row.find_all('th')
                for th in y:
                    tablecolumn.append(th.text)
            playeron.pop(0)
            tablecolumn[0] = 'Players'
            count = 0
            length = len(tablecolumn)-1
            values = ' VALUES ('
            for item in tablecolumn:
                if count == 0:
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
            overall = "[" + self.teamname + seasonstr + "On Court]"
            executestr = 'CREATE TABLE IF NOT EXISTS ' + overall + tableheader
            cur.execute(executestr)
            cur.execute('DELETE FROM ' + overall)
            cur.executemany('INSERT INTO ' + overall + tableheader1 + values, (playeron))
            cur.execute('INSERT INTO [Table Names]([Table Name], Columns, Value) VALUES (?,?,?)', (overall, tableheader1, values))
            conn.commit()

            a = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div/nba-stat-table[3]/div[2]/div[1]')
            content =  a.get_attribute('innerHTML')
            soup = BeautifulSoup(content,'lxml')
            tag = soup.find('table')
            c = tag.find_all('tr')
            tablecolumn1 = []
            playeroff = []
            hold = []
            hold1 = []
            for row in c:
                x = row.find_all('td')
                x = [ele.text for ele in x]
                playeroff.append(x)
                y = row.find_all('th')
                for th in y:
                    tablecolumn1.append(th.text)
            playeroff.pop(0)
            count = 0
            tablecolumn1[0] = 'Players'
            length = len(tablecolumn)-1
            values = ' VALUES ('
            for item in tablecolumn:
                if count == 0:
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
            overall = "[" + self.teamname + seasonstr + "Off Court]"
            executestr = 'CREATE TABLE IF NOT EXISTS ' + overall + tableheader
            cur.execute(executestr)
            cur.execute('DELETE FROM ' + overall)
            cur.executemany('INSERT INTO ' + overall + tableheader1 + values, (playeroff))
            cur.execute('INSERT INTO [Table Names]([Table Name], Columns, Value) VALUES (?,?,?)', (overall, tableheader1, values))
            conn.commit()
            return
    def getboxscores(self):
        driver.get(self.inputurl)
        seasonstr = " " + self.year + " "

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
        #
        # driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div/nba-stat-table/div[1]/div/div/a[2]').click()
        # a = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div/nba-stat-table/div[2]/div[1]')
        # content =  a.get_attribute('innerHTML')
        # soup = BeautifulSoup(content,'lxml')
        # tag = soup.find('table')
        # c = tag.find_all('tr')
        #
        # boxscores1 = []
        # for row in c:
        #     x = row.find_all('td')
        #     x = [ele.text for ele in x]
        #     boxscores1.append(x)
        # boxscores1.pop(0)
        # for item in boxscores1:
        #     boxscores.append(item)

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
            if count < 4:
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
        cur.execute('INSERT INTO [Table Names]([Table Name], Columns, Value) VALUES (?,?,?)', (overall, tableheader1, values))
        conn.commit()
        return


cur.execute("SELECT name FROM sqlite_master;")
a = cur.fetchall()
conn.commit()
b = []
for item in a:
    item2 = ''.join(item)
    b.append(item2)

if 'NBA URL Table' in b:
    teamurltag = []
    teamnames = []
    cur.execute('SELECT Url FROM[NBA URL Table];')
    url = cur.fetchall()
    for url in url:
        urlstr = '' .join(url)
        teamurltag.append(urlstr)
    cur.execute('SELECT Team FROM [NBA URL Table];')
    team = cur.fetchall()
    conn.commit()
    for team in team:
        str = "".join(team)
        teamnames.append(str)
else:
     url_set()
     teamurltag = []
     teamnames = []
     cur.execute('SELECT Url FROM [NBA URL Table];')
     url = cur.fetchall()
     for url in url:
         urlstr = '' .join(url)
         teamurltag.append(urlstr)
     cur.execute('SELECT Team FROM [NBA URL Table];')
     team = cur.fetchall()
     conn.commit()
     for team in team:
         str = "".join(team)
         teamnames.append(str)
