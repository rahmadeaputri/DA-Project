import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from babel.numbers import format_currency
sns.set(style='white')

# Judul aplikasi
st.title('Bicycle Rental Trends and User Insight :bike:')

# Function untuk menghitung rata-rata penyewaan per jam, musim, dan cuaca
def avg_rentals_per_hour(hour_df):
    avg_rentals = hour_df.groupby(['season', 'weathersit', 'hr'])['cnt'].mean().reset_index()
    avg_rentals.rename(columns={'cnt': 'avg_rentals'}, inplace=True)
    return avg_rentals

# Function untuk membuat pivot table data heatmap
def create_heatmap_data(avg_rentals):
    heatmap_data = avg_rentals.pivot_table(
        index=['season', 'weathersit'],
        columns='hr',
        values='avg_rentals',
        aggfunc='mean'
    )
    return heatmap_data

# Function untuk filtering data berdasarkan user segment
def filter_user_segment(rfm_combined, selected_segment):
    if selected_segment == "All":
        return rfm_combined
    else:
        return rfm_combined[rfm_combined['user_segment'] == selected_segment]

# Function untuk plotting barplot segmentasi user
def plot_user_segment(filtered_rfm_combined, selected_segment):
    st.markdown(f"#### Behavioral Patterns for Segment: {selected_segment}")
    fig, ax = plt.subplots(figsize=(16, 7))
    sns.countplot(
        data=filtered_rfm_combined,
        x='user_segment',
        hue='user_type'
    )
    plt.xlabel('Segment')
    plt.ylabel('Total')
    st.pyplot(fig)

# Function untuk membuat heatmap korelasi
def plot_correlation_heatmap(day_df, columns_to_include):
    correlation_matrix = day_df[columns_to_include].corr()
    fig, ax = plt.subplots(figsize=(16, 7))
    sns.heatmap(
        correlation_matrix,
        annot=True,
        cmap='coolwarm',
        vmin=-1,
        vmax=1
    )
    plt.title("Correlation Heatmap")
    st.pyplot(fig)

# Mapping untuk `season` dan `weathersit`
season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
weathersit_mapping = {1: "Clear", 2: "Cloudy", 3: "Light Rain/Snow", 4: "Heavy Rain/Snow"}

# Membaca data dari CSV
hour_df = pd.read_csv("data/cleaned/hour_df_cleaned.csv")
day_df = pd.read_csv("data/cleaned/day_df_cleaned.csv")
rfm_combined = pd.read_csv("data/cleaned/rfm_combined.csv")

# Sidebar Filter
with st.sidebar:
    st.sidebar.title("Filter For Each Dashboard")
    selected_season = st.selectbox("Season:", ["All"] + list(season_mapping.values()))
    selected_weather = st.selectbox("Weather:", ["All"] + list(weathersit_mapping.values()))
    temp_min, temp_max = st.slider("Range of Temperature (Normalized):",
                                   float(hour_df['temp'].min()),
                                   float(hour_df['temp'].max()),
                                   (float(hour_df['temp'].min()), float(hour_df['temp'].max())))
    day_type_options = st.multiselect("Choose Day Type (Weekday, Weekend, Holiday)",
                                      day_df['day_type'].unique(),
                                      default=day_df['day_type'].unique())
    columns_to_include = st.multiselect("Select Columns for Correlation Heatmap",
                                       day_df.select_dtypes(include=['int64', 'float64']).columns,
                                       default=day_df.select_dtypes(include=['int64', 'float64']).columns)
    selected_user_segment = st.selectbox("Segment", ["All"] + list(rfm_combined['user_segment'].unique()))

# Menghitung rata-rata penyewaan
avg_rentals = avg_rentals_per_hour(hour_df)
filtered_data = avg_rentals.copy()

# Filter berdasarkan season
if selected_season != "All":
    selected_season_code = {v: k for k, v in season_mapping.items()}[selected_season]
    filtered_data = filtered_data[filtered_data['season'] == selected_season_code]

# Filter berdasarkan weather
if selected_weather != "All":
    selected_weather_code = {v: k for k, v in weathersit_mapping.items()}[selected_weather]
    filtered_data = filtered_data[filtered_data['weathersit'] == selected_weather_code]

# Heatmap Data
heatmap_data_filtered = create_heatmap_data(filtered_data)
heatmap_data_All = create_heatmap_data(avg_rentals)

heatmap_data_All.index = heatmap_data_All.index.map(lambda x: f"{season_mapping[x[0]]} - {weathersit_mapping[x[1]]}")
heatmap_data_filtered.index = heatmap_data_filtered.index.map(lambda x: f"{season_mapping[x[0]]} - {weathersit_mapping[x[1]]}")

# Plot Heatmap
st.markdown(f'##### Peak Bike Usage {selected_season} Season During {selected_weather} Weather')
fig, ax = plt.subplots(figsize=(18, 7))
sns.heatmap(heatmap_data_All, cmap="YlGnBu", annot=False, cbar=False, alpha=0.3, ax=ax, vmin=0, vmax=670)
sns.heatmap(heatmap_data_filtered, cmap="YlGnBu", annot=True, fmt='.1f', cbar_kws={'label': 'Average Bike Rentals'}, linewidths=0.5, ax=ax, vmin=0, vmax=670)
st.pyplot(fig)

# Scatterplot Temperature
filtered_hour_df = hour_df[(hour_df['temp'] >= temp_min) & (hour_df['temp'] <= temp_max)]
st.markdown(f"##### Bike Rentals for Temperature Range {temp_min:.2f} - {temp_max:.2f}")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x='temp', y='cnt', data=filtered_hour_df, hue='weathersit', palette='coolwarm')
plt.xlabel("Temperature (Normalized)")
plt.ylabel("Total of Bike Rentals")
plt.legend(title="Weather Condition", loc='upper left')
st.pyplot(fig)

# Barplot User Behavior
filtered_day_df = day_df[day_df['day_type'].isin(day_type_options)]
st.markdown("##### Analyzing User Behavior: Registered vs. Casual Bike Rentals on Weekdays and Holidays")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='day_type', y='cnt', hue='user_type', data=filtered_day_df, ci=None)
plt.ylabel('Average Bike Rentals')
plt.xlabel('')
plt.legend(title='User', loc='upper left')
st.pyplot(fig)

# Heatmap Korelasi
st.markdown('##### Major Factors Impacting Bike Rental Usage')
plot_correlation_heatmap(day_df, columns_to_include)

# Barplot Segmentasi User
filtered_rfm_combined = filter_user_segment(rfm_combined, selected_user_segment)
plot_user_segment(filtered_rfm_combined, selected_user_segment)
