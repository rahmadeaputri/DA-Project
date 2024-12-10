import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from babel.numbers import format_currency
sns.set(style='dark')


st.title ('Bicycle Rental Trends and User Insight :bike:')

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
    3: "FAll",
    4: "Winter"
}

weathersit_mapping = {
    1: "Clear",
    2: "Cloudy",
    3: "Light Rain/Snow",
    4: "Heavy Rain/Snow"
}
#---------------------------------------------------------------------
#membaca data dari csv
hour_df = pd.read_csv("data/cleaned/hour_df_cleaned.csv")
day_df = pd.read_csv("data/cleaned/day_df_cleaned.csv")
rfm_combined = pd.read_csv("data/cleaned/rfm_combined.csv")        


#menghitung rata-rata penyewaan per jam, musim dan cuaca
avg_rentals = avg_rentals_per_hour(hour_df)
#membuat data untuk heatmap
#heatmap_data = create_heatmap_data(avg_rentals)

#Sidebar
with st.sidebar:
    st.sidebar.title("Filter For Each Dasboard")
    
    selected_season = st.selectbox(
    "Season:",
    ["All"] + list(season_mapping.values())  # Tambahkan "All" ke list pilihan
    )

    selected_weather = st.selectbox(
    "Weather",
    ["All"] + list(weathersit_mapping.values())  # Tambahkan "All" ke list pilihan
    )
    
    temp_min, temp_max = st.slider(
    "Range of Temperature (Normalized):",
    float(hour_df['temp'].min()),
    float(hour_df['temp'].max()),
    (float(hour_df['temp'].min()), float(hour_df['temp'].max()))
    )

    day_type_options = st.multiselect(
    "Choose Day Type (Weekday, Weekend, Holiday)", 
    day_df['day_type'].unique(), 
    default=day_df['day_type'].unique()
    )

    columns_to_include = st.multiselect(
    "Select Columns for Correlation Heatmap",
    day_df.select_dtypes(include=['int64', 'float64']).columns,
    default=day_df.select_dtypes(include=['int64', 'float64']).columns
    )
    
    selected_user_segment = st.selectbox(
    "Segment", 
    ["All"] + list(rfm_combined['user_segment'].unique())  # Tambahkan "Semua"
    )
    
#st.subheader(':sparkles: Peak Bike Usage by Season and Weather')  
# Filter berdasarkan season
if selected_season == "All":
    filtered_data = avg_rentals.copy()  # Jika "All", gunakan All data
else:
    # Cari kode season berdasarkan nama season yang dipilih
    selected_season_code = {v: k for k, v in season_mapping.items()}[selected_season]
    filtered_data = avg_rentals[avg_rentals['season'] == selected_season_code]

# Filter berdasarkan weather
if selected_weather == "All":
    filtered_data = filtered_data  # Tidak perlu filter tambahan
else:
    # Cari kode weather berdasarkan nama weather yang dipilih
    selected_weather_code = {v: k for k, v in weathersit_mapping.items()}[selected_weather]
    filtered_data = filtered_data[filtered_data['weathersit'] == selected_weather_code]

# Pivot table untuk data terfilter (lapisan atas - warna penuh)
heatmap_data_filtered = create_heatmap_data(filtered_data)
# Pivot table untuk seluruh data (lapisan utama - pudar)
heatmap_data_All = create_heatmap_data(avg_rentals)

#st.write("Heatmap Data All", heatmap_data_All)
#st.write("Heatmap Data Filtered", heatmap_data_filtered)

#buat label gabungan untuk sumbu Y
heatmap_data_All.index = heatmap_data_All.index.map(
    lambda x: f"{season_mapping[x[0]]} - {weathersit_mapping[x[1]]}"
)
heatmap_data_filtered.index = heatmap_data_filtered.index.map(
    lambda x: f"{season_mapping[x[0]]} - {weathersit_mapping[x[1]]}"
)

#heatmap
st.markdown(f'##### Peak Bike Usage {selected_season} Season During {selected_weather} Weather')
fig,ax = plt.subplots(figsize=(18,7))
# Heatmap utama (seluruh data dengan transparansi rendah)
sns.heatmap(
    heatmap_data_All,
    cmap="YlGnBu",
    annot=False,
    cbar=False,
    alpha=0.3,  # Transparansi rendah
    ax=ax,
    vmin=0,
    vmax=670
)
# Heatmap overlay (data terfilter dengan warna penuh)
sns.heatmap(
    heatmap_data_filtered, 
    cmap="YlGnBu",
    annot=True,  
    fmt='.1f', 
    cbar_kws={'label': 'Average Bike Rentals'}, 
    linewidths=0.5,
    ax=ax,
    vmin=0,
    vmax=670
    )
plt.xlabel("Hours")
plt.ylabel("Season and Weather")
#plt.xticks(rotation=0)
#plt.yticks(rotation=0)
st.pyplot(fig)


#-------------------------------------------------------------
#scatterplot
#st.subheader(":sparkles: Effects of Weather Conditions and Temperature on Bike Rental Trends")
filtered_hour_df = hour_df[(hour_df['temp'] >= temp_min) & (hour_df['temp'] <= temp_max)]
st.markdown(f"##### Bike Rentals for Temperature Range {temp_min:.2f} - {temp_max:.2f}")
fig,ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(
    x='temp', 
    y='cnt', 
    data=filtered_hour_df, 
    hue='weathersit_condition', 
    palette='coolwarm'
    )
plt.xlabel("Temperature (Normalized)")
plt.ylabel("Total of Bike Rentals")
plt.legend(title="Weather Condition", loc='upper left')
st.pyplot(fig)

#-------------------------------------------------------------

# barplot
#st.subheader(':sparkles: Analyzing User Behavior: Registered vs. Casual Bike Rentals on Weekdays and Holidays')
st.markdown("##### Analyzing User Behavior: Registered vs. Casual Bike Rentals on Weekdays and Holidays")
filtered_day_df = day_df[day_df['day_type'].isin(day_type_options)]
fig,ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x='day_type', 
    y='cnt', 
    hue='user_type', 
    data=filtered_day_df, 
    ci=None
    )
plt.ylabel('Average Bike Rentals')
plt.xlabel('')
plt.legend(title='User', loc='upper left')
st.pyplot(fig)

#-------------------------------------------------------------
st.markdown('##### Major Factors Impacting Bike Rental Usage')
#heatmap korelasi variabel
correlation_matrix_filtered = day_df[columns_to_include].corr()
fig,ax = plt.subplots(figsize=(16, 7))
sns.heatmap(
    correlation_matrix_filtered, 
    annot=True, 
    cmap='coolwarm', 
    vmin=-1, 
    vmax=1
    )
st.pyplot(fig)


#barplots
#st.markdown('##### Behavioral Patterns of Bike Users (Casual vs. Registered) Based on Rental Time, Usage Intensity, and Total Contribution')
if selected_user_segment == "All":
    filtered_rfm_combined = rfm_combined  # Jika "Semua", gunakan semua data
else:
    filtered_rfm_combined = rfm_combined[rfm_combined['user_segment'] == selected_user_segment]
    
st.markdown(f"#### Behavioral Patterns for Segment: {selected_user_segment}")
fig,ax = plt.subplots(figsize=(16, 7))
sns.countplot(
    data=filtered_rfm_combined, 
    x='user_segment', 
    hue='user_type'
    )
plt.xlabel('Segment')
plt.ylabel('Total')
st.pyplot(fig)