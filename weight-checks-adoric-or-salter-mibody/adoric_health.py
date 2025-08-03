import os
import read_my_file as rmf

import pandas as pd
import streamlit as st
import plotly.express as px
# import statsmodels.api as sm
import random

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

st.write(os.environ['HOSTNAME'])

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
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

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
number_of_recent_readings = 83
fig_01_df = pivoted_df.iloc[:number_of_recent_readings].copy()

fig_01_df['Weight'] = fig_01_df['Weight'].astype(float)
# st.write('check weight only')
# st.dataframe(fig_01_df)

st.dataframe(fig_01_df[['Weight', 'BMI']])

max_weight = fig_01_df['Weight'].max()
min_weight = fig_01_df['Weight'].min()
# st.write(f'Max weight: {max_weight}, min weight: {min_weight}.')
fig_01 = px.scatter(
    fig_01_df,
    y='Weight',
    # size='Bone Mass',
    trendline='rolling',
    trendline_options=dict(function="mean", window=7),
    trendline_color_override="red",
    range_y=(min_weight-1, max_weight+1),
    hover_data='Weight',
    )
fig_01.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#dfdfdf')
fig_01.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#dfdfdf')

st.write()
st.write()
st.write('Weight readings and a weekly trendline')
st.plotly_chart(fig_01)

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
    weight_weekly_average_df.resample('W-Sun').mean().round(1)
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
# st.write('weight_weekly_average_df:')
# st.dataframe(weight_weekly_average_df)

# # weight_weekly_average_df['date_time'] =
# weight_weekly_average_df['date_time']

st.dataframe(weight_weekly_average_df)

df = pd.DataFrame(
    {
        "Command": ["**st.table**", "*st.dataframe*"],
        "Type": ["`static`", "`interactive`"],
        "Docs": [
            "[:rainbow[docs]]\
(https://docs.streamlit.io/develop/api-reference/data/st.dataframe)",
            "[:book:]\
(https://docs.streamlit.io/develop/api-reference/data/st.table)",
        ],
    }
)
st.table(df)

df = pd.DataFrame(
    {
        "name": ["Roadmap", "Extras", "Issues"],
        "url": [
            "https://roadmap.streamlit.app",
            "https://extras.streamlit.app",
            "https://issues.streamlit.app"
            ],
        "stars": [random.randint(0, 1000) for _ in range(3)],
        "views_history": [
            [random.randint(0, 5000) for _ in range(30)] for _ in range(3)
            ],
    }
)

st.dataframe(
    df,
    column_config={
        "name": "App name",
        "stars": st.column_config.NumberColumn(
            "Github Stars",
            help="Number of stars on GitHub",
            format="%d ⭐",
        ),
        "url": st.column_config.LinkColumn("App URL"),
        "views_history": st.column_config.LineChartColumn(
            "Views (past 30 days)", y_min=0, y_max=5000
        ),
    },
    hide_index=True,
)

st.image(
    '''https://media.istockphoto.com/id/825383494/photo/
business-man-pushing-large-stone-up-to-hill-business-heavy-tasks-and-problems-concept.jpg
?s=612x612&w=0&k=20&c=wtqvbQ6OIHitRVDPTtoT_1HKUAOgyqa7YzzTMXqGRaQ=''',
    caption='Syzyf', use_container_width=True
    )

options = ["North", "East", "South", "West"]
selection = st.pills("Directions", options, selection_mode="single")
st.markdown(f"Your selected options: {selection}.")

options = ["North", "East", "South", "West"]
selection = st.pills("Directions", options, selection_mode="multi")
st.markdown(f"Your selected options: {selection}.")
my_list = weight_weekly_average_df.index.to_list()

options = st.multiselect(
    "What are your favorite colors?",
    my_list,
    default=[my_list[0], my_list[-1]],
    max_selections=2
)
options = sorted(options)
st.write("You selected:", options)
st.write("You selected:", sorted(options))

if len(options) > 0:
    st.dataframe(weight_weekly_average_df.loc[options[-1]:options[0]])
else:
    st.write('No range selected so the last entry is displayed:')
    st.dataframe(weight_weekly_average_df.iloc[:1])

st.write("""
**INDUSTRY**
Software Application
""")
# There are 2 spaces after **INDUSTRY**
# Or use the break with unsafe_allow_html=True.
link = "https://media.istockphoto.com/id/825383494/photo/\
business-man-pushing-large-stone-up-to-hill-business-heavy\
-tasks-and-problems-concept.jpg?s=612x612&w=0&k=20&c=\
wtqvbQ6OIHitRVDPTtoT_1HKUAOgyqa7YzzTMXqGRaQ="
st.write(f"""
### Syzyf
<p><img src="{link}" alt="Syzyfincio"></p>
<p href="{link}">Tralala</p>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
rows_slice = int(len(fig_01_df)/3)
container_h = (3+(1+rows_slice)*35)
with col1:
    st.header("Part I")
    st.dataframe(fig_01_df[['Weight', 'BMI']].iloc[:rows_slice],
                 height=container_h)
with col2:
    st.header("Part II")
    st.dataframe(fig_01_df[['Weight', 'BMI']].iloc[rows_slice:2*rows_slice],
                 height=container_h)
with col3:
    st.header("Part III")
    st.dataframe(fig_01_df[['Weight', 'BMI']].iloc[2*rows_slice:],
                 height=container_h)
