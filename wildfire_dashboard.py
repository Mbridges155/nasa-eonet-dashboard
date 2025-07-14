import streamlit as st
import pandas as pd
import plotly.express as px

# Title of the dashboard
st.title("NASA Wildfires Dashboard")

# Load your data
@st.cache_data
def load_data():
    return pd.read_csv("eonet_events.csv")

df = load_data()

# Convert to datetime
df['data'] = pd.to_datetime(df['date'])

# Dropdown to choose category
event_types = df['category'].unique()
selected_type = st.selectbox("Choose an event category:", sorted(event_types))

# Filter by category
filtered_df = df[df['category'] == selected_type].copy()

# Convert date + extract date_only
filtered_df['date'] = pd.to_datetime(filtered_df['date'], errors='coerce')
filtered_df['date_only'] = filtered_df['date'].dt.date

# Date range slider
min_date = filtered_df['date_only'].min()
max_date = filtered_df['date_only'].max()
selected_dates = st.slider(
    "Select a date range:",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

# Filter by selected date range
filtered = filtered_df[
    (filtered_df['date_only'] >= selected_dates[0]) &
    (filtered_df['date_only'] <= selected_dates[1])
]

# Show total events
st.metric(label=f"{selected_type} in Range", value=len(filtered))

# Show the interactive map
fig = px.scatter_geo(
    filtered,
    lat='latitude',
    lon='longitude',
    hover_name='title',
    animation_frame='date_only',
    title='Wildfires Over Time (EONET)',
    projection='natural earth'
)

st.plotly_chart(fig, use_container_width=True)

# Layout: Tabs for Map, Chart, and Data Table
tab1, tab2, tab3 = st.tabs(["Map", "Event Chart", "Data Table"])

with tab1:
    fig = px.scatter_geo(
        filtered,
        lat='latitude',
        lon='longitude',
        hover_name='title',
        animation_frame='date_only',
        color='title',
        title=f'{selected_type} Events Over Time (EONET)',
        projection='natural earth'
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Number of Events per Day")

    daily_counts = filtered['date_only'].value_counts().sort_index()

    fig_bar = px.bar(
        x=daily_counts.index,
        y=daily_counts.values,
        labels={'x': 'Date', 'y': 'Event Count'},
        title='Event Frequency Over Time'
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with tab3:
    st.subheader("Filtered Event Data")
    st.dataframe(filtered)

# Add download button
csv = filtered.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Data as CSV",
    data=csv,
    file_name=f"{selected_type.lower()}_events.csv",
    mime='text/csv'
)