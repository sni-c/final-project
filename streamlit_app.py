# streamlit_app.py

import streamlit as st
import pandas as pd
import snowflake.connector
from PIL import Image
import datetime as dt
import plotly.graph_objects as go
from plotly.colors import n_colors

# Initialize connection.
# Uses st.cache to only run once.
# @st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
def init_connection():
    return snowflake.connector.connect(**st.secrets["snowflake"])

conn = init_connection()

# Perform query.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

def color_negative_red(value):
  if value < 0:
    color = 'red'
  elif value > 0:
    color = 'green'
  else:
    color = 'black'
  return 'color: %s' % color

def streamlit_table(results, image, slug, typer):
    df = pd.DataFrame(results)
    df.columns = ['COLLECTIONSLUG', 'TOTAL_SALES', 'AVERAGE_PRICE (ETH)', 'FLOOR_PRICE (ETH)', '1D_CHANGE', '7D_CHANGE', '30D_CHANGE', '% OWNER/SUPPLY']
    df.sort_values(['%s' % typer], inplace=True, ascending=False)
    st.image(collection_image,width=60,caption=slug)
    st.table(df.style.format(subset=['AVERAGE_PRICE (ETH)', 'FLOOR_PRICE (ETH)', 'TOTAL_SALES', '1D_CHANGE', '7D_CHANGE', '30D_CHANGE','% OWNER/SUPPLY'], formatter="{:,.2f}").applymap(color_negative_red, subset=['1D_CHANGE', '7D_CHANGE', '30D_CHANGE']))

def days_between(d1, d2):
    d1 = dt.datetime.strptime(d1, "%Y-%m-%d")
    d2 = dt.datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

st.markdown("""
<style>
.small-font {
    font-size:14px !important;
}
</style>
""", unsafe_allow_html=True)

# Page hierarchy
page = st.selectbox("Choose your page", ["Home Page", "Page 1: Latest NFT Trends", "Page 2: Recent Sales"]) 

if page == "Home Page":
    # Display 10 Random Recently Sold NFT images on Home Page 
    carousell_img = run_query("WITH PRICING AS (SELECT IMAGE_URL, SOLD_PRICE, EVENT_TIMESTAMP FROM STG_SALES WHERE SOLD_PRICE IS NOT NULL LIMIT 49) SELECT * FROM PRICING ORDER BY SOLD_PRICE DESC")
    carousell_img_clean = []
    carousell_price = []
    for i in range(len(carousell_img)):
        carousell_img_clean.append(carousell_img[i][0])
        days = days_between(str(carousell_img[i][2].date()), str(dt.datetime.now().date()))
        carousell_price.append(carousell_img[i][1])
    st.image(carousell_img_clean,width=100,caption=carousell_price)


if page == "Page 1: Latest NFT Trends":

    # Display Top 10 Collections
    collection_stats_create_time = run_query("SELECT CREATE_TIME from STG_COLLECTION ORDER BY CREATE_TIME DESC LIMIT 10;")
    collection_stats = run_query("WITH RESULTING AS (SELECT IMAGE_URL, COLLECTIONSLUG, CAST(TOTAL_SALES AS INT) AS TOTAL_SALES, CAST(AVERAGE_PRICE AS FLOAT) AS AVERAGE_PRICE, CAST(FLOOR_PRICE AS FLOAT) AS FLOOR_PRICE, CAST(ONE_DAY_CHANGE AS FLOAT) AS ONE_DAY_CHANGE, CAST(SEVEN_DAY_CHANGE AS FLOAT) AS SEVEN_DAY_CHANGE, CAST(THIRTY_DAY_CHANGE AS FLOAT) AS THIRTY_DAY_CHANGE, CAST(TOTAL_SUPPLY AS INT) AS TOTAL_SUPPLY, CAST(NUM_OWNERS AS INT) AS NUM_OWNERS from PROD.DBT_SNIC.STG_COLLECTION ORDER BY CREATE_TIME DESC LIMIT 10) SELECT * FROM RESULTING ORDER BY TOTAL_SALES DESC")

    collection_image = []
    collection_slug = []
    collection_results = []
    for i in range(len(collection_stats)):
        collection_image.append(collection_stats[i][0])
        collection_slug.append(collection_stats[i][1])
        collection_results.append((collection_stats[i][1],collection_stats[i][2],collection_stats[i][3],collection_stats[i][4],collection_stats[i][5],collection_stats[i][6],collection_stats[i][7],collection_stats[i][9]/collection_stats[i][8]*100))

    st.title('Latest NFT Trends')
    st.markdown('NFT Collections by Trading Volume over Last 7 Days')
    st.markdown('<p class="small-font">Last updated on %s, %s (UTC)</p>' % (pd.to_datetime(collection_stats_create_time[0][0].split('_')[0]).strftime("%d %B %Y"), pd.to_datetime(collection_stats_create_time[0][0].split('_')[1].replace('.',':')).strftime("%I:%M %p")), unsafe_allow_html=True)

    table_type = st.radio(
        "Select table type",
        options=[
        "Sort by Total Sales",
        "Sort by Average Price",
        "Sort by Floor Price"
        ],
        )
    if table_type == "Sort by Total Sales":
        streamlit_table(collection_results, collection_image, collection_slug, 'TOTAL_SALES')
    elif table_type == "Sort by Average Price":
        streamlit_table(collection_results, collection_image, collection_slug, 'AVERAGE_PRICE (ETH)')
    else:
        streamlit_table(collection_results, collection_image, collection_slug, 'FLOOR_PRICE (ETH)')

if page == "Page 2: Recent Sales":

    sales_stats_create_time = run_query("SELECT CREATE_TIME from STG_SALES ORDER BY CREATE_TIME DESC LIMIT 10;")
    
    # Display Most Recent Sales of Each Collection

    collection_name = run_query("SELECT COLLECTIONSLUG from STG_COLLECTION ORDER BY CREATE_TIME, FLOOR_PRICE DESC LIMIT 10;")
    query1 = "SELECT ID, URL, EVENT_TIMESTAMP, NAME, SOLD_PRICE, IMAGE_URL, NUM_SALES from STG_SALES WHERE COLLECTIONSLUG = '%s' ORDER BY CREATE_TIME DESC LIMIT 20;"
    
    st.title('Recent Sales Per Collection')
    st.markdown('List of recent sales for each Top 10 collection')
    st.markdown('<p class="small-font">Last updated on %s, %s (UTC)</p>' % (pd.to_datetime(sales_stats_create_time[0][0].split('_')[0]).strftime("%d %B %Y"), pd.to_datetime(sales_stats_create_time[0][0].split('_')[1].replace('.',':')).strftime("%I:%M %p")), unsafe_allow_html=True)

    for i in range(0,10):
        linklist = []
        imagelist = []
        captionlist = []
        # Find Collection Name of Top 10 collection
        query2 = query1 % collection_name[i][0]
        sales_stats = run_query(query2)
        st.title(collection_name[i][0]) 
        for p in range(len(sales_stats)):
            imagelist.append(sales_stats[p][5])
            captionlist.append(sales_stats[p][4])
            linklist.append("[link](%s)" % sales_stats[p][1])
        try:
            st.image(imagelist,width=80,caption=captionlist)
        except:
            pass






