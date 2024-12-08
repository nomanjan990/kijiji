import streamlit as st
import pandas as pd
import pandasql as psql
from datetime import datetime, timedelta

# Read the CSV data
df = pd.read_csv('test.csv')

# Convert the 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S').dt.date
print(df['date'])

# SQL queries to get various statistics
query_total_ads = "SELECT count(title) as 'Total Ads' from df"
query_ads_with_phone = "SELECT sum(has_phone) as 'Ads with Phone' from df"
query_categories = "SELECT count(distinct category) as 'Total Categories' from df"
query_models = "SELECT count(distinct model) as 'Total Models' from df"

# Execute SQL queries
result_total_ads = psql.sqldf(query_total_ads, locals())
result_ads_with_phone = psql.sqldf(query_ads_with_phone, locals())
result_categories = psql.sqldf(query_categories, locals())
result_models = psql.sqldf(query_models, locals())

# Get today's date and the date 30 days ago
today = datetime.today().date()
last_30_days = today - timedelta(days=30)


# SQL query to get the number of ads today
query_today = f"SELECT count(*) as 'Ads Today' from df where date = '{today}'"
result_today = psql.sqldf(query_today, locals())


# SQL query to get the number of ads in the last 30 days
query_30_days = f"SELECT count(*) as 'Ads in Last 30 Days' from df where date >= '{last_30_days}'"
result_30_days = psql.sqldf(query_30_days, locals())

# Streamlit app
st.set_page_config(page_title="Kijiji Auto Ads Analysis", layout="wide")
st.title("Kijiji Auto Ads Analysis")

# Set dark background for the entire page and white text
st.markdown("""
    <style>
        body {
            background-color: #333333; /* Dark background for the page */
            color: white;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
        }
        .stMarkdown {
            color: white;
        }
        .card {
            background-color: #FFFFFF;  /* Light background for the cards */
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            margin: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);  /* Light shadow for depth */
        }
        h3 {
            color: #333333;  /* Dark text for the card headings */
        }
        p {
            font-size: 2em;
            color: #333333;  /* Dark text for the card values */
        }
        .streamlit-expanderHeader {
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Extract results for all the queries
total_ads = result_total_ads['Total Ads'][0]
ads_with_phone = result_ads_with_phone['Ads with Phone'][0]
total_categories = result_categories['Total Categories'][0]
total_models = result_models['Total Models'][0]
ads_today = result_today['Ads Today'][0]
ads_last_30_days = result_30_days['Ads in Last 30 Days'][0]

# Create layout using Streamlit's columns for cards side by side
col1, col2, col3 = st.columns(3)

# Card for Total Ads
with col1:
    st.markdown(f"""
    <div class="card">
        <h3>Total Ads</h3>
        <p>{total_ads}</p>
    </div>
    """, unsafe_allow_html=True)

# Card for Ads with Phone
with col2:
    st.markdown(f"""
    <div class="card">
        <h3>Ads with Phone</h3>
        <p>{ads_with_phone}</p>
    </div>
    """, unsafe_allow_html=True)

# Card for Total Categories
with col3:
    st.markdown(f"""
    <div class="card">
        <h3>Total Categories</h3>
        <p>{total_categories}</p>
    </div>
    """, unsafe_allow_html=True)

# Create a new row of cards for Ads Today, Ads in Last 30 Days, and Total Models
col4, col5, col6 = st.columns(3)

# Card for Ads Today
with col4:
    st.markdown(f"""
    <div class="card">
        <h3>Ads Today</h3>
        <p>{ads_today}</p>
    </div>
    """, unsafe_allow_html=True)

# Card for Ads in Last 30 Days
with col5:
    st.markdown(f"""
    <div class="card">
        <h3>Ads in Last 30 Days</h3>
        <p>{ads_last_30_days}</p>
    </div>
    """, unsafe_allow_html=True)

# Card for Total Models
with col6:
    st.markdown(f"""
    <div class="card">
        <h3>Total Models</h3>
        <p>{total_models}</p>
    </div>
    """, unsafe_allow_html=True)

# Add a spacer to separate cards from charts
st.markdown("<hr>", unsafe_allow_html=True)

# Create the bar charts below the cards for additional insights
query_city_phone = "SELECT city, Count(has_phone) as Phone_Count from df where city !='NA' group by city"
result_city_phone = psql.sqldf(query_city_phone, locals())


# Create a bar chart for make vs Phone Count
query_make_phone = "SELECT make, Count(has_phone) as Phone_Count from df group by make order by Phone_Count desc"
result_make_phone = psql.sqldf(query_make_phone, locals())

# Display Bar Chart for Ads by make
st.subheader("Ads by Make")
make_chart = st.bar_chart(result_make_phone.set_index('make')['Phone_Count'], use_container_width=True)

# Create a bar chart for Category vs Phone Count
query_category_phone = "SELECT category, Count(has_phone) as Phone_Count from df group by category order by Phone_Count desc"
result_category_phone = psql.sqldf(query_category_phone, locals())

# Display Bar Chart for Ads by Category
st.subheader("Ads by Category")
category_chart = st.bar_chart(result_category_phone.set_index('category')['Phone_Count'], use_container_width=True)

# Customizing the appearance of the charts
st.markdown("""
    <style>
        .streamlit-expander {
            background-color: #444444;
        }
        .streamlit-chart {
            background-color: #444444;
            color: white;
        }
        .stBarChart rect {
            fill: #FF9800;  /* Custom color for bars */
            border-radius: 8px;
        }
        .stBarChart text {
            fill: white;
        }
        .stBarChart path {
            stroke: white;
        }
    </style>
""", unsafe_allow_html=True)
