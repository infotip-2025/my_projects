import os
import read_my_file as rmf

import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime
# import statsmodels.api as sm
import random

import pokemon as pok

# setup the directory path
# drive = 'u:'
# path_a = 'OneDrive'
# path_b = 'DRIVE_GOOGLE'
# path_c = 'Adoric health'
# full_path = os.path.join(drive, '/', path_a, path_b, path_c)
# full_path = './Data'
# full_path = 
# '/mount/src/my_projects/weight-checks-adoric-or-salter-mibody/Data'
# full_path = '/mount/src/my_projects/weight-checks-adoric-or-salter-mibody/Data'

# ! bardzo przydatna linia!!!
# ! st.write(os.environ.items())
# ! ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑

# st.write('Jeb sie chuju!')

page_layout = st.sidebar.radio(
     "Page layout:", options=['centered', 'wide']
 )
st.set_page_config(layout=page_layout)

os_environ_hostname = os.environ.get('HOSTNAME', 'unknown-host')   # os.environ['HOSTNAME']

st.write('\'HOSTNAME\' if known: ', os_environ_hostname)

if os.environ.get('HOSTNAME') == 'streamlit':
    full_path = \
        os.getcwd() + '/weight-checks-adoric-or-salter-mibody/Data'
else:
    drive = 'u:'
    path_a = 'OneDrive'
    path_b = 'DRIVE_GOOGLE'
    path_c = 'Adoric health'
    full_path = os.path.join(drive, '/', path_a, path_b, path_c)

## '''
## pick current dir - not needed for this purpose
## and change working dir to the required one
## current_dir = os.getcwd()
### os.chdir(full_path)
## xxxxxx_st.write(os.getcwd)
## print(full_path)
## '''

data_line_by_line, \
    numer_of_files, \
    data_line_by_line_user_names_only \
    = rmf.read_files_to_list(full_path)

# os.chdir(current_dir)

# setup streamlite page
# ! st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# rmf.print_data(data_line_by_line)
# print('Number of processed files:', numer_of_files)

df = pd.DataFrame(data_line_by_line)
df.columns = [
    'day_name',
    'date',
    'time',
    'attribute',
    'value',
    'info_symbol',
    'info_txt'
    ]
df['date_time'] = pd.to_datetime(
    df['date']+df['time'],
    format='%m/ %d/%Y%H:%M'
    )  # or format='mixed'
# print(df.head(50))

pivoted_df = df.pivot(index='date_time', columns='attribute', values='value')
pivoted_df.drop(columns='BMR', inplace=True)
pivoted_df.sort_index(ascending=False, inplace=True)
# print(pivoted_df.head(50))

# start_date = '2020-01-01'
# end_date = '2025-08-02'
# # Create the full datetime index
# full_index = pd.date_range(start=start_date, end=end_date, freq='h')

# pivoted_df = pivoted_df.reindex(full_index)
# pivoted_df.sort_index(inplace=True)

# ! st.dataframe(pivoted_df)
# ! st.write(pivoted_df.isnull().sum())

# fig_01_start_date =

# number_of_recent_readings = 1093

# ???????????????????????????????????????????????????????
# ???????????? local only - weight ??????????????????????
# ???????????????????????????????????????????????????????
date_when_diagnosed_with_diabetics_type_2 = '2025-05-12'
days_since_20250512 = (pd.Timestamp.today() - pd.to_datetime(date_when_diagnosed_with_diabetics_type_2)).days
if os.environ.get('HOSTNAME') != 'streamlit':
    try:
        number_of_recent_readings = \
            int(
                st.text_input(
                    'Provide integer number of recent records to dislplay' +
                    '(default value calculated to start on 2025-05-12).',
                    days_since_20250512
                    )
            )
    except ValueError:
        st.warning('Not an integer provided! Default value used: 83.')
        number_of_recent_readings = 83

    the_first_valid_entry = st.date_input("Remove entries before (there are a few entries from Mar 2020 and then readings start in Oct 2022): ", datetime(2022, 1, 1))

    fig_01_df = pivoted_df.iloc[:number_of_recent_readings].copy()
    fig_01_df = fig_01_df[fig_01_df.index >= str(the_first_valid_entry)]
    # st.dataframe(fig_01_df.index)
    fig_01_df['Weight'] = fig_01_df['Weight'].astype(float)
    # st.write('check weight only')
    # st.dataframe(fig_01_df)

    st.warning(f'All readings for {days_since_20250512} days')    
    st.dataframe(fig_01_df[['Weight', 'BMI']])

    start_date = fig_01_df.index[0].date()
    max_weight = fig_01_df['Weight'].max()
    min_weight = fig_01_df['Weight'].min()
    trendline_window = '28D'
    # st.write(f'Max weight: {max_weight}, min weight: {min_weight}.')
    fig_01 = px.scatter(
        fig_01_df,
        y='Weight',
        # size='Bone Mass',
        trendline='rolling',
        trendline_options=dict(function="mean", window=trendline_window),
        trendline_color_override="red",
        range_y=(min_weight-1, max_weight+1),
        hover_data='Weight',
        )
    fig_01.update_xaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='#dfdfdf', 
        tick0=(pd.Timestamp.today().date() - pd.Timedelta(number_of_recent_readings, 'D')),
        dtick=7*24*60*60*1000,
        tickangle=90,
    )
    fig_01.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#dfdfdf', dtick=1)

    week_day_today = datetime.today().strftime('%A')[:3]

    st.warning(f'Weight readings and a \'{trendline_window}\' trendline')
    st.plotly_chart(fig_01)


    st.warning('What is our preferred average calculations range?')
    frequency_for_agg = st.radio(
        f"Select mothly, weekly (week end Sun), weekly (week end Fri), (week end today: {week_day_today})",
        [f"W-{week_day_today}", "ME", "W-Sun", "W-Fri"],
        captions=[
            f"Weekly {week_day_today} (today)",
            "Monthly",
            "Weekly Sun",
            "Weekly Fri",
        ],
        horizontal=True,
    )

    # df.resample('ME').mean()
    weight_weekly_average_df = fig_01_df.drop(
        columns=['Bone Mass',
                'Muscle Mass',
                'Body fat',
                'Visceral fat',
                'Body water']
        ).copy()
    weight_weekly_average_df['BMI'] = \
        weight_weekly_average_df['BMI'].astype(float)
    weight_weekly_average_df['Weight'] = \
        weight_weekly_average_df['Weight'].astype(float)

    weight_weekly_average_df = \
        weight_weekly_average_df.resample(frequency_for_agg).mean().round(1)
    weight_weekly_average_df.sort_index(ascending=False, inplace=True)
    weight_weekly_average_df['weight_change'] = \
        weight_weekly_average_df['Weight'] \
        - weight_weekly_average_df['Weight'].shift(-1)
    weight_weekly_average_df.reset_index(inplace=True)
    weight_weekly_average_df['date_time'] = \
        pd.to_datetime(weight_weekly_average_df['date_time']).dt.date
    weight_weekly_average_df.set_index('date_time', inplace=True)
    weight_weekly_average_df.rename(
        columns={'BMI': 'average_bmi', 'Weight': 'average_weight'},
        inplace=True
        )

    st.dataframe(weight_weekly_average_df)

# ???????????????????????????????????????????????????????
# ???????????? local only - weight ??????????????????????
# ???????????????????????????????????????????????????????

st.write(os.getcwd())
