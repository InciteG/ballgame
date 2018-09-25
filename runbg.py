# BallGame Start
#run bgdatacol, run ballgameupdater
import bgdatacol
import sqlite3

conn = sqlite3.connect('Test1.db')
cur = conn.cursor()

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
     bgdatacol.url_set()
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

for teamurltag, teamnames in zip(teamurltag, teamnames):
    bgdatacol.NBAScrape(teamurltag, teamnames)
    # bgdatacol.NBAUpdate(teamurltag, teamnames)
bgdatacol.driver.quit()
