
import pandas as pd
import re
import time

def MustBeGreaterThanZero (x):
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
        tablets_quantities = list(stock.values())
        
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


# Start counter
start_time = time.time()

# ! Change this if you want to read from live Google Sheets !
use_file_not_url = True
# ! Change this if you want to read from live Google Sheets !

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
    }, # 'Morning': '6:00', 'Afternoon': '12:00', 'Evening': '18:00'},
                 inplace=True
                 )
df_dosage.dropna(
    axis=0, how='any', subset=['Name'], inplace=True
    )
# df_dosage.fillna(
#     value='', method=None, inplace=True
#     )
'''
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


full_datetimes = pd.to_datetime(
    [f"{date.date()} {time}" for date in full_index for time in times]
)

# Reindex the original DataFrame to include the full range
#df_dosage = df_dosage.reindex(full_datetimes)
#df_dosage.sort_index(inplace=True)
'''

df_dosage.fillna(0, inplace=True)
df_dosage['daily_dose_mg'] = (df_dosage['Morning'] + df_dosage['Afternoon'] + df_dosage['Evening'])
df_dosage.drop(columns=['Morning', 'Afternoon', 'Evening'], inplace=True)

df_collections['collected_today_mg'] = df_collections['Quantity'] * df_collections['Size (mg)']
df_collections.drop(columns=['Quantity', 'Size (mg)'], inplace=True)

# unpivot three columns
df_dosage = df_dosage.pivot(columns=['Name'], values=['daily_dose_mg'], index=['Date']) #.fillna(0)
df_collections = df_collections.pivot(columns=['Name'], values=['collected_today_mg'], index=['Date']) #.fillna(0)

df_dosage.columns = df_dosage.columns.droplevel(0)
df_collections.columns = df_collections.columns.droplevel(0)

columns_iterator = df_collections.columns

for i_column in columns_iterator:
    df_collections.rename(columns={i_column: i_column + '_in'}, inplace=True)
    df_dosage.rename(columns={i_column: i_column + '_out'}, inplace=True)
    
df_full = df_collections.merge(df_dosage, how='outer', on='Date')

start_date = '2025-05-12'
end_date = '2025-08-28'
# Create the full datetime index
full_index = pd.date_range(start=start_date, end=end_date, freq="D")

df_full = df_full.reindex(full_index)
df_full.sort_index(inplace=True)


columns_iterator_new = df_full.columns
for i_column in columns_iterator_new:
    if '_out' in i_column:
        df_full[i_column].ffill(inplace=True)
    elif '_in' in i_column:
        df_full[i_column].fillna(0, inplace=True)

for i_column in columns_iterator:
    df_full[i_column] = df_full[i_column + '_in'].cumsum() - df_full[i_column + '_out'].cumsum()    
    df_full[i_column] = df_full[i_column].apply(MustBeGreaterThanZero).fillna('')
        
# for i_column in columns_iterator:
#     df_full[i_column]=None
#     for i_row in range(len(df_full)):
#         df_full[i_column][i_row] = df_full[i_column+'_in'][i_row] - df_full[i_column+'_out'][i_row]

print(df_collections)
print(df_dosage)
df_full.drop(columns=['Atorvastatin_in', 'Dapagliflozin_in', 'Metformin_in', 'Atorvastatin_out', 'Dapagliflozin_out', 'Metformin_out'], inplace=True)
print(df_full[49:])

df_full.to_csv('./medicines.csv')
df_full.to_excel('./medicines.xlsx', sheet_name='RunningTotal',)
df_full.to_markdown('./medicines.md',)
# Show counter
end_time = time.time()
print(f"\nElapsed Time: {round(end_time-start_time, 2)} seconds")

