import re, sqlite3
from langdetect import detect

con = sqlite3.connect('linkedin.db')
cur = con.cursor()

cur.execute("SELECT url, description FROM vacancies")
data = cur.fetchall()

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
  cleantext = re.sub(cleanr, ' ', raw_html)
  return cleantext


cur.execute("DROP TABLE vacancies_e")
cur.execute('''CREATE TABLE vacancies_e
               (id integer PRIMARY KEY, url text, description text, language text)''')

id = 1
for x in data:
    d = cleanhtml(x[1])
    print(type(d))
    u = x[0]
    l = detect(str(d))
    print(l)
    cur.execute("INSERT INTO vacancies_e VALUES (?,?,?,?)",(id,str(u),str(d),l))
    con.commit()
    id+=1