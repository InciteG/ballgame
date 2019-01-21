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

"""Module Setup"""
from bs4 import BeautifulSoup
import time
import sqlite3
import datetime
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

"""Webdriver Setup and SQL Setup"""
chrome_options = Options()
chrome_options.binary_location = r"C:\Users\Gary_Guo\AppData\Local\Google\Chrome SxS\Application\chrome.exe"
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-gpu")

conn = sqlite3.connect('TeamStats.db')
cur = conn.cursor()

driver = webdriver.Chrome(r"C:\Users\Gary_Guo\AppData\Local\Google\Chrome SxS\Application\chromedriver.exe", chrome_options=chrome_options)
driver.implicitly_wait(4)

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
        itemlist.append(item2[1])
        for a in item2[2::]:
            if a.islower() or a == '6':
                itemlist.append(a)
            elif a.isupper():
                itemlist.append(" ")
                itemlist.append(a)
                store = a
            elif a == '7':
                itemlist.append(" ")
                itemlist.append(a)
                store = a
        input = "" .join(itemlist)
        teamlist2.append(input)
    print(teamlist2)
    cur.execute('CREATE TABLE IF NOT EXISTS [NBA URL Table](Team TEXT, Url TEXT)')
    cur.execute('DELETE FROM [NBA URL Table]')
    cur.executemany('INSERT INTO [NBA URL Table](Team, Url) VALUES (?,?)', zip(teamlist2,teamurltag))
    conn.commit()
    return
"""Obtain latest injury report information for the NBA from http://www.rotoworld.com
Name; Status; Date Condition was updated; Injury; Potential return; Team of player"""
def injuryupdate():
    cur.execute('CREATE TABLE IF NOT EXISTS [Player Injury List]([Name] TEXT, [Status] TEXT, [Date] TEXT, Injury TEXT, Returns TEXT, Team TEXT)')
    cur.execute('DELETE FROM [Player Injury List]')
    x = requests.get('http://www.rotoworld.com/teams/injuries/nba/all/').text
    soup = BeautifulSoup(x, 'lxml')
    a = soup.find_all('div', class_='pb')
    for s in a:
        n = s.find('div', class_='player')
        b = s.find('table')
        u = b.find_all('tr')
        dat = []
        for r in u:
            y = r.find_all('td')
            y = [ele.text for ele in y]
            dat.append(y)
        for q in dat:
            q.pop(1)
            q.pop(1)
        head = dat[0]
        head.insert(6, 'Team')
        dat.pop(0)
        for y in dat:
            str = y[2]
            lst = list(str)
            lst.pop(3)
            lst.insert(3, ' ')
            if len(lst) == 5:
                lst.insert(4, '0')
            else:
                pass
            str = ''.join(lst)
            y.insert(3, str)
            y.pop(2)
            y.insert(6, n.text)
        cur.executemany('INSERT INTO [Player Injury List]([Name], [Status], [Date], Injury, Returns, Team) VALUES (?,?,?,?,?,?)', (dat))
        conn.commit()

"""Default conditions for scraping based on stat pages relevant to my personal interest"""
def defaultget(team, link, year):
    tag3 = ['traditional/',  'advanced/', 'players-traditional/', 'players-advanced/', 'onoffcourt-advanced/', 'boxscores/', 'boxscores-advanced/']
    seasontype = ['&SeasonType=Regular%20Season','&SeasonType=Playoffs']
    permode = ['', '&PerMode=Per100Possessions', '&PerMode=Per36']
    yeartag = '?Season='+ year
    cur.execute('CREATE TABLE IF NOT EXISTS [Table Names]([Table Name] TEXT, [Columns] TEXT, [Value] TEXT)')
    cur.execute("SELECT name FROM sqlite_master;")
    tabletuple = cur.fetchall()
    conn.commit()
    tablestr = []
    for item in tabletuple:
        item2 = ''.join(item)
        tablestr.append(item2)
    reg = ['Team Stats Traditional DaysRest', 'Team Stats Advanced DaysRest', 'Players Traditional Players', 'Players Advanced Players', 'On/Off Court Advanced OffCourt', 'Box Scores','Advanced Box Scores Advanced']
    for name, tag in zip(reg, tag3):
        tablename = team.upper() + " " + year + " " + name
        if tablename in tablestr:
            print('No need ' + tablename)
        else:
            inputurl = link + tag + yeartag +  seasontype[0]
            scrape(inputurl, year)

"""Generic scraping function for all stats pages on http://stats.nba.com
Special formatting changes for Boxscores:
Date format change from 'October, 21, 2017' to '10/21/2017'
Boxscore table for season with more than 70 games in a year have two pages of data - identify whether the next button exists to click or not """
def scrape(inputurl, year):
    driver.get(inputurl)
    city = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[2]/div/div/div[1]/div/div/div[2]/div[1]').text
    teamname = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[2]/div/div/div[1]/div/div/div[2]/div[2]').text
    deny = 1
    store = []
    s = driver.find_elements_by_class_name('toggle-nav-component__button')
    for stuff in s:
        d =  stuff.get_attribute('innerHTML')
        soup = BeautifulSoup(d,'lxml')
        tag = soup.find('a')
        store.append(tag.text)
    x = store[1]
    y = store[2]
    if y == '':
        define = x
    else:
        define = x + " " + y
    seasonstr = " " + year + " "
    team = city + " " + teamname
    #team advanced overall
    cond = 1
    try:
        s = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div/nba-stat-table/div[1]/div/div/a[2]')
    except NoSuchElementException:
        cond = 0
    if cond == 0:
        a = driver.find_elements_by_class_name('nba-stat-table')
        for q in a:
            content =  q.get_attribute('innerHTML')
            soup = BeautifulSoup(content,'lxml')
            tag = soup.find('table')
            c = tag.find_all('tr')
            tablecolumn = []
            data = []
            hold = []
            hold1 = []
            for row in c:
                x = row.find_all('td')
                x = [ele.text for ele in x]
                data.append(x)
                y = row.find_all('th')
                for th in y:
                    cort = []
                    cortn = []
                    ru = list(th.text)
                    for nu in ru:
                        if nu == " ":
                            pass
                        else:
                            cort.append(nu)
                    for h in cort:
                        if h == """\n""":
                            pass
                        else:
                            cortn.append(h)
                    stj = "" .join(cortn)
                    tablecolumn.append(stj)
            data.pop(0)
            count = 0
            length = len(tablecolumn)-1
            values = ' VALUES ('
            add = ''.join(tablecolumn[0])
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
            overall = "[" + team + seasonstr + define + " " + add + "]"
            cur.execute('CREATE TABLE IF NOT EXISTS ' + overall + tableheader)
            cur.execute('DELETE FROM ' + overall)
            cur.executemany('INSERT INTO ' + overall + tableheader1 + values, (data))
            cur.execute('INSERT INTO [Table Names]([Table Name], Columns, Value) VALUES (?,?,?)', (overall, tableheader1, values))
            conn.commit()
    else:
        # est = []
        # dd = list(define)
        # for stuff in dd:
        #     if stuff == " ":
        #         pass
        #     else:
        #         est.append(stuff)
        # define = "" .join(est)
        a = driver.find_element_by_class_name('nba-stat-table')
        content =  a.get_attribute('innerHTML')
        soup = BeautifulSoup(content,'lxml')
        tag = soup.find('table')
        c = tag.find_all('tr')
        tablecolumn = []
        data = []
        hold = []
        hold1 = []
        for row in c:
            x = row.find_all('td')
            x = [ele.text for ele in x]
            data.append(x)
            y = row.find_all('th')
            for th in y:
                tablecolumn.append(th.text)
        data.pop(0)
        tablecolumn[0] = 'Opponent'
        tablecolumn.insert(0, 'Date')
        tablecolumn.insert(3, 'H/A')
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
            data.append(item)

        for item in data:
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
        overall = "[" + team + seasonstr + define + "]"
        cur.execute('CREATE TABLE IF NOT EXISTS ' + overall + tableheader)
        cur.execute('DELETE FROM ' + overall)
        cur.executemany('INSERT INTO ' + overall + tableheader1 + values, (data))
        cur.execute('INSERT INTO [Table Names]([Table Name], Columns, Value) VALUES (?,?,?)', (overall, tableheader1, values))
        conn.commit()
    return
