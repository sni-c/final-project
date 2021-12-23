import requests
import json
import datetime

def collection_data(collection):
   
   url = "https://api.opensea.io/api/v1/collection/%s/stats" % collection

   x = str(datetime.datetime.now().replace(microsecond=0)).replace(' ', '_')
   datestr = x.replace(':', '.')

   try:
      response = requests.request("GET", url)

      text = json.loads(response.text)

      collectiondict = {}
      
      collectiondict['collectionslug'] = collection
      collectiondict['one_day_volume'] = text['stats']['one_day_volume']
      collectiondict['one_day_change'] = text['stats']['one_day_change']
      collectiondict['one_day_sales'] = text['stats']['one_day_sales']
      collectiondict['one_day_average_price'] = text['stats']['one_day_average_price']
      collectiondict['seven_day_volume'] = text['stats']['seven_day_volume']
      collectiondict['seven_day_change'] = text['stats']['seven_day_change']
      collectiondict['seven_day_sales'] = text['stats']['seven_day_sales']
      collectiondict['seven_day_average_price'] = text['stats']['seven_day_average_price']
      collectiondict['thirty_day_volume'] = text['stats']['thirty_day_volume']
      collectiondict['thirty_day_change'] = text['stats']['thirty_day_change']
      collectiondict['thirty_day_sales'] = text['stats']['thirty_day_sales']
      collectiondict['thirty_day_average_price'] = text['stats']['thirty_day_average_price']
      collectiondict['total_volume'] = text['stats']['total_volume']
      collectiondict['total_sales'] = text['stats']['total_sales']
      collectiondict['total_supply'] = text['stats']['total_supply']
      collectiondict['num_owners'] = text['stats']['num_owners']
      collectiondict['average_price'] = text['stats']['average_price']
      collectiondict['market_cap'] = text['stats']['market_cap']
      collectiondict['floor_price'] = text['stats']['floor_price']
      collectiondict['create_time'] = datestr

      return collectiondict

   except Exception as Argument:
      f = open("logfile_openseacollection.txt", "a")
      f.write(str(Argument))
      f.close()
      raise Exception("Unable to pull from OpenSea - Collection Stats")
