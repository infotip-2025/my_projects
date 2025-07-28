# from datetime import date, timedelta

# start_date = date(2025, 5, 12)
# end_date = date(2025, 7, 28)
# delta = timedelta(days=1)
# while start_date <= end_date:
#     print(start_date.strftime("%Y-%m-%d %H:%M"))
#     start_date += delta

import pandas as pd

# display only date using date() function
for i in pd.bdate_range(start='2025-05-12', end='2025-07-28', freq='6h'):
    if i.time() != pd.to_datetime('00:00:00').time():
        print(i)
