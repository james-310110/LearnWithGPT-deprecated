import requests
from bs4 import BeautifulSoup

def scrape(sites):
  urls = []
  
  def scrape_helper(current_site):
    nonlocal urls
    r = requests.get(current_site)
    s = BeautifulSoup(r.text, 'html.parser')
    for i in s.find_all("a"):
      if "href" in i.attrs:
        href = i.attrs["href"]
        if href.startswith("/") or href.startswith("#"):
          full_url = site + href
          if full_url not in urls:
            urls.append(full_url)
            scrape_helper(full_url)
  
  for site in sites:
    scrape_helper(site)
  return urls          