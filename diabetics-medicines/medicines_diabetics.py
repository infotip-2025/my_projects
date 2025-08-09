import pandas as pd
import re
import time
import streamlit as st


def MustBeGreaterThanZero(x):
    if x <= 0:
        return ''
    else:
        try: 
            return int(x)
        except ValueError:
            return x


def select_tablets(required_dose, stock):
    # sorts stock dictionary by doses from lowest to highest
    stock = dict(sorted(stock.items()))

    # checks total available dosage
    available = sum([x*y for x, y in stock.items()])
    # ---- print(f'Available: {available}, required: {required_dose}')

    # create dictonary for our tablets composition,
    # with keys from stock and levels zeroed
    doses_composition = {x: 0 for x in stock.keys()}
    composed_dose_total = 0

    # returns the same stock levels and '0' if not emough left
    if available < required_dose:
        return (doses_composition, stock, 0)
    else:  # sufficient dosage in stock

        # takes doses from dictionary
        tablets_doses = list(stock.keys())
        # takes quantities of particular doses from dictionary
        # tablets_quantities = list(stock.values())
        
        # ---- print(dict(zip(tablets_doses, tablets_quantities)))
        
        dose_to_add_index = 0
        dose_to_remove_index = 0
        
        while required_dose != composed_dose_total:
            # find the first/lowest available dose
            # ---- print(f'''dose_to_add_index {dose_to_add_index},
# ---- dose_to_remove_index {dose_to_remove_index},
# ---- tablets_doses[dose_to_add_index] {tablets_doses[dose_to_add_index]},
# ---- stock[tablets_doses[dose_to_add_index]] {stock[tablets_doses[dose_to_add_index]]}''')

            while stock[tablets_doses[dose_to_add_index]] == 0:
                dose_to_add_index += 1
            # add a tablet to my composition and remove it from stock
            doses_composition[tablets_doses[dose_to_add_index]] += 1
            stock[tablets_doses[dose_to_add_index]] -= 1
            # count the composed dose
            composed_dose_total = \
                sum([x*y for x, y in doses_composition.items()])
            # if composed dose is over required dose
            # remove a piece of a lowest dose available
            # ---- print(f'required_dose {required_dose}, composed_dose_total {composed_dose_total}')
            while required_dose < composed_dose_total:
                # ---- print('!!! required_dose < composed_dose_total !!!')
                # find the first lowest dose available in composed tablet set
                while doses_composition[
                    tablets_doses[dose_to_remove_index]
                        ] == 0:
                    dose_to_remove_index += 1
                # add a tablet back to stock and remove it from my composition
                doses_composition[tablets_doses[dose_to_remove_index]] -= 1
                stock[tablets_doses[dose_to_remove_index]] += 1
                # recalculate composed dose
                composed_dose_total = \
                    sum([x*y for x, y in doses_composition.items()])
                # ---- print(f'Had to remove a tablet - recalculated composed_dose_total: {composed_dose_total}')

        return (doses_composition, stock, 1)


@st.cache_data
def load_df_from_google_sheets(from_file):

    file = 't:/_DOWNLOAD_/ROGcio/' + \
        'Chlanie browara i reszta statystyk Sprinkwell.xlsx'

    full_google_link = '''https://docs.google.com/spreadsheets/d/
    1n3aDcsdgAMb17yXnmKZHUm4hK7P8exlkO6H0NdvLZZ8/edit?usp=sharing'''

    sheet_name = 'Medicines Diabetics'

# use file (for testing) or online version (for regular executions)
    if use_file_not_url:
        excel_source = file.strip()
    else:
        google_key_pattern_begin = '.*/d/'
        google_key_pattern_end = '/[^/]*'
        google_key_only = re.sub(
            rf'{google_key_pattern_end}', '',
            re.sub(rf'{google_key_pattern_begin}', '', full_google_link)
            ).strip()

        url = 'https://docs.google.com/spreadsheet/ccc?key=' + \
            google_key_only + '&output=xlsx'
        excel_source = url

    # read from google sheets (file or online)
    loaded_df = pd.read_excel(excel_source, sheet_name=sheet_name)

    return loaded_df


# Start counter
start_time = time.time()

st.warning('Reading data from Google Sheets can tale around 30 seconds.')

st.markdown("""<HR>""", unsafe_allow_html=True,)

# ! Change this if you want to read from live Google Sheets !
use_file_not_url = st.checkbox('Read from local file? Uncheck if run remotely!!!', False)
# ! Change this if you want to read from live Google Sheets !

st.markdown("""<HR>""", unsafe_allow_html=True,)

# ?????????????????????????????????????????????????????????
# ??????????????????????????????????????????????????????????????????????????????????????????????????????????????????
# ??????????????????????????????????????????????????????????????????????????????????????????????????????????????????
# ?????????????????????????????????????????????????????????
# ! If you want to simulate an extra
# ! collection, set extra_collection_requested
# ! to True and provide an extra date
# ! e.g. tomorrows date. Additionally
# ! set values in the below df creator
extra_collection_requested = st.checkbox('Do you want to simulate an extra collection?')
# st.warning(extra_collection_requested)
extra_collection_date_time = \
    pd.to_datetime('today').date() + pd.Timedelta('1 days')  # time is redundand as plenty of the code below was amended
extra_collection_date_time = \
    st.date_input(
        f'Enter new date. The default one is {extra_collection_date_time}: ',
        extra_collection_date_time,
        min_value='today'
        )

df_extra = pd.DataFrame(
    {
        'Date': [extra_collection_date_time,
                 extra_collection_date_time,
                 extra_collection_date_time],
        'Name': ['Atorvastatin',
                 'Dapagliflozin',
                 'Metformin'],
        'collected_today_mg': [28*40.0, 28*5.0, 56*1000],
    },
    index=[10000, 10001, 10002]
)
# ?????????????????????????????????????????????????????????
# ??????????????????????????????????????????????????????????????????????????????????????????????????????????????????
# ??????????????????????????????????????????????????????????????????????????????????????????????????????????????????
# ?????????????????????????????????????????????????????????

st.markdown("""<HR>""", unsafe_allow_html=True,)

df = load_df_from_google_sheets(use_file_not_url)

# select relevant columns from spreadsheet
# for collections table and drop extra
# empty lines
df_collections = df.loc[:, 'Date':'Size (mg)']
df_collections.dropna(
    axis=0, how='any', subset=['Name'], inplace=True
    )

# select relevant columns from spreadsheet
# for dosage table and drop extra
# empty lines
df_dosage = df.loc[:, 'Date.1':'Evening']
df_dosage.rename(columns={
    'Date.1': 'Date', 'Name.1': 'Name',
    },
                 inplace=True
                 )
df_dosage.dropna(
    axis=0, how='any', subset=['Name'], inplace=True
    )

# replace Null with zeroes and add all doses from same day
# to calculate the whole day dosage for particular tablets
# then drop columns that were used for this calculation
df_dosage.fillna(0, inplace=True)
df_dosage['daily_dose_mg'] = (df_dosage['Morning'] + df_dosage['Afternoon'] + df_dosage['Evening'])
df_dosage.drop(columns=['Morning', 'Afternoon', 'Evening'], inplace=True)

# calculate total of particular medicine (mg)
# collected on particular day
# then drop columns that were used for this calculation
df_collections['collected_today_mg'] = df_collections['Quantity'] * df_collections['Size (mg)']
df_collections.drop(columns=['Quantity', 'Size (mg)'], inplace=True)

# standarise 'Data' to be data only 
# without the time component
df_dosage['Date'] = df_dosage['Date'].apply(lambda x: pd.to_datetime(x).date())
df_collections['Date'] = df_collections['Date'].apply(lambda x: pd.to_datetime(x).date())

# st.warning('tables prepared:')
# st.dataframe(df_collections)
# st.dataframe(df_dosage)
# st.write(df_collections.dtypes)
# st.write(df_dosage.dtypes)

if extra_collection_requested:
    df_collections = pd.concat([df_collections, df_extra])
# st.dataframe(df_collections)

# unpivot three columns
# from wide to long data structure
df_dosage = df_dosage.pivot(columns=['Name'], values=['daily_dose_mg'], index=['Date'])
df_collections = df_collections.pivot(columns=['Name'], values=['collected_today_mg'], index=['Date'])

# drop an extra index level which appeared after pivoting
df_dosage.columns = df_dosage.columns.droplevel(0)
df_collections.columns = df_collections.columns.droplevel(0)

# add suffixes to columns:
# for dosage use '_out'
# for collections use '_in'
columns_iterator = df_collections.columns
for i_column in columns_iterator:
    df_collections.rename(columns={i_column: i_column + '_in'}, inplace=True)
    df_dosage.rename(columns={i_column: i_column + '_out'}, inplace=True)


# merge colloections and dosage on 'Date'
# outer, so all rows from both tables
# are included
df_full = df_collections.merge(df_dosage, how='outer', on='Date')
# st.write('dosage and collections merged')
# st.warning(type(df_full))
# st.write(df_full)

# !!!!! set dates here - start must be first medicines collection date
start_date = '2025-05-12'
end_date = str(pd.to_datetime('today').date() + pd.Timedelta("60 days"))  # '2025-09-22'
# st.write(f'start {type(start_date)}, end {type(end_date)}')
# !!!!!

# Create the full datetime index for required dates
full_index = pd.date_range(start=start_date, end=end_date)   #, freq="D")

df_full = df_full.reindex(full_index)
df_full.sort_index(inplace=True)
df_full.index = df_full.index.date

# fill Nulls in colections with zeros (no extra medicines added)
# fill Nulls in dosage with previous dosage value - if Null
# then the previous dosege has not changes so is the same value 
# as was a day before
columns_iterator_new = df_full.columns
# uses iterator_new with _in an _out suffixes
for i_column in columns_iterator_new:
    # st.warning(i_column)
    if '_out' in i_column:
        df_full[i_column].ffill(inplace=True)
    elif '_in' in i_column:
        df_full[i_column].fillna(0, inplace=True)

# calculates difference between two running totals:
# 'collections running total' (all collected till date)
# minus
# 'dosage running total' (all consumed till date)
# uses 'old' iterator without _in or _out suffixes
for i_column in columns_iterator:
    df_full[i_column] = \
        df_full[i_column + '_in'].cumsum() - \
        df_full[i_column + '_out'].cumsum()
    df_full[i_column] = \
        df_full[i_column].apply(MustBeGreaterThanZero).fillna('')

st.write(df_collections)
st.write(df_dosage)
df_full.drop(columns=['Atorvastatin_in', 'Dapagliflozin_in', 'Metformin_in',
                      'Atorvastatin_out', 'Dapagliflozin_out', 'Metformin_out'],
             inplace=True)
st.write(df_full[49:])

df_full.to_csv('./medicines.csv')
df_full.to_excel('./medicines.xlsx', sheet_name='RunningTotal',)
# df_full.to_markdown('./medicines.md',)

st.markdown("""<HR>""", unsafe_allow_html=True,)

# Show counter
end_time = time.time()
st.warning(f"\nElapsed Time: {round(end_time-start_time, 2)} seconds")
