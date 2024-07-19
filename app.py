import streamlit as st
import pandas as pd

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv('redbus.csv', parse_dates=['departing_time', 'reaching_time'])
    return df

data = load_data()

# Custom CSS for styling
st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://example.com/your_background_image.jpg");
        background-size: cover;
    }
    .sidebar .sidebar-content {
        background-color: rgba(248, 249, 250, 0.8);
        color: #343a40;
    }
    .stButton>button {
        background-color: #343a40;
        color: white;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #495057;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title of the app
st.title('RedBus-like Bus Booking App')

# Sidebar for search filters
st.sidebar.header('Search for Buses')

state = st.sidebar.selectbox('Select State', data['state'].unique())
route_name = st.sidebar.selectbox('Select Route', data[data['state'] == state]['route_name'].unique())
bus_type = st.sidebar.selectbox('Select Bus Type', data['bustype'].unique())

# Star Rating Slider
rating_range = st.sidebar.slider(
    'Select Star Rating Range',
    min_value=float(data['star_rating'].min()),
    max_value=float(data['star_rating'].max()),
    value=(float(data['star_rating'].min()), float(data['star_rating'].max()))
)

# Price Range Slider
price_range = st.sidebar.slider(
    'Select Price Range',
    min_value=float(data['price'].min()),
    max_value=float(data['price'].max()),
    value=(float(data['price'].min()), float(data['price'].max()))
)

# Time Filter Slider
time_filter = st.sidebar.slider(
    'Select Departure Time Range',
    min_value=data['departing_time'].dt.time.min(),
    max_value=data['departing_time'].dt.time.max(),
    value=(data['departing_time'].dt.time.min(), data['departing_time'].dt.time.max())
)

# Filter data based on selections
filtered_data = data[
    (data['state'] == state) &
    (data['route_name'] == route_name) &
    (data['bustype'] == bus_type) &
    (data['star_rating'] >= rating_range[0]) &
    (data['star_rating'] <= rating_range[1]) &
    (data['price'] >= price_range[0]) &
    (data['price'] <= price_range[1]) &
    (data['departing_time'].dt.time >= time_filter[0]) &
    (data['departing_time'].dt.time <= time_filter[1])
]

# Display available buses in a table
st.header('Available Buses')
st.dataframe(filtered_data[['busname', 'bustype', 'departing_time', 'duration', 'reaching_time', 'star_rating', 'price', 'seats_available']])

# Footer
st.write('Developed by PARIVALLAL SHANMUGAM')
