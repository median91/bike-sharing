# ===============================================================
#           CREATE DASHBOARD BIKE SHARING USING STREAMLIT       =
#           ---------------------------------------------       =
# Nama          : Jauza Krito                                   =
# Email         : jauza1998@gmail.com                           =
# Id Dicoding   : dicoding.com/users/jauzakrito/                =
# Created       : 30 September 2023                             =
# ===============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import calendar

import warnings


@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data
data = load_data("dataset/day.csv")


st.title("Bike Sharing Public Dashboard")


st.sidebar.title("Information:")
st.sidebar.markdown("**• Nama: Jauza Krito**")
st.sidebar.markdown(
    "**• Email: [jauza1998@gmail.com](jauza1998@gmail.com)**")
st.sidebar.markdown(
    "**• Dicoding: [jauzakrito](https://www.dicoding.com/users/jauzakrito/)**")
st.sidebar.markdown(
    "**• LinkedIn: [Jauza Krito](https://www.linkedin.com/in/jauzakrito/)**")


st.sidebar.title("Dataset Bike Share")

# Display summary statistics
if st.sidebar.checkbox("Show Summary Statistics"):
    st.subheader("Summary Statistics")
    st.write(data.describe())

# Show the dataset
if st.sidebar.checkbox("Show Dataset"):
    st.subheader("Raw Data")
    st.write(data)

col1, col2 = st.columns(2)

with col1:
    season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    data["season_label"] = data["season"].map(season_mapping)

    season_count = data.groupby("season_label")["cnt"].sum().reset_index()
    fig_season_count = px.bar(season_count, x="season_label",
                              y="cnt", title="Season-wise Bike Share Count")
    fig_season_count.update_xaxes(title="Season")
    fig_season_count.update_yaxes(title="Rental bikes")
    st.plotly_chart(fig_season_count, use_container_width=True,
                    height=400, width=600)

with col2:
    weather_mapping = {1: "Clear", 2: "Cloudy", 3: "Snowy", 4: "Rainy"}
    data['weather_description'] = data['weathersit'].map(weather_mapping)
    weather_count = data.groupby("weather_description")["cnt"].sum().reset_index()
    fig_weather_count = px.bar(weather_count, x="weather_description",
                            y="cnt", title="Weather Situation-wise Bike Share Count")
    fig_weather_count.update_xaxes(title="Weather Situation")
    fig_weather_count.update_yaxes(title="Rental bikes")
    st.plotly_chart(fig_weather_count, use_container_width=True, height=400, width=800)


# Showing for weekday
data["weekday_description"] = data["weekday"].apply(lambda x: calendar.day_name[x])
weekday_count = data.groupby("weekday_description")["cnt"].sum().reset_index()

fig_weekday_count = px.line(weekday_count, x="weekday_description", y="cnt", 
                            title="Weekday-wise Bike Share Count")
fig_weekday_count.update_xaxes(title="Weekday")
fig_weekday_count.update_yaxes(title="Rental bikes")
st.plotly_chart(fig_weekday_count, use_container_width=True, height=400, width=800)


# For humidity, temp, and windspeed
data['season_label'] = data['season'].map(season_mapping)

humidity_vs_cnt = data.groupby(["season_label", "hum", "temp", "windspeed"])["cnt"].sum().reset_index()

selected_season = st.selectbox("Select a season", list(season_mapping.values()))
selected_data = humidity_vs_cnt[humidity_vs_cnt["season_label"] == selected_season]

fig_humidity = px.scatter(selected_data, x="hum", y="cnt", title=f"Bike Share Count vs. Humidity for {selected_season}")
fig_humidity.update_xaxes(title="Humidity")

fig_temp = px.scatter(selected_data, x="temp", y="cnt", title=f"Bike Share Count vs. Temperature for {selected_season}")
fig_temp.update_xaxes(title="Temperature")

fig_wind = px.scatter(selected_data, x="windspeed", y="cnt", title=f"Bike Share Count vs. Windspeed for {selected_season}")
fig_wind.update_xaxes(title="Windspeed")
fig_wind.update_yaxes(title="Bike Share Count")

st.plotly_chart(fig_humidity, use_container_width=True)
st.plotly_chart(fig_temp, use_container_width=True)
st.plotly_chart(fig_wind, use_container_width=True)
