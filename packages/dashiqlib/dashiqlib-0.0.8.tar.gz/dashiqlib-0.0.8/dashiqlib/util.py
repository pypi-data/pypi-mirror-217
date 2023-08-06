"""Utility functions for DashIQ lib"""

from pandas import DataFrame


def df_mask_from_dates(df: DataFrame, start_date, end_date) -> DataFrame:
    """Returns a masked dataframe based on a start_date and end_date"""
    _df = df
    if start_date is not None:
        mask = df['segments.date'] > start_date
        _df = df.loc[mask]
    if end_date is not None:
        mask = df['segments.date'] <= end_date
        _df = _df.loc[mask]
    return _df
