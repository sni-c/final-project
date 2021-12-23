import cloudscraper
import json
import requests
from bs4 import BeautifulSoup

def get_top10_collections():
  # scrapes site to obtain top 10 collections in last 7d
  scraper = cloudscraper.create_scraper(
    browser={
      'browser': 'chrome',
      'platform': 'android',
      'desktop': False
    }
  )
  try: 
    url = "https://crypto.com/price/nft-collections"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="__NEXT_DATA__")
    strresults = json.loads(results.text)

    collections = {}
    for item in strresults['props']['pageProps']['nftListResponse']['data']:
      name = {}
      name['slug'] = item['slug']
      name['index'] = item['index']
      name['assets'] = item['assets']
      name['floor_price'] = item['floor_price']
      name['sales_7d'] = item['sales_7d']
      name['volume_7d'] = item['volume_7d']
      collections[item['slug']] = name
  
  except Exception as Argument:
    f = open("logfile_scrape.txt", "a")
    f.write(str(Argument))
    f.close()
    raise Exception("Unable to scrape from Crypto.com")

  return collections;