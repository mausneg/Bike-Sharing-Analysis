import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns

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

           
def main_content(df):
    st.header("Bike Sharing Dashboard")
    st.write("Select the tab to view the data")
        
    df_working_holiday = create_working_holiday(df)

    tab_1, tab_2, tab_3 = st.tabs(["Daily Count", "Hourly Count", "Working Holiday"])
    with tab_1:
        fig, ax = plt.subplots()
        sns.lineplot(data=df, x='dteday', y='registered_day', ax=ax, color='blue', label='Registered Users', markers='o')
        sns.lineplot(data=df, x='dteday', y='casual_day', ax=ax, color='orange', label='Casual Users', markers='o')
        ax.legend()
        ax.set_title('Daily Count')
        plt.xticks(df['dteday'][::int(len(df)/10)], rotation=45, size=8)
        plt.xlabel('Date')
        plt.ylabel('Count')
        plt.grid(alpha=0.3)
        st.pyplot(fig)
        st.dataframe(df)

    with tab_2:
        st.write("Select a date to view hourly details:")
        unique_dates = df['dteday'].dt.date.unique()
        selected_date = st.selectbox("Select Date", options=unique_dates)  
        filtered_data = df[df['dteday'].dt.date == selected_date]
        st.write(f"Hourly details for {selected_date}:")
        sns.lineplot(data=filtered_data, x='hr', y='registered_hour', ax=ax, color='blue', label='Registered Users', markers='o')
        sns.lineplot(data=filtered_data, x='hr', y='casual_hour', ax=ax, color='orange', label='Casual Users', markers='o')
        ax.set_title(f'Hourly Bike Rentals on {selected_date}')
        ax.set_xlabel('Hour')
        ax.set_ylabel('Count')
        plt.grid(alpha=0.3)
        plt.xticks(filtered_data['hr'], size=8)
        st.pyplot(fig)
        st.dataframe(filtered_data)

    with tab_3:
        st.write("Bike Rentals by Day Type")
        fig, ax = plt.subplots(figsize=(8, 5))
        bar_width = 0.35  # Lebar bar
        x = range(len(df_working_holiday['day_type']))
        ax.bar([p for p in x], df_working_holiday['casual_day'], width=bar_width, label='Casual Users', color='orange')
        ax.bar([p + bar_width for p in x], df_working_holiday['registered_day'], width=bar_width, label='Registered Users', color='green')
        ax.set_xlabel('Day Type', fontsize=12)
        ax.set_ylabel('Count', fontsize=12)
        ax.set_title('Bike Rentals by Day Type', fontsize=14)
        ax.set_xticks([p + bar_width / 2 for p in x])  # Posisikan label di tengah
        ax.set_xticklabels(df_working_holiday['day_type'])
        ax.legend()
        st.pyplot(fig)
        st.dataframe(df_working_holiday)




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
    df_all = pd.read_csv("dashboard/all.csv")
    df_all['dteday'] = pd.to_datetime(df_all['dteday'])
    start_dat, end_date = side_bar(df_all)
    df_main = date_filter(df_all, start_dat, end_date)
    main_content(df_main)

if __name__ == "__main__":
    main()