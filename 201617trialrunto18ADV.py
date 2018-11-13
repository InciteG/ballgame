import datetime
import time
import sqlite3
import pandas as pd
import numpy as np
dict = {'ATL': 'ATLANTA HAWKS',
    'BOS': 'BOSTON CELTICS',
    'BKN': 'BROOKLYN NETS',
    'CHA': 'CHARLOTTE HORNETS',
    'CHI': 'CHICAGO BULLS',
    'CLE': 'CLEVELAND CAVALIERS',
    'DAL': 'DALLAS MAVERICKS',
    'DEN': 'DENVER NUGGETS',
    'DET': 'DETROIT PISTONS',
    'GSW': 'GOLDEN STATE WARRIORS',
    'HOU': 'HOUSTON ROCKETS',
    'IND': 'INDIANA PACERS',
    'LAC': 'L A CLIPPERS',
    'LAL': 'LOS ANGELES LAKERS',
    'MEM': 'MEMPHIS GRIZZLIES',
    'MIA': 'MIAMI HEAT',
    'MIL': 'MILWAUKEE BUCKS',
    'MIN': 'MINNESOTA TIMBERWOLVES',
    'NOP': 'NEW ORLEANS PELICANS',
    'NYK': 'NEW YORK KNICKS',
    'OKC': 'OKLAHOMA CITY THUNDER',
    'ORL': 'ORLANDO MAGIC',
    'PHI': 'PHILADELPHIA 76ERS',
    'PHX': 'PHOENIX SUNS',
    'POR': 'PORTLAND TRAIL BLAZERS',
    'SAC': 'SACRAMENTO KINGS',
    'SAS': 'SAN ANTONIO SPURS',
    'TOR': 'TORONTO RAPTORS',
    'UTA': 'UTAH JAZZ',
    'WAS': 'WASHINGTON WIZARDS'}
conn = sqlite3.connect('Test3.db')
cur = conn.cursor()

def dataframe(dataset, column):
    df = pd.DataFrame(data = dataset, columns=column)
    return df

def resulttable(condition, year, data):
    tablename = "[" + condition + " " + year + "]"
    cur.execute('CREATE TABLE IF NOT EXISTS' + tablename + '(Team TEXT, Right REAL, Wrong REAL, Difmean REAL, Percentage REAl)')
    cur.execute('DELETE FROM'+ tablename)
    cur.executemany('INSERT INTO' + tablename + '(Team,Right,Wrong,Difmean,Percentage) VALUES(?,?,?,?,?)', (data))
    conn.commit()

# def columnheadconvert(lists):
#     listconvhold = []
#     lists[0] = 'Team'
#     for item in lists:
#         change = list(item)
#         change.insert(0, '\'')
#         change.insert(len(change), '\'')
#         change.insert(len(change), ', ')
#         changeback = ''.join(change)
#         listconvhold.append(changeback)
#     strhold = ''.join(listconvhold)
#     rech = list(strhold)
#     rech.pop()
#     rech.pop()
#     strc = ''.join(rech)
#     strfin = '[' + strc + ']'
#     return strfin
def teamlocation(team, year):
    q = []
    tablename = '[' + team + ' ' + year + ' ' + 'Team Stats Traditional Location]'
    cur.execute('SELECT * FROM ' + tablename)
    col = cur.description
    for u in col:
        q.append(u[0])
    y = cur.fetchall()
    home = list(y[0])
    away = list(y[1])
    tablename1 = '[' + team + ' ' + year + ' ' + 'Team Stats Advanced Location]'
    cur.execute('SELECT * FROM ' + tablename1)
    col1 = cur.description
    col1l = list(col1)
    col1l.pop(0)
    col1l.pop(0)
    col1l.pop(0)
    for j in col1l:
        q.append(j[0])
    z = cur.fetchall()
    hometoadv = list(z[0])
    hometoadv.pop(0)
    hometoadv.pop(0)
    hometoadv.pop(0)
    awaytoadv = list(z[1])
    awaytoadv.pop(0)
    awaytoadv.pop(0)
    awaytoadv.pop(0)

    tablename2 = '[' + team + ' ' + year + ' ' + 'Team Stats Traditional Overall]'
    cur.execute('SELECT * FROM ' + tablename2)
    ovr = cur.fetchall()
    ovr = list(ovr[0])
    tablename3 = '[' + team + ' ' + year + ' ' + 'Team Stats Advanced Overall]'
    cur.execute('SELECT * FROM ' + tablename3)
    ovr2 = cur.fetchall()
    ovr2 = list(ovr2[0])
    ovr2.pop(0)
    ovr2.pop(0)
    ovr2.pop(0)

    overall = []

    for x,y,z in zip(hometoadv, awaytoadv, ovr2):
        home.append(x)
        away.append(y)
        ovr.append(z)
    q[0] = team
    df = dataframe([ovr,home,away], q)
    return df

def teamlocationcomp(team, year):
    q = []
    tablename = '[' + team + ' ' + year + ' ' + 'Team Stats Traditional Location]'
    cur.execute('SELECT * FROM ' + tablename)
    col = cur.description
    for u in col:
        q.append(u[0])
    y = cur.fetchall()
    home = list(y[0])
    away = list(y[1])
    tablename1 = '[' + team + ' ' + year + ' ' + 'Team Stats Advanced Location]'
    cur.execute('SELECT * FROM ' + tablename1)
    col1 = cur.description
    col1l = list(col1)
    col1l.pop(0)
    col1l.pop(0)
    col1l.pop(0)
    for j in col1l:
        q.append(j[0])
    z = cur.fetchall()
    hometoadv = list(z[0])
    hometoadv.pop(0)
    hometoadv.pop(0)
    hometoadv.pop(0)
    awaytoadv = list(z[1])
    awaytoadv.pop(0)
    awaytoadv.pop(0)
    awaytoadv.pop(0)

    for x,y in zip(hometoadv, awaytoadv):
        home.append(x)
        away.append(y)
    home[0] = team
    away[0] = team
    return home, away, q

def locationtest(year):
    teamnames = []
    cur.execute('SELECT Team FROM [NBA URL Table];')
    team = cur.fetchall()
    conn.commit()
    for team in team:
        str = "".join(team)
        teamnames.append(str.upper())
    year = '2016-17'
    colhead = teamlocationcomp('BOSTON CELTICS', year)[2]
    homestore = []
    awaystore = []
    totstore = []
    for teams in teamnames:
        store = teamlocationcomp(teams, year)
        home = store[0]
        away = store[1]
        homestore.append(home)
        awaystore.append(away)

        store2 = teamlocation(teams,year)
        totstore.append(store2)
    hometable = dataframe(homestore, colhead)
    awaytable = dataframe(awaystore, colhead)

locationtest('2016-17')






# for team in teamnames:
#     tablename = '[' + team + " 2016-17 " + 'Team Traditional]'
#     cur.execute('SELECT Team, W, L FROM ' + tablename + 'WHERE GP=82.0')
#     a = cur.fetchone()
#     conn.commit()
#     a = list(a)
#     a[0] = team
#     dataset.append(a)
# result = []
# for team  in teamnames:
#     tableget = '[' + team + " " + year + ' Box Scores]'
#     cur.execute('SELECT Opponent, [W/L] FROM ' + tableget)
#     n = cur.fetchall()
#     store = []
#     print()
#     for item in n:
#         item = list(item)
#         store.append(item)
#     outstore = []
#     for item in store:
#         x = item[0]
#         value = dict.get(x)
#         y = item[1]
#         for item in dataset:
#             if team == item[0]:
#                 win = item[1]
#             else:
#                 pass
#             if value == item[0]:
#                 outcome = item[1] - win
#                 if outcome > 0:
#                     outstore.append('L')
#                 elif outcome < 0:
#                     outstore.append('W')
#                 else:
#                     outstore.append('T')
#             else:
#                 pass
#
#     correct = 0
#     wrong = 0
#     for stuff,item in zip(outstore, store):
#         a = stuff == item[1]
#         if a is True:
#             correct = correct + 1
#         else:
#             wrong = wrong + 1
#     n = [team, correct, wrong]
#     result.append(n)
#
# df = dataframe(result, ['Team', 'Correct', 'Wrong'])
# stuff = df.sort_values(['Correct'], ascending=False)
# mean = df['Correct'].mean()
# add = []
# for n in result:
#     x = n[1] - mean
#     s = "%.1f" % x
#     add.append(s)
# newcol = df['Correct']-mean
# s = stuff.assign(diffrommean = df.Correct-mean)
# d = s.assign(correctpct = df.Correct/(df.Correct+df.Wrong))
# print(d)
# n = d.values.T.tolist()
# q = np.array(n)
# i = q.transpose()
# nt = i.tolist()
# nt2 = []
# for item in nt:
#     sn = []
#     sn.append(item[0])
#     sn.append(item[1])
#     sn.append(item[2])
#     item[3] = float(item[3])
#     item[3] = "%.1f" %item[3]
#     item[4] = float(item[4])
#     item[4] = "%.3f" %item[4]
#     sn.append(item[3])
#     sn.append(item[4])
#     nt2.append(sn)
#
# resulttable('More Wins 16 to 18', year, nt2)

# u = datetime.datetime.now()
# teamname =
# year = ['2016-17', '2017-18']
# cur.execute('SELECT * FROM [HOUSTON ROCKETS 2017-18 Box Scores]')
# a = cur.fetchall()
# conn.commit()
# b = list(reversed(a))
# c = b
#
# for cond in c:
#     present = list(cond[0])
#     a1 = present[6:10]
#     a1 = '' .join(a1)
#     a1 = int(a1)
#     a2 = present[3:5]
#     a2 = '' .join(a2)
#     a2 = int(a2)
#     a3 = present[0:2]
#     a3 = '' .join(a3)
#     a3 = int(a3)
#     for date in b:
#         c = list(date[0])
#         d = c[0:2]
#         d = '' .join(d)
#         d = int(d)
#         e = c[3:5]
#         e = '' .join(e)
#         e = int(e)
#         f = c[6:10]
#         f = '' .join(f)
#         f = int(f)
#         condition = datetime.datetime(f, d, e) < datetime.datetime(a1, a3, a2)
#         if condition is True:
#             print(date[0] + 'Matches')
#         else:
#             pass
#     print('------------------------------------------')
#     # present = datetime.datetime.now().strftime('%Y-%m-%d')

# a = datetime.datetime(2017, 1, 1) > u
# print(a)
