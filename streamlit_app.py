# streamlit_app.py

import streamlit as st
import snowflake.connector
import pandas as pd
from PIL import Image

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

collection_stats = run_query("SELECT * from STG_COLLECTION ORDER BY CREATE_TIME DESC LIMIT 10;")

st.title('Latest NFT Trends')
st.markdown('NFT Collections by Trading Volume:')
coll_df = pd.DataFrame(collection_stats)
st.table(coll_df)

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


