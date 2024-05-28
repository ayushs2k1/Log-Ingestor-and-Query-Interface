import streamlit as st
from elasticsearch import Elasticsearch
import pandas as pd
from datetime import datetime
import os

from dotenv import load_dotenv

load_dotenv()

# Elasticsearch connection settings
ES_HOST = os.getenv("ES_HOST")
ES_PORT = 9200
ES_INDEX = os.getenv("ES_INDEX")
ES_SCHEME = os.getenv("ES_SCHEME")

# Elasticsearch credentials
ES_USERNAME = os.getenv("ES_USERNAME")
ES_PASSWORD = os.getenv("ES_PASSWORD")


# Connect to Elasticsearch
client = Elasticsearch([{'host': ES_HOST, 'port': ES_PORT, 'scheme': ES_SCHEME}], http_auth=(ES_USERNAME, ES_PASSWORD), verify_certs=False)

# Initialize filters
@st.experimental_singleton
def init_filters():
    return {
        'start_date': datetime.now().date(),
        'end_date': datetime.now().date(),
        'level': '',
        'message': '',
        'resourceId': '',
        'traceId': '',
        'spanId': '',
        'commit': '',
        'parentResourceId': ''
    }

# Streamlit UI
st.title('Log Search Dashboard')

# Filters
filters = init_filters()
with st.sidebar:
    st.subheader('Filters')
    filters['start_date'] = st.date_input('Start Date', value=filters['start_date'])
    filters['end_date'] = st.date_input('End Date', value=filters['end_date'])
    filters['level'] = st.text_input('Level', value=filters['level'])
    filters['message'] = st.text_input('Message', value=filters['message'])
    filters['resourceId'] = st.text_input('Resource ID', value=filters['resourceId'])
    filters['traceId'] = st.text_input('Trace ID', value=filters['traceId'])
    filters['spanId'] = st.text_input('Span ID', value=filters['spanId'])
    filters['commit'] = st.text_input('Commit', value=filters['commit'])
    filters['parentResourceId'] = st.text_input('Parent Resource ID', value=filters['parentResourceId'])

# Initialize list to hold must queries
must_queries = []

# Add range query for timestamp if start_date and end_date are provided
if filters['start_date'] and filters['end_date']:
    must_queries.append({
        "range": {
            "timestamp": {
                "gte": filters['start_date'].isoformat(),  # Convert to ISO format
                "lte": filters['end_date'].isoformat()     # Convert to ISO format
            }
        }
    })

# Add individual match queries for other non-empty filters
for key, value in filters.items():
    if key not in ['start_date', 'end_date'] and value:
        must_queries.append({"match": {key: value}})



TABLE_PAGE_SIZE = 10

# Initialize pagination parameters
page_number = st.sidebar.number_input('Page Number', min_value=1, value=1)

# Calculate the starting index for the current page
from_index = (page_number - 1) * TABLE_PAGE_SIZE

print(f"---------page number is {page_number} and from_index is {from_index}--------")

# Update the query body to include pagination parameters
es_query = {
    "query": {
        "bool": {
            "must": must_queries
        }
    },
    "from": from_index,  # Starting index for the current page
    "size": TABLE_PAGE_SIZE    # Number of hits per page
}

print("Query is --> ", es_query)

# Execute the query
response = client.search(index='logrecords', body=es_query)

# Retrieve hits from the response
results = response['hits']['hits']

# Convert results to DataFrame
data = []
for hit in results:
    data.append(hit['_source'])
df = pd.DataFrame(data)

# Set the size of the dashboard to fit the size of the dataset
# st.set_page_config(layout="wide")  # Set the layout to wide

# Display results for the current page
st.subheader(f'Search Results - Page {page_number}')

if not df.empty:
    # Convert column headers to Title case
    df.columns = df.columns.str.title()

    # Color code the 'Level' column
    def colorize_level(level):
        color_map = {
            'error': 'red',
            'info': 'green',
            'warning': 'yellow',
            'debug': 'blue'
        }
        return f'background-color: {color_map.get(level.lower(), "white")}'

    styled_df = df.style.applymap(colorize_level, subset=['Level'])


    # Apply the colorize_level function to the 'Level' column
    styled_df = df.style.apply(lambda x: [colorize_level(v) if x.name == 'Level' else '' for v in x], axis=0)
    st.dataframe(styled_df, width=1200, height=len(df)*25)  # Adjust height based on the length of the DataFrame
else:
    st.write('No results found.')

# Calculate the total number of hits
total_hits = int(response['hits']['total']['value'])

# Calculate the total number of pages
total_pages = -(-total_hits // TABLE_PAGE_SIZE)  

# Display pagination information
st.sidebar.write(f'Total Records: {total_hits}')
st.sidebar.write(f'Total Pages: {total_pages}')
