with source as (
  select * from PROD.ANALYTICS.RECENTSALE_INGEST
),

stg_sales as (
  select RECENTSALE:create_time::string AS CREATE_TIME,
  RECENTSALE:nftid::string AS ID,
  RECENTSALE:permalink::string AS URL,
  RECENTSALE:collectionslug::string AS COLLECTIONSLUG,
  RECENTSALE:name::string AS NAME,
  RECENTSALE:event_timestamp::timestamp AS EVENT_TIMESTAMP,
  RECENTSALE:eth_price::string AS ETH_PRICE,
  RECENTSALE:usd_price::string AS USD_PRICE,
  RECENTSALE:image_url::string AS IMAGE_URL,
  RECENTSALE:num_sales::string AS NUM_SALES
  FROM source,LATERAL FLATTEN (input => RECENTSALE)
  QUALIFY ROW_NUMBER() OVER (PARTITION BY id ORDER BY id) = 1
)
select * from stg_sales