import requests,re, time

url = 'https://www.linkedin.com/jobs/view/junior-java-developer-at-dxc-technology-2555323006/'

web = requests.session()


for x in range(500):
    req = web.get("https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Developer&location=Belgium&trk=public_jobs_jobs-search-bar_search-submit&pageNum=2&position=1&start={}".format(x))
    time.sleep(0.2)
    print([ x.split('?')[0] for x in re.findall(r"<a class=\"result-card__full-card-link\"href=\"(.*?)\"",req.text)])