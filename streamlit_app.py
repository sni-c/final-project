# streamlit_app.py

import streamlit as st
import snowflake.connector
import pandas as pd
from PIL import Image
import datetime
import plotly.graph_objects as go
from plotly.colors import n_colors

# Initialize connection.
# Uses st.cache to only run once.
@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
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

def streamlit_table(results):
    df = pd.DataFrame(results)
    df.columns = ['COLLECTIONSLUG', 'TOTAL_SALES', 'AVERAGE_PRICE (ETH)', 'FLOOR_PRICE (ETH)']
    st.table(df.style.format(subset=['AVERAGE_PRICE (ETH)', 'FLOOR_PRICE (ETH)', 'TOTAL_SALES'], formatter="{:,.2f}"))


# Display Top 10 Collections

collection_stats_create_time = run_query("SELECT CREATE_TIME from STG_COLLECTION ORDER BY CREATE_TIME DESC LIMIT 10;")
collection_stats = run_query("SELECT COLLECTIONSLUG, CAST(TOTAL_SALES AS INT), CAST(AVERAGE_PRICE AS FLOAT), CAST(FLOOR_PRICE AS FLOAT) from STG_COLLECTION ORDER BY CREATE_TIME DESC LIMIT 10;")

st.title('Latest NFT Trends')
st.markdown('NFT Collections by Trading Volume: Last updated on %s, %s (UTC)' % (pd.to_datetime(collection_stats_create_time[0][0].split('_')[0]).strftime("%d %B %Y"), pd.to_datetime(collection_stats_create_time[0][0].split('_')[1].replace('.',':')).strftime("%I:%M %p")))
streamlit_table(collection_stats)

collection_name = run_query("SELECT COLLECTIONSLUG from STG_COLLECTION ORDER BY CREATE_TIME DESC LIMIT 10;")
query1 = "SELECT * from STG_SALES WHERE COLLECTIONSLUG = '%s' ORDER BY CREATE_TIME DESC LIMIT 10;"
queryimg = "SELECT IMAGE_URL from STG_SALES WHERE COLLECTIONSLUG = '%s' QUALIFY ROW_NUMBER() OVER (PARTITION BY IMAGE_URL ORDER BY IMAGE_URL DESC) = 1;"

st.title('Recent Sales Per Collection')
st.markdown('10 recent sales per Top 10 collection:')

for i in range(0,10):
    query2 = query1 % collection_name[i][0]
    sales_stats = run_query(query2) 
    stats_df = pd.DataFrame(sales_stats)
    st.table(stats_df)

    st.markdown('NFT Viz')
    queryimg2 = queryimg % collection_name[i][0]
    sales_images = run_query(queryimg2)
    st.image(sales_images[i][0], width = 200)


