import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency


# ================== Rental Harian =====
def create_daily_rent(df):
    daily_rent = df.resample(rule='D', on ='dteday').agg({
        'casual':'sum',
        'registered':'sum',
        'cnt':'sum',
        'totalPrice':'sum'
    }).reset_index()

    daily_rent.rename(columns={
        "casual":"casual_rent",
        "registered":"member_rent",
        "cnt":"bike_rent",
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

daily_data = pd.read_csv("dashboard/day_data_with_price.csv")
hourly_data = pd.read_csv("dashboard/hours_data_with_price.csv")

# ===================== Urutkan Berdasarkan dteday terbaru ===
# datetime_columns = ['dteday']
daily_data.sort_values(by='dteday', inplace=True)
hourly_data.sort_values(by='dteday', inplace=True)
daily_data.reset_index(drop=True, inplace=True)
hourly_data.reset_index(drop=True, inplace=True)

daily_data["dteday"] = pd.to_datetime(daily_data["dteday"])
hourly_data["dteday"] = pd.to_datetime(hourly_data["dteday"])

# ===================== KOLOM FILTER ===================================
## WIDGET DATE INPUT SEBAGAI FILTER dg SIDEBAR

min_date = daily_data['dteday'].min()
max_date = daily_data['dteday'].max()

with st.sidebar:
    st.title("Welcome to this Dashboard")

    # logo
    st.image("dashboard/logo.png")

    st.text("Silahkan masukkan range tanggal untuk filter dahsboard")

    # ambil start_date & end_date dr inputan
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# data yang diambil adalah data yang masuk ke dalam range min max
# Ubah filter menjadi seperti ini:
main_df1 = daily_data[(daily_data["dteday"] >= pd.to_datetime(start_date)) & 
                      (daily_data["dteday"] <= pd.to_datetime(end_date))]

mask = hourly_data["dteday"].between(
    pd.to_datetime(start_date),
    pd.to_datetime(end_date)
)
main_df2 = hourly_data[mask]

# used all helper function
daily_rent_df = create_daily_rent(main_df1)
byweek_rent_df = create_byweek(main_df1)
byseason_rent_df = create_byseason(main_df1)
byhour_rent_df = create_byhours(main_df2)

# =========================================== MAIN CONTENT ========================================================
st.header("W.D.C Bike Rent Dashboard :bike:")

## ================= Total Rent dan Revenue
st.subheader("Daily Rent")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_rent = daily_rent_df.bike_rent.sum()
    st.metric("Total Rents", value=total_rent)

with col2:
    casual_rent = daily_rent_df.casual_rent.sum()
    st.metric("Casual Rents", value=casual_rent)

with col3:
    member_rent = daily_rent_df.member_rent.sum()
    st.metric("Member Rents", value=member_rent)

with col4:
    total_revenue = daily_rent_df.revenue.sum()
    st.metric("Total Revenue ($)", value=total_revenue)

fig, ax = plt.subplots(figsize=(16,8))

ax.plot(
    daily_rent_df["dteday"],
    daily_rent_df["bike_rent"],
    marker='o', 
    linewidth=2,
    color="#4F4F4F"
)
ax.set_title("Bike Rent Revenue ($)", fontsize=40)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
    
st.pyplot(fig)

# # ===================== Perentalan berdasarkan Weekday/Weekend
st.subheader("Weekday/Weekend Rent")
st.text("Perentalan Sepeda berdasarkan Tipe Hari (Weekday atau Weekend)")

byweek_rent_df["day_type"] = byweek_rent_df["workingday"].map({
    1: "Weekday",
    0: "Weekend"
})

pie_df = byweek_rent_df.groupby("day_type", observed=True)["bike_rent"].sum()
fig, ax = plt.subplots(figsize=(18, 12))
colors = ["#4F4F4F", "#A19E9E"]

labels = [
    f"{label}\n({value:,})"
    for label, value in zip(pie_df.index, pie_df.values)
]

ax.pie(
    pie_df,
    labels=labels,
    autopct="%1.1f%%",
    startangle=90,
    colors=colors,
    textprops={"fontsize": 28}
)

ax.set_title("Proportion of Bike Rentals: Weekday vs Weekend", fontsize=40)
ax.axis("equal")

st.pyplot(fig)

# ======================== Perentalan berdasarkan Musim/Cuaca
st.subheader("Bike Rent by Seasons")
st.text("Perentalan Sepeda berdasarkan Musim")

byseason_rent_df["season_type"] = byseason_rent_df["season"].map({
    1: "Partly Cloudly",
    2: "Mist Cloudly",
    3: "Light",
    4: "Heavy Rain"
})

byseason_rent_df["season_type"] = pd.Categorical(
    byseason_rent_df["season_type"],
    categories=["Partly Cloudly", "Mist Cloudly", "Light", "Heavy Rain"],
    ordered=True
)

fig, ax = plt.subplots(figsize=(18, 8))
colors = ["#C8C7C7", "#807E7E", "#4F4F4F", "#A5A2A2"]

ax.barh(
    byseason_rent_df["season_type"],
    byseason_rent_df["bike_rent"],
    color=colors
)

ax.set_xlabel("Number of Rentals", fontsize=30)
ax.set_ylabel("Season", fontsize=30)
ax.set_title("Bike Rentals by Season Type", fontsize=50)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=30)

for container in ax.containers:
    ax.bar_label(container, fmt="%.0f", fontsize=28, padding=10)

st.pyplot(fig)

# =========================== Jam Perentalan Paling Ramai ke Sepi 
st.subheader("Bike Rent by Hours")
st.text("Perentalan Berdasarkan Jam (0-23)")

byhour_rent_df = byhour_rent_df.sort_values(by="hr") 

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 10)) 

ax.bar(
    byhour_rent_df["hr"],     
    byhour_rent_df["bike_rent"],
    color="#4F4F4F"
)

ax.set_xlabel("Hours (24-hour format)", fontsize=20)
ax.set_ylabel("Total Rentals", fontsize=20)
ax.set_title("Hourly Bike Rental Trend", fontsize=30)
ax.set_xticks(range(0, 24))
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=15)

for container in ax.containers:
    ax.bar_label(container, fmt="%.0f", fontsize=12, padding=3)

st.pyplot(fig)

st.caption('Copyright (c) W.D.C Rent 2025')