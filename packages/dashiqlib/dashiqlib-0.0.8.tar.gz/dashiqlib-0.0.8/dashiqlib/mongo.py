"""DashIQ MongoDB data access methods"""
import os
from re import finditer
from pymongo import MongoClient
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

conn_str = os.getenv('MONGODB_CONN_STR')

DB_NAME = 'meltano'


def google_ad_group_performance() -> pd.DataFrame:
    """Returns a DataFrame of Google Ads performance data"""
    client = MongoClient(conn_str)
    db = client[DB_NAME]
    ad_grp = pd.json_normalize(list(db.get_collection('ad_group_performance').find()))
    cmpn = pd.json_normalize(list(db.get_collection('campaign').find()))

    # Merge so we have the campaign name
    df = pd.merge(
            ad_grp,cmpn[['campaign.resourceName','campaign.name']],
            on='campaign.resourceName',
            how='left')
    # Type the columns we need properly
    df['metrics.clicks'] = pd.to_numeric(df['metrics.clicks'])
    df['metrics.costMicros'] = pd.to_numeric(df['metrics.costMicros'])
    df['metrics.impressions'] = pd.to_numeric(df['metrics.impressions'])
    df['segments.date'] = pd.to_datetime(df['segments.date'])
    return df

def google_conversions_by_location() -> pd.DataFrame:
    """Returns a DataFrame of conversion data from Google Ads"""
    client = MongoClient(conn_str)
    db = client[DB_NAME]
    conv = pd.json_normalize(list(db.get_collection('conversion_by_location').find()))
    return conv


def get_metrics_cols(df: pd.DataFrame) -> list:
    """Returns a list of user friendly labels derived form DataFrame column names"""
    cols = []
    for col in df.columns:
        if str(col).startswith("metrics."):
            cols.append({'label': camel_to_human(str(col).split(".")[1]), 'value': col })
    return cols

def camel_to_human(instr: str) -> str:
    """Converts a camel case string to a human readable string"""
    split = ' '.join(camel_case_split(instr)).title()
    return split

def camel_case_split(identifier):
    """Returns a split string based on a camel case input"""
    matches = finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    return [m.group(0) for m in matches]
