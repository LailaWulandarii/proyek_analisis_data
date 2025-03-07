import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Pengaturan halaman, judul, icon
st.set_page_config(
    page_title="Dashboard Analisis",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded",
)
st.title("📊 Dashboard Kualitas Udara")

#Load data dari file csv
def load_data():
    return pd.read_csv("cleaned_data.csv") 

airQuality_df = load_data()

#Sidebar navigasi
st.sidebar.title("Pilih Analisis:")
menu = st.sidebar.selectbox("", ["Tren Bulanan", "Tren Tahunan", "Korelasi Suhu dengan Polusi"])

#Menu yang akan muncul untuk tren bulanan
if menu == "Tren Bulanan":
    st.subheader("📈 Tren Rata-rata PM2.5 dan PM10 Bulanan")

    #Pilih bulan (default: semua bulan)
    bulan_options = ['Semua Bulan', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    selected_bulan = st.multiselect("Pilih Bulan 📅", bulan_options, default="Semua Bulan")

    #Filter data berdasarkan pilihan
    monthly_trend = airQuality_df.groupby('month')[['PM2.5', 'PM10']].mean()
    if "Semua Bulan" not in selected_bulan:
        bulan_dict = {name: i+1 for i, name in enumerate(bulan_options[1:])}
        selected_months = [bulan_dict[b] for b in selected_bulan]
        monthly_trend = monthly_trend.loc[monthly_trend.index.isin(selected_months)]

    #Plot data
    fig, ax = plt.subplots(figsize=(10, 5))
    monthly_trend.plot(kind='line', marker='o', ax=ax)
    plt.xlabel("Bulan")
    plt.ylabel("Rata-rata Nilai PM")
    plt.xticks(ticks=range(1, 13), labels=bulan_options[1:])
    plt.legend(["PM2.5", "PM10"])
    plt.grid(alpha=0.5)
    st.pyplot(fig)
    
#Menu yang akan muncul untuk tren tahunan
elif menu == "Tren Tahunan":
    st.subheader("📉 Tren Rata-rata PM2.5 dan PM10 Tahunan")

    #Pilih tahun (default: semua tahun)
    tahun_options = ["Semua Tahun"] + sorted(airQuality_df['year'].unique().tolist())
    selected_tahun = st.multiselect("Pilih Tahun 📆", tahun_options, default="Semua Tahun")

    #Filter data berdasarkan pilihan tahun
    yearly_trend = airQuality_df.groupby('year')[['PM2.5', 'PM10']].mean()
    if "Semua Tahun" not in selected_tahun:
        selected_years = [t for t in selected_tahun if t != "Semua Tahun"]
        yearly_trend = yearly_trend.loc[yearly_trend.index.isin(selected_years)]

    #Plot data tahunan
    fig, ax = plt.subplots(figsize=(8, 4))
    yearly_trend.plot(kind='line', marker='o', ax=ax)
    
    plt.xlabel("Tahun")
    plt.ylabel("Rata-rata Nilai PM")
    plt.xticks(ticks=yearly_trend.index, labels=yearly_trend.index.astype(str))
    plt.legend(["PM2.5", "PM10"])
    plt.grid(alpha=0.5)
    st.pyplot(fig)

#Menu yang akan muncul untuk korelasi suhu dengan polusi
elif menu == "Korelasi Suhu dengan Polusi":
    st.subheader("🌡️ Hubungan Suhu dengan Polusi (PM2.5 dan PM10)")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Suhu vs PM2.5")
        fig, ax = plt.subplots()
        sns.scatterplot(data=airQuality_df, x='TEMP', y='PM2.5', alpha=0.6, ax=ax)
        sns.regplot(data=airQuality_df, x='TEMP', y='PM2.5', scatter_kws={'alpha':0.6}, line_kws={'color':'red'}, ax=ax)
        plt.xlabel("Suhu (°C)")
        plt.ylabel("PM2.5")
        st.pyplot(fig)
    
    with col2:
        st.write("### Suhu vs PM10")
        fig, ax = plt.subplots()
        sns.scatterplot(data=airQuality_df, x='TEMP', y='PM10', alpha=0.6, ax=ax)
        sns.regplot(data=airQuality_df, x='TEMP', y='PM10', scatter_kws={'alpha':0.6}, line_kws={'color':'red'}, ax=ax)
        plt.xlabel("Suhu (°C)")
        plt.ylabel("PM10")
        st.pyplot(fig)
    
    correlation_pm25 = airQuality_df['TEMP'].corr(airQuality_df['PM2.5'])
    correlation_pm10 = airQuality_df['TEMP'].corr(airQuality_df['PM10'])
    
    st.info(f"📌 Korelasi suhu dan PM2.5: {correlation_pm25:.2f}")
    st.info(f"📌 Korelasi suhu dan PM10: {correlation_pm10:.2f}")
    st.warning("⚠️ Tidak ada korelasi yang signifikan antara suhu dan polusi.")