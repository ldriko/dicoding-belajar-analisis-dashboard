import seaborn as sns
import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

all_df = pd.read_csv("main_data.csv")
all_df["dteday"] = pd.to_datetime(all_df["dteday"]).dt.date
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()


def create_seasonal_df(df):
    df["season"] = df["season"].map({1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"})
    return df


def create_hourly_df(df):
    df.groupby("hr").agg({"cnt": "sum"})
    return df


def create_holiday_df(df):
    df["holiday"] = df["holiday"].map({0: "No", 1: "Yes"})
    return df


def create_weather_df(df):
    df["weathersit"] = df["weathersit"].map(
        {
            1: "Clear, Few clouds, Partly cloudy, Partly cloudy",
            2: "Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist",
            3: "Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds",
            4: "Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog",
        }
    )
    return df


with st.sidebar:
    st.write("## Sidebar")
    start_date, end_date = st.date_input(
        "Select a date range",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date,
    )

main_df = all_df[(all_df["dteday"] >= start_date) & (all_df["dteday"] <= end_date)]

st.header("Bike Sharing Dashboard")
st.subheader("Overview")

col1, col2 = st.columns(2)

with col1:
    st.write("## Total Rentals")
    total_rentals = main_df["cnt"].sum()
    st.write(total_rentals)

with col2:
    st.write("## Average Rentals per Hour")
    average_rentals = main_df["cnt"].mean()
    st.write(average_rentals)

st.subheader("Seasonal Bike Rentals")

seasonal_rentals = create_seasonal_df(main_df)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=seasonal_rentals, x="season", y="cnt", ax=ax)
st.pyplot(fig)

st.subheader("Bike Rentals by Weekday")
hourly_rentals = create_hourly_df(main_df)
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=hourly_rentals, x="hr", y="cnt", ax=ax, hue="weekday")
st.pyplot(fig)

st.subheader("Bike Rentals on Holidays")
holiday_rentals = create_holiday_df(main_df)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=holiday_rentals, x="holiday", y="cnt", ax=ax)
st.pyplot(fig)

st.subheader("Bike Rentals by Weather")
weather_rentals = create_weather_df(main_df)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=weather_rentals, x="weathersit", y="cnt", ax=ax)
plt.xticks(rotation=90)
st.pyplot(fig)
