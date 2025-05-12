import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import os

def create_working_holiday(df):
    df_working_holiday = df.groupby(['workingday_day', 'holiday_day']).agg({
        'cnt_day': 'sum',
        'casual_day': 'sum',
        'registered_day': 'sum'    
    }).reset_index()
    df_working_holiday['day_type'] = df_working_holiday.apply(
        lambda row: 'weekend' if row['workingday_day'] == 0 and row['holiday_day'] == 0 else 
                    'holiday' if row['holiday_day'] == 1 else 
                    'working', axis=1
    )
    df_working_holiday.drop(columns=['workingday_day', 'holiday_day'], inplace=True)
    return df_working_holiday

def create_weather(df):
    df_weather = df.groupby(['weathersit_hour']).agg({
    'cnt_hour': 'sum',
    'casual_hour': 'sum',
    'registered_hour': 'sum'    
    }).reset_index()
    df_weather['weather'] = df_weather.apply(
    lambda row: 'clear_cloudy' if row['weathersit_hour'] == 1 else 
                'mist_cloudy' if row['weathersit_hour'] == 2 else 
                'light_rain_snow' if row['weathersit_hour'] == 3 else 
                'heavy_rain_snow_fog', axis=1
    )
    df_weather.drop(columns=['weathersit_hour'], inplace=True)
    return df_weather
           
def main_content(df):
    st.header("Bike Sharing Dashboard")
    st.write("Select the tab to view the data")
    df_working_holiday = create_working_holiday(df)
    df_weather = create_weather(df)

    tab_1, tab_2, tab_3, tab_4, tab_5 = st.tabs(["Working Holiday", "Weather", "Correlation", "Daily Count", "Hourly Count"])

    with tab_1:
        st.write("Bike Rentals by Day Type")
        fig, ax = plt.subplots(figsize=(8, 5))
        bar_width = 0.35 
        x = range(len(df_working_holiday['day_type']))
        ax.bar([p for p in x], df_working_holiday['casual_day'], width=bar_width, label='Casual Users', color='orange')
        ax.bar([p + bar_width for p in x], df_working_holiday['registered_day'], width=bar_width, label='Registered Users', color='green')
        ax.set_xlabel('Day Type', fontsize=12)
        ax.set_ylabel('Count', fontsize=12)
        ax.set_title('Bike Rentals by Day Type', fontsize=14)
        ax.set_xticks([p + bar_width / 2 for p in x])
        ax.set_xticklabels(df_working_holiday['day_type'])
        st.pyplot(fig)
        st.dataframe(df_working_holiday)

    with tab_2:
        st.write("Bike Rentals by Weather")
        fig, ax = plt.subplots(figsize=(10, 6))
        bar_width = 0.35 
        x = range(len(df_weather['weather']))
        ax.bar([p for p in x], df_weather['casual_hour'], width=bar_width, label='Casual Users', color='orange')
        ax.bar([p + bar_width for p in x], df_weather['registered_hour'], width=bar_width, label='Registered Users', color='green')
        ax.set_xlabel('Weather', fontsize=12)
        ax.set_ylabel('Count', fontsize=12)
        ax.set_title('Bike Rentals by Weather', fontsize=14)
        ax.set_xticks([p + bar_width / 2 for p in x])
        ax.set_xticklabels(df_weather['weather'])
        ax.legend()
        st.pyplot(fig)
        st.dataframe(df_weather)

    with tab_3:
        st.write("Correlation Between Features")
        fig, axes = plt.subplots(3, 1, figsize=(6, 12))
        sns.scatterplot(x='atemp_original_day', y='cnt_day', data=df, color='blue', ax=axes[0])
        axes[0].set_title('Suhu vs Jumlah Peminjaman')
        axes[0].set_xlabel('Suhu')
        axes[0].set_ylabel('Jumlah Peminjaman')
        sns.scatterplot(x='hum_original_day', y='cnt_day', data=df, color='green', ax=axes[1])
        axes[1].set_title('Kelembapan vs Jumlah Peminjaman')
        axes[1].set_xlabel('Kelembapan')
        axes[1].set_ylabel('Jumlah Peminjaman')
        sns.scatterplot(x='windspeed_original_day', y='cnt_day', data=df, color='red', ax=axes[2])
        axes[2].set_title('Kecepatan Angin vs Jumlah Peminjaman')
        axes[2].set_xlabel('Kecepatan Angin')
        axes[2].set_ylabel('Jumlah Peminjaman')
        plt.tight_layout()
        st.pyplot(fig)

    with tab_4:
        st.write("Daily Count of Bike Rentals")
        fig, ax = plt.subplots(figsize=(18, 6))
        sns.lineplot(data=df, x='dteday', y='registered_day', ax=ax, color='blue', label='Registered Users', marker='o', markersize=3)
        sns.lineplot(data=df, x='dteday', y='casual_day', ax=ax, color='orange', label='Casual Users', marker='o', markersize=3)
        ax.legend()
        ax.set_title('Daily Count')
        plt.xticks(df['dteday'][::int(len(df)/10)], rotation=45, size=8)
        plt.xlabel('Date')
        plt.ylabel('Count')
        plt.grid(alpha=0.3)
        st.pyplot(fig)
        st.dataframe(df)

    with tab_5:
        st.write("Select a date to view hourly details:")
        unique_dates = df['dteday'].dt.date.unique()
        selected_date = st.selectbox("Select Date", options=unique_dates)
        filtered_data = df[df['dteday'].dt.date == selected_date]
        st.write(f"Hourly details for {selected_date}:")
        fig, ax = plt.subplots()
        sns.lineplot(data=filtered_data, x='hr', y='cnt_hour', ax=ax, color='blue', label='Jumlah Peminjaman  ', marker='o')
        ax.set_title(f'Hourly Bike Rentals on {selected_date}')
        ax.set_xlabel('Hour')
        ax.set_ylabel('Count')
        ax.set_xticks(filtered_data['hr'])
        ax.set_xticklabels(filtered_data['hr'], size=8)
        ax.legend()
        plt.grid(alpha=0.3)
        st.pyplot(fig)
        st.dataframe(filtered_data)




def date_filter(df, start_date, end_date):
    return df[(str(start_date) <= df['dteday']) & (df['dteday'] <= str(end_date))]

def side_bar(df):
    min_date = df['dteday'].min()
    max_date = df['dteday'].max()
    
    with st.sidebar:
        st.title("Filter Data")
        st.write("Select the date range:")
        start_date, end_date = st.date_input(
            label='Range Time',min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
            )
        
        return start_date, end_date

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "all.csv")
    df_all = pd.read_csv(file_path)
    df_all['dteday'] = pd.to_datetime(df_all['dteday'])
    start_dat, end_date = side_bar(df_all)
    df_main = date_filter(df_all, start_dat, end_date)
    main_content(df_main)

if __name__ == "__main__":
    main()