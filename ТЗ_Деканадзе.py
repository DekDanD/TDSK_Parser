import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import openpyxl

def parse_apartments_csv():
    df = pd.read_csv('Экспозиция ТДСК с 01.07.2023 по 31.12.2023 (1).csv', sep='\t')
    actual_table = pd.DataFrame()
    df['actualized_at'] = pd.to_datetime(df['actualized_at'], format='ISO8601')
    df['actualized_at'] = df['actualized_at'].dt.strftime('%d-%m-%Y')
    print(df['actualized_at'].drop_duplicates())
    dates = pd.date_range(start='2023-07-01', end='2023-12-31')
    dates_list = dates.strftime('%d-%m-%y').tolist()
    df['gp'] = [gp[:gp.find(')') + 1] for gp in df['address']]
    print(df['gp'])
    for i in dates_list:
        actual_table.loc[len(actual_table)] = {'Дата': i}
    for i, row in df.iterrows():
        dates = pd.date_range(start='2023-07-01', end='2023-12-31')
        
    print(df)

parse_apartments_csv()