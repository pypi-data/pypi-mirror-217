import os
import pandas as pd

cur_dir = os.path.dirname(os.path.realpath(__file__))


def load_stock_returns_on_calls(data_type='train'):
    return pd.read_parquet(
        f'{cur_dir}/{data_type}/stock_return_data.parquet')


def load_stock_history():
    return pd.read_parquet(
        f'{cur_dir}/all_stock_price_history.parquet')


def load_call_description(data_type='train'):
    return pd.read_parquet(
        f'{cur_dir}/{data_type}/call_data.parquet')


def load_call_statements(data_type='train'):
    return pd.read_parquet(
        f'{cur_dir}/{data_type}/call_statement_data.parquet')
