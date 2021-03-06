import requests
import json
import datetime

def wei_converter(wei):
   eth = wei / 1000000000000000000
   return eth

def store_rec20_sales(collection):
   
   url = "https://api.opensea.io/api/v1/assets?order_by=sale_date&order_direction=desc&offset=0&limit=20&collection=%s" % collection

   x = str(datetime.datetime.now().replace(microsecond=0)).replace(' ', '_')
   datestr = x.replace(':', '.')

   try:
      response = requests.request("GET", url)

      text = json.loads(response.text)

      collectionlist = []
      i = 0

      for i in range(0,20):
         name = {}
         name['collectionslug'] = collection
         name['nftid'] = text['assets'][i]['id']
         name['permalink'] = text['assets'][i]['permalink']
         name['num_sales'] = text['assets'][i]['num_sales']
         name['name'] = text['assets'][i]['name']
         name['event_timestamp'] = text['assets'][i]['last_sale']['event_timestamp']
         name['eth_price'] = text['assets'][i]['last_sale']['payment_token']['eth_price']
         name['usd_price'] = text['assets'][i]['last_sale']['payment_token']['usd_price']
         name['sold_price'] = wei_converter(int(text['assets'][i]['last_sale']['total_price']))
         imageurl = text['assets'][i]['image_original_url'] 
         if imageurl == None:
            imageurl = text['assets'][i]['image_url']
         name['image_url'] = imageurl
         collectionlist.append(name)
         name['create_time'] = datestr
      return collectionlist

   except Exception as Argument:
      f = open("logfile_openseasales.txt", "a")
      f.write(str(Argument))
      f.close()
      raise Exception("Unable to pull from OpenSea - Sales Stats")

