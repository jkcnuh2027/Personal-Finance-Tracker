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

def get_monthly_stats(df):
    """Get monthly statistics for the filtered data"""
    if df.empty:
        return []
    
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])
    df['month_year'] = df['date'].dt.to_period('M')
    
    # Group by month and calculate stats
    monthly_stats = []
    for month in df['month_year'].unique():
        month_data = df[df['month_year'] == month]
        income = month_data[month_data['category'] == 'Income']['amount'].sum()
        expenses = month_data[month_data['category'] != 'Income']['amount'].sum()
        net = income - expenses
        
        monthly_stats.append((str(month), income, expenses, net))
    
    return sorted(monthly_stats, key=lambda x: x[0])

def get_daily_averages(df):
    """Calculate daily averages for each category"""
    if df.empty:
        return {}
    
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Calculate date range
    start_date = df['date'].min()
    end_date = df['date'].max()
    days = (end_date - start_date).days + 1
    
    if days == 0:
        return {}
    
    # Calculate daily averages by category
    daily_averages = {}
    for category in df['category'].unique():
        cat_data = df[df['category'] == category]
        total_amount = cat_data['amount'].sum()
        daily_avg = total_amount / days
        daily_averages[category] = daily_avg
    
    return daily_averages

def get_percentage_changes(df):
    """Calculate month-over-month percentage changes"""
    if df.empty:
        return {}
    
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])
    df['month_year'] = df['date'].dt.to_period('M')
    
    # Get unique months sorted
    months = sorted(df['month_year'].unique())
    if len(months) < 2:
        return {}
    
    # Calculate changes for each category
    changes = {}
    for category in df['category'].unique():
        cat_data = df[df['category'] == category]
        monthly_totals = cat_data.groupby('month_year')['amount'].sum()
        
        if len(monthly_totals) >= 2:
            # Compare last two months
            current_month = monthly_totals.iloc[-1]
            previous_month = monthly_totals.iloc[-2]
            
            if previous_month != 0:
                change = ((current_month - previous_month) / previous_month) * 100
                changes[category] = change
            else:
                changes[category] = 0 if current_month == 0 else 100
    
    return changes

def get_trend_analysis(df):
    """Get comprehensive trend analysis"""
    if df.empty:
        return {}
    
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])
    df['month_year'] = df['date'].dt.to_period('M')
    
    # Calculate trends for each category
    trends = {}
    for category in df['category'].unique():
        cat_data = df[df['category'] == category]
        monthly_totals = cat_data.groupby('month_year')['amount'].sum()
        
        if len(monthly_totals) >= 3:
            # Calculate trend direction
            recent_avg = monthly_totals.tail(2).mean()
            older_avg = monthly_totals.head(2).mean()
            
            if older_avg != 0:
                trend_direction = ((recent_avg - older_avg) / older_avg) * 100
                trends[category] = {
                    'direction': 'increasing' if trend_direction > 5 else 'decreasing' if trend_direction < -5 else 'stable',
                    'percentage': trend_direction
                }
            else:
                trends[category] = {'direction': 'stable', 'percentage': 0}
        else:
            trends[category] = {'direction': 'insufficient_data', 'percentage': 0}
    
    return trends
