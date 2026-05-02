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
            rows.append({'Дата': i.strftime('%d.%m.%Y'), 
                         'Корпус': gp,
                        'Количество активных квартир': len(df[(df['actualized_at'] >= i) & (df['gp'] == gp)])})

    actual_table = pd.DataFrame(rows)
    actual_table.to_excel('actual_table.xlsx', index=False,engine='xlsxwriter')


def extend_dataframe(df: pd.DataFrame):
    pass


def plot_graphics(df: pd.DataFrame):
    df['published_at'] = pd.to_datetime(df['published_at'], format='ISO8601').dt.tz_localize(None).dt.normalize()
    df['actualized_at'] = pd.to_datetime(df['actualized_at'])
    df_for_plot = df[(df['actualized_at'] >= '2023-07-01') & (df['actualized_at'] <= '2024-12-31') & (df['published_at'] <= '2023-12-31')]
    life = df_for_plot.groupby(['id', 'room_count']).agg(
    start=('published_at', 'min'), 
    end=('actualized_at', 'max')
).reset_index()
    active_months = []
    for m in range(7, 13):
        mask = (life['start'].dt.month <= m) & (life['end'].dt.month >= m)
        temp = life[mask].copy()
        temp['month'] = m
        active_months.append(temp)

    pivot_table = pd.concat(active_months).pivot_table(index='month', columns='room_count', values='id', aggfunc='count')
    pivot_table.plot(kind='bar', figsize=(12, 6), title='Активные объекты ТДСК (2П 2023)')
    plt.show()

    plt.pie(df['room_count'].value_counts(), labels=df['room_count'].value_counts().index)
    plt.title('Распределение квартир по комнатам (изначальная выборка)')
    plt.legend()
    plt.axis('equal')
    plt.show()

    bins = [0, 20, 30, 40, 50, 60, 70, 80, 90, 100, float('inf')]
    labels = ['<20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100', '>100']

    df_area = pd.cut(df['area'], bins=bins, labels=labels).value_counts().sort_index()

    x = np.arange(len(labels))
    width = 0.4

    bars = plt.bar(x, df_area, width)
    plt.bar_label(bars)
    plt.show()

    bins = [0, 4000000, 5000000, 6000000, 7000000, 8000000, float('inf')]
    labels = ['<4 млн', '4-5', '5-6', '6-7', '7-8', '>8 млн']

    df_price = pd.cut(df['price'], bins=bins, labels=labels).value_counts().sort_index()

    x = np.arange(len(labels))
    width = 0.4

    bars = plt.bar(x, df_price, width)
    plt.bar_label(bars)
    plt.show()

df = parse_apartments_csv()
make_actual_table_to_write(df)
plot_graphics(df)

extend_dataframe(df)
