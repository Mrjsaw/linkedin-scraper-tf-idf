import csv, requests, time, re, sqlite3

#webscraper
web = requests.session()

#sqlite
con = sqlite3.connect('linkedin.db')
cur = con.cursor()

#reading csv file (URLS)
c = 1
s = 1
with open('urls.csv', newline='\n') as csvfile:
    urlReader = csv.reader(csvfile)
    for row in urlReader:
        req = web.get(row[0])
        time.sleep(0.2)
        res = re.findall(r"<div class=\"show-more-less-html__markup show-more-less-html__markup--clamp-after-5\">([\s\S]*?)<\/div>", req.text)
        if len(res) > 0:
            print("{} out of 571 urls saved to db".format(c))
            print("{} urls skipped".format(s-c))
            cur.executemany("insert into vacancies values (?, ?)", zip(row,res))
            con.commit()
            c+=1
        s+=1
con.close()