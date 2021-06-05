import sqlite3

#sqlite
con = sqlite3.connect('linkedin.db')
cur = con.cursor()

cur.execute("DELETE from vacancies WHERE url like 'h'")