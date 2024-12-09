import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from babel.numbers import format_currency
sns.set(style='dark')

#st.set_page_config(layout="wide")
st.title ('Dashboard : Bicycle Rental Trends and User Insight :bike:')

def avg_rentals_per_hour (hour_df):
    """
    Mengitung rata-rata penyewaan sepeda per jam, musim dan cuaca
    
    parameter : hour_df : df yang berisi penyewaan dengan kolom season, weathersit, hr, dan cnt
    
    returns: df yg berisi rata2 penyewaan sepeda per jam, musim dan cuaca
    """
    avg_rentals = hour_df.groupby(['season','weathersit', 'hr'])['cnt'].mean().reset_index()
    avg_rentals.rename(columns={'cnt':'avg_rentals'},inplace =True)
    return avg_rentals

def create_heatmap_data(avg_rentals):
    """
    Membuat pivot table untuk heatmap berdasarkan rata-rata penyewaan per jam, musim, dan cuaca.

    Parameters:
    avg_rentals (DataFrame): DataFrame yang berisi rata-rata penyewaan per jam, musim, dan cuaca.

    Returns:
    DataFrame: Pivot table untuk heatmap.
    """
    heatmap_data = avg_rentals.pivot_table(
        index=['season','weathersit'],
        columns='hr',
        values='avg_rentals',
        aggfunc='mean'
    )
    return heatmap_data

def numerical_df(day_df):
    numerical_df = day_df.select_dtypes(include=['int64','float64'])
    correlation_matrix = numerical_df.corr()
    return correlation_matrix

# Mapping untuk `season` dan `weathersit`
season_mapping = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}

weathersit_mapping = {
    1: "Clear",
    2: "Cloudy",
    3: "Light Rain/Snow",
    4: "Heavy Rain/Snow"
}

#--------------------------------------------------------------------------
#membaca data dari csv
hour_df = pd.read_csv("data/cleaned/hour_df_cleaned.csv")
day_df = pd.read_csv("data/cleaned/day_df_cleaned.csv")
rfm_combined = pd.read_csv("data/cleaned/rfm_combined.csv")        

#menghitung rata-rata penyewaan per jam, musim dan cuaca
avg_rentals = avg_rentals_per_hour(hour_df)
#membuat data untuk heatmap
heatmap_data = create_heatmap_data(avg_rentals)
#buat label gabungan untuk sumbu Y
heatmap_data.index=heatmap_data.index.map(
    lambda x: f"{season_mapping[x[0]]} - {weathersit_mapping[x[1]]}"
)

#menghitung korlasi antar variabel
correlation_matrix = numerical_df(day_df)

#--------------------------------------------------------------------------
#col1, col2 = st.columns([2,2])

#heatmap
#col1.markdown("## Peak Bike Usage by Season and Weather")
st.subheader('Peak Bike Usage by Season and Weather')
#with col1:
fig,ax = plt.subplots(figsize=(16,7))
sns.heatmap(
    heatmap_data, 
    cmap="YlGnBu", 
    annot=True, 
    fmt='.1f', 
    cbar_kws={'label': 'Average Bike Rentals'}, 
    linewidths=0.5
    )
plt.xlabel("Hours")
plt.ylabel("Season and Weather")
plt.xticks(rotation=0)
plt.yticks(rotation=0)
st.pyplot(fig)

#scatterplot
st.subheader('Effects of Weather Conditions and Temperature on Bike Rental Trends')
fig,ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(
    x='temp', 
    y='cnt', 
    data=hour_df, 
    hue='weathersit_condition', 
    palette='coolwarm'
    )
plt.xlabel("Temperature (Normalized)")
plt.ylabel("Total of Bike Rentals")
plt.legend(title="Weather Condition", loc='upper left')
st.pyplot(fig)

# barplot
st.subheader('Analyzing User Behavior: Registered vs. Casual Bike Rentals on Weekdays and Holidays')
fig,ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x='day_type', 
    y='cnt', 
    hue='user_type', 
    data=day_df, 
    ci=None
    )
plt.ylabel('Average Bike Rentals')
plt.xlabel('Days Type')
plt.legend(title='Tipe Pengguna', loc='upper left')
st.pyplot(fig)

#heatmap korelasi variabel
st.subheader('Major Factors Impacting Bike Rental Usage')
fig,ax = plt.subplots(figsize=(16, 7))
sns.heatmap(
    correlation_matrix, 
    annot=True, 
    cmap='coolwarm', 
    vmin=-1, 
    vmax=1
    )
st.pyplot(fig)

#barplots
st.subheader('Behavioral Patterns of Bike Users (Casual vs. Registered) Based on Rental Time, Usage Intensity, and Total Contribution')
fig,ax = plt.subplots(figsize=(16, 7))
sns.countplot(
    data=rfm_combined, 
    x='user_segment', 
    hue='user_type'
    )
plt.xlabel('Segment')
plt.ylabel('Total')
st.pyplot(fig)