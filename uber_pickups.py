import streamlit as st 
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')

date_column = 'date/time'
data_url = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data = pd.read_csv(data_url, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[date_column] = pd.to_datetime(data[date_column])
    return data

#data loading
datasetState = st.text('Loading dataset...')

#load 10000 rows of dataset
data = load_data(10000)

#notifying data fetching was successful
datasetState.text('Done! (using st.cache)')

#momitoring dataset
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
#generating histogram
hist = np.histogram(
    data[date_column].dt.hour, bins=24, range=(0, 24))[0]

st.bar_chart(hist)

#concentration of traffic at 17:00
hours = st.slider('hour', 0, 23, 17)
filteredData = data[data[date_column].dt.hour == hours]
st.subheader(f'Map of all pickups at {hours}:00')
st.map(filteredData)