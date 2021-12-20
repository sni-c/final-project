import requests
import json

def store_rec20_sales(collection):
   
   url = "https://api.opensea.io/api/v1/assets?order_by=sale_date&order_direction=desc&offset=0&limit=20&collection=%s" % collection

   try:
      response = requests.request("GET", url)

      text = json.loads(response.text)

      collections = {}
      i = 0

      for i in range(0,20):
         name = {}
         name['nftid'] = text['assets'][i]['id']
         name['num_sales'] = text['assets'][i]['num_sales']
         name['image_url'] = text['assets'][i]['image_original_url']
         name['name'] = text['assets'][i]['name']
         name['event_timestamp'] = text['assets'][i]['last_sale']['event_timestamp']
         name['eth_price'] = text['assets'][i]['last_sale']['payment_token']['eth_price']
         name['usd_price'] = text['assets'][i]['last_sale']['payment_token']['usd_price']
         collections['values'] = name
      return collections

   except:
      return None
