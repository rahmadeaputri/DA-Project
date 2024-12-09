import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from babel.numbers import format_currency
sns.set(style='dark')



def avg_rentals_per_hour (hour_df):
    avg_rentals = hour_df.groupby(['season','weathersit', 'hr'])['cnt'].mean().reset_index()
    avg_rentals.rename(columns={'cnt':'avg_rentals'},inplace =True)
    return avg_rentals
  
hour_df = pd.read_csv("data/cleaned/hour_df_cleaned.csv")
#day_df = pd.read_csv("day.csv")     

st.subheader('Peak Bike Usage by Season and Weather')


st.set_page_config(layout="wide")
st.title ('Dashboard : Bicycle Rental Trends and User Insight :bike:')

