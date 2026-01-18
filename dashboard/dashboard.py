import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency


# ================== Rental Harian =====
def create_dailiy_rent(df):
    daily_rent = df.resample(rule='D', on ='dteday').agg({
        'cnt':'sum',
        'totalPrice':'sum'
    }).reset_index()

    daily_rent.rename(columns={
        "cnt":'bike_rent',
        "totalPrice":"revenue"
    }, inplace=True)

    return daily_rent

# =================== Jumlah Rental berdasarkan Weekday/Weekend =====
def create_byweek(df):
    byweek_rent = df.groupby("workingday").agg({
        'casual':'sum',
        'registered':'sum',
        'cnt':'sum'
    }).reset_index()

    byweek_rent.rename(columns={
        'casual':'casual_rent',
        'registered':'member_rent',
        'cnt':'bike_rent'
    }, inplace=True)
    
    return byweek_rent

# ==================== Perentalan berdasarkan Musim =====
def create_byseason(df):
    byseason_rent = df.groupby("season").agg({
        'casual':'sum',
        'registered':'sum',
        'cnt':'sum'
    }).reset_index()

    byseason_rent.rename(columns={
        'casual':'casual_rent',
        'registered':'member_rent',
        'cnt':'bike_rent'
    }, inplace=True)
    
    return byseason_rent

# =================== Perentalan berdasarkan Jam =====
def create_byhours(df):
    byhours_rent = df.groupby('hr').agg({
        'casual':'sum',
        'registered':'sum',
        'cnt':'sum'
    }).reset_index()

    byhours_rent.rename(columns={
        'casual':'casual_rent',
        'registered':'member_rent',
        'cnt':'bike_rent'
    }, inplace=True)

    return byhours_rent

daily_data = pd.read_csv("../dataset/day_data_with_price.csv")
hourly_data = pd.read_csv("../hours_data_with_price.csv")

# ===================== Urutkan Berdasarkan dteday terbaru ===
datetime_columns = ['dteday']
daily_data.sort_values(by='dteday', inplace=True)
hourly_data.sort_values(by='dteday', inplace=True)
daily_data.reset_index(inplace=True)
hourly_data.reset_index(inplace=True)

for column in datetime_columns:
    daily_data[column] = pd.to_datetime(daily_data[column])
    hourly_data[column] = pd.to_datetime(hourly_data[column])

# ===================== KOLOM FILTER ===================================
## WIDGET DATE INPUT SEBAGAI FILTER dg SIDEBAR

min_date = daily_data['dteday'].min()
max_date = daily_data['dteday'].max()

with st.sidebar:
    st.title("Welcome to this Dashboard")

    # logo
    st.image("logo.png")

    st.text("Silahkan masukkan range tanggal untuk filter dahsboard")

    # ambil start_date & end_date dr inputan
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# data yang diambil adalah data yang masuk ke dalam range min max
main_df1 = daily_data[(daily_data["dteday"] >= str(start_date)) & (daily_data["dteday"] <= str(end_date))]
main_df2 = hourly_data[(hourly_data["dteday"] >= str(start_date)) & (hourly_data["dteday"] <= str(end_date))]

# used all helper function
daily_rent_df = create_dailiy_rent(main_df1)
byweek_rent_df = create_byweek(main_df1)
byseason_rent_df = create_byseason(main_df1)
byhour_rent_df = create_byhours(main_df2)