# BallGame Start
#run bgdatacol, run ballgameupdater

import sqlite3
import bgfunctions

conn = sqlite3.connect('TeamStats.db')
cur = conn.cursor()

"""Check if url table exists and runs bg.functions.url_set() if not"""
cur.execute("SELECT name FROM sqlite_master;")
a = cur.fetchall()
conn.commit()
b = []
for item in a: #get list of table names in database to check for 'NBA URL Table'
    item2 = ''.join(item)
    b.append(item2)

if 'NBA URL Table' in b: #if NBA URL table exists, withdraw team and respective url to python variables
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
     bgfunctions.url_set()
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

for teams, url in zip(teamnames, teamurltag):
    years = ['2016-17', '2017-18', '2018-19']
    for x in years:
        bgfunctions.defaultget(teams, url, x)
bgfunctions.driver.close()
