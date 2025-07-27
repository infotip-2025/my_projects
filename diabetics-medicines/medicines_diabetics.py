
import pandas as pd
import re
import time

# Start counter
start_time = time.time()

use_file_not_url = True
file = '''t:/_DOWNLOAD_/ROGcio/Chlanie browara i reszta statystyk Sprinkwell.xlsx'''

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

df = pd.read_excel(excel_source, sheet_name=sheet_name)
df_collections = df.loc[:, 'Date':'Size (mg)']
df_collections.dropna(
    axis=0, how='any', subset=['Name'], inplace=True
    )
df_dosage = df.loc[:, 'Date.1':'Evening']
df_dosage.rename(columns={
    'Date.1': 'Date', 'Name.1': 'Name',
    'Morning': '6:00', 'Afternoon': '12:00', 'Evening': '18:00'},
                 inplace=True
                 )
df_dosage.dropna(
    axis=0, how='any', subset=['Name'], inplace=True
    )
# df_dosage.fillna(
#     value='', method=None, inplace=True
#     )

# unpivot three columns
df_dosage = pd.melt(df_dosage,
                    id_vars=['Date', 'Name'],
                    value_vars=['6:00', '12:00', '18:00'],
                    var_name='Day_Time',
                    value_name='Dosage'
                    )

df_dosage['Date'] = df_dosage['Date'].astype(str)

df_dosage['Index'] = pd.to_datetime(
    df_dosage['Date']+df_dosage['Day_Time'], format='%Y-%m-%d%H:%M'
    )
df_dosage.sort_values(
    by='Index', ascending=True, inplace=True
    )
df_dosage.set_index('Index', inplace=True)

# print(df_dosage.dtypes)

mask_empty_dosage_removed = df_dosage['Dosage'].notnull()
df_dosage = df_dosage[mask_empty_dosage_removed]

df_dosage.drop(columns=['Date', 'Day_Time'], inplace=True)

# .fillna(
#     value = {'deck':'X'},
#     method = None, ## We're using
#                       a pre-determined value, not backfilling/padding
#     inplace = True ## Have the changes take place
# )

print(df_dosage.columns)
print(df_collections.loc[:])
print()
print(df_dosage.loc[:])

# Show counter
end_time = time.time()
print(f"\nElapsed Time: {round(end_time-start_time, 2)} seconds")
