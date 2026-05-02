import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import openpyxl
import requests
from bs4 import BeautifulSoup

def parse_apartments_csv():
    df = pd.read_csv('Экспозиция ТДСК с 01.07.2023 по 31.12.2023 (1).csv', sep='\t')

    df['actualized_at'] = pd.to_datetime(df['actualized_at'], format='ISO8601').dt.tz_localize(None).dt.normalize()
    return df
def make_actual_table_to_write(df: pd.DataFrame):
    dates = pd.date_range(start='2023-07-01', end='2023-12-31')
    df['gp'] = [gp[:gp.find(')') + 1] for gp in df['address']]
    corpuses = df['gp'].unique()[df['gp'].unique() != '']
    rows = []
    for i in dates:
        for gp in corpuses:
            rows.append({'Дата': i.strftime('%d.%m.%Y'), 'Корпус': gp, 'Количество активных квартир': len(df[(df['actualized_at'] >= i) & (df['gp'] == gp)])})

    actual_table = pd.DataFrame(rows)
    actual_table.to_excel('actual_table.xlsx', index=False,engine='xlsxwriter')
df = parse_apartments_csv()
make_actual_table_to_write(df)
