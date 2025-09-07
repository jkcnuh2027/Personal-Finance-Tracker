import pandas as pd

def load_transactions(file_path="data/transactions.csv"):
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])  # Match your CSV
    return df

def filter_by_category(df, categories):
    return df[df['Category'].isin(categories)]

df = load_transactions("data/transactions.csv")
options = [{'label': c, 'value': c} for c in df['Category'].unique()]
