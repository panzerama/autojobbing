from bs4 import BeautifulSoup as bs
import requests as r
import os
import sys
import re

def is_jobs(tag):
    return tag.string == "jobs" or tag.string == "careers"


if os.path.exists('geekwire-200.md'):
    os.rename('geekwire-200.md', 'geekwire-200-past.md')

try:
    geek_wire = r.get('https://www.geekwire.com/geekwire-200/')
except:
    print("Unexpected error!")
    sys.exit()

f = open('geekwire-200.md', 'w')

if geek_wire.status_code != 200:
    print("Bad request")
else:
    geek_soup = bs(geek_wire.content, 'html.parser')

    startup_index = geek_soup.select(".title > a")

    websites = [x.attrs['href'] for x in startup_index]

    for site in websites:
        if site[-1] is not '/':
            site = site + '/'
        f.write(site + '\n')

f.close()

print("Done aquiring geekwire\'s top 200")

# follow links and retrieve 'jobs' or 'careers' links

address_file = open('geekwire-200.md', 'r')
results_file = open('job-site-links.md', 'w')

for address in address_file:
    address = address.rstrip()
    try:
        company_page = r.get(address)
        if company_page.status_code == 200:
            print("Success for " + address)
    except Exception as e:
        print("Oops, that didn't work for " + address)
        print(e)
        continue

    if company_page.status_code != 200:
        results_file.write(address + " status code : " + str(company_page.status_code) + "\n")
    else:
        jobs_re = re.compile('(jobs?)|(work)|(careers?)', re.IGNORECASE)
        company_page_soup = bs(company_page.content, 'html.parser')
        for tag in company_page_soup("a"):
            if tag.string and jobs_re.search(tag.string):
                try:
                    results_file.write("[jobs for " + address + "](" + tag['href'] + ")\n")
                except:
                    pass

address_file.close()
results_file.close()


