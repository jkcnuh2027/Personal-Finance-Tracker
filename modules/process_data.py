import pandas as pd
import os
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# PostgreSQL connection string
DB_URL = "postgresql+psycopg2://username:password@localhost:5432/finance_db"
CSV_FILE = "data/transactions.csv"

# Create engine
try:
    engine = create_engine(DB_URL)
    with engine.connect() as conn:
        print("Connected to PostgreSQL!")
    USE_DB = True
except OperationalError:
    print("PostgreSQL not available, using CSV fallback.")
    USE_DB = False

def load_transactions():
    """Load transactions from PostgreSQL if available, otherwise CSV"""
    if USE_DB:
        try:
            df = pd.read_sql("SELECT * FROM transactions", engine)
        except Exception as e:
            print(f"Error loading from DB: {e}, falling back to CSV")
            df = pd.read_csv(CSV_FILE)
    else:
        df = pd.read_csv(CSV_FILE)
    
    # Ensure consistent column names
    df = df.rename(columns={
        'Date': 'date', 
        'Category': 'category', 
        'Amount': 'amount', 
        'Description': 'description'
    })
    return df

def insert_transaction(date, category, amount, description):
    """Insert a transaction into PostgreSQL or append to CSV"""
    df_new = pd.DataFrame([{
        'date': date,
        'category': category,
        'amount': amount,
        'description': description
    }])
    
    if USE_DB:
        try:
            df_new.to_sql('transactions', engine, if_exists='append', index=False)
        except Exception as e:
            print(f"Error inserting to DB: {e}, writing to CSV instead")
            df_new.to_csv(CSV_FILE, mode='a', header=not os.path.exists(CSV_FILE), index=False)
    else:
        df_new.to_csv(CSV_FILE, mode='a', header=not os.path.exists(CSV_FILE), index=False)

def filter_by_category(df, selected_categories):
    """Filter transactions by selected categories"""
    if not selected_categories:
        return df
    return df[df['category'].isin(selected_categories)]
