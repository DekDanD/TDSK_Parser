import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import openpyxl

def parse_apartments_csv():
    df = pd.read_csv('Экспозиция ТДСК с 01.07.2023 по 31.12.2023 (1).csv', sep='\t')
    actual_table = pd.DataFrame(columns=['Дата', 'Корпус', 'Количество активных квартир'])

    df['actualized_at'] = pd.to_datetime(df['actualized_at'], format='ISO8601')
    df['actualized_at'] = df['actualized_at'].dt.strftime('%d.%m.%y')
    dates = pd.date_range(start='2023-07-01', end='2023-12-31')
    dates_list = dates.strftime('%d.%m.%y').tolist()
    df['gp'] = [gp[:gp.find(')') + 1] for gp in df['address']]
    corpuses = df['gp'].unique()[df['gp'].unique() != '']
    for i in dates_list:
        for gp in corpuses:
            actual_table.loc[len(actual_table)] = {'Дата': i, 'Корпус': gp, 'Количество активных квартир': len(df[(df['actualized_at'] <= i) & (df['gp'] == gp)])}

    actual_table.to_excel('actual_table.xlsx')
parse_apartments_csv()