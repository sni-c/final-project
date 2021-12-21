with source as (
  select * from PROD.ANALYTICS.DAILYCOLLECTION_INGEST
),

stg_collection as (
  select DAILYCOLL:create_time::string AS CREATE_TIME,
  DAILYCOLL:collectionslug::string AS COLLECTIONSLUG,
  DAILYCOLL:one_day_volume::string AS one_day_volume,
  DAILYCOLL:one_day_change::string AS one_day_change,
  DAILYCOLL:one_day_sales::string AS one_day_sales,
  DAILYCOLL:one_day_average_price::string AS one_day_average_price,
  DAILYCOLL:seven_day_volume::string AS seven_day_volume,
  DAILYCOLL:seven_day_change::string AS seven_day_change,
  DAILYCOLL:seven_day_sales::string AS seven_day_sales,
  DAILYCOLL:seven_day_average_price::string AS seven_day_average_price,
  DAILYCOLL:thirty_day_volume::string AS thirty_day_volume,
  DAILYCOLL:thirty_day_change::string AS thirty_day_change,
  DAILYCOLL:thirty_day_sales::string AS thirty_day_sales,
  DAILYCOLL:thirty_day_average_price::string AS thirty_day_average_price,
  DAILYCOLL:total_volume::string AS total_volume,
  DAILYCOLL:total_sales::string AS total_sales,
  DAILYCOLL:total_supply::string AS total_supply,
  DAILYCOLL:num_owners::string AS num_owners,
  DAILYCOLL:average_price::string AS average_price,
  DAILYCOLL:market_cap::string AS market_cap,
  DAILYCOLL:floor_price::string AS floor_price
  FROM source,LATERAL FLATTEN (input => DAILYCOLL)
)
select * from stg_collection