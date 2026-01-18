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