import requests, re, sqlite3, csv

con = sqlite3.connect('linkedin.db')
cur = con.cursor()
cur.execute("DROP TABLE vacancies")
cur.execute('''CREATE TABLE vacancies
               (url text, description text)''')

web = requests.session()
#web.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0'})

list_of_urls = []
#22 urls per cycle?
for x in range(1000):
    print(x)
    req = web.get("https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Developer&location=Belgium&trk=public_jobs_jobs-search-bar_search-submit&pageNum=2&position=1&start={}".format(x))
    list_of_urls.extend([ x.split('?')[0] for x in re.findall(r"<a class=\"result-card__full-card-link\"href=\"(.*?)\"",req.text)])
    print("Total Length of unique URLS: {}".format(len(set(list_of_urls))))

with open('urls.csv', 'w', newline='\n') as csvfile:
    urlwriter = csv.writer(csvfile)
    for x in list(set(list_of_urls)):
        urlwriter.writerow([x])
#print(set(list_of_urls))

content = []
i = 1
myData = list(set(list_of_urls))
for x in myData:
    req = web.get(x)
    print(str(i), " out of " + str(len(myData)))
    i += 1
    res = re.findall(r"<div class=\"show-more-less-html__markup show-more-less-html__markup--clamp-after-5\">([\s\S]*?)<\/div>", req.text)
    print(res)
    content.extend(res)
print("Length of content: {}".format(len(content)))
print("Length of myData: {}".format(len(myData)))
content = zip(myData,content)
cur.executemany("insert into vacancies values (?, ?)", content)
con.commit()