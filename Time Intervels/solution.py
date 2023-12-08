import pandas as pd
import re

df= pd.read_csv('output.csv')
df.columns=df.columns.str.strip()

date_pattern = r'\d{2}-\d{2}-\d{4}'
hour_pattern = r'^(1?\d|2[0-4])$'
time_block_pattern = r'\d{2}:\d{2} - \d{2}:\d{2}'

def get_transformed_df(df):
    for index, row in df.iterrows():
        first_col_val = row.iloc[0]
        shift_amount = 0
        if re.match(date_pattern, first_col_val):
            shift_amount = 0
        elif re.match(hour_pattern, first_col_val):
            shift_amount = 1
        elif re.match(time_block_pattern, first_col_val):
            shift_amount = 2

        shifted_row = row.shift(shift_amount)
        df.iloc[index] = shifted_row

    return df

result = get_transformed_df(df)
result.to_csv('result.csv', index=False)