An interactive web application to visualize personal financial transactions over time. The app provides dynamic charting and filtering capabilities, helping users understand spending patterns and trends at a glance.

By default, the app connects to a local **PostgreSQL** database to store and retrieve transactions. If PostgreSQL is not available, it automatically falls back to a local transactions.csv file.

As of now when the list of transactions (.csv) is uploaded or entered via the transaction form, data visualization of income/expenses over time is given.

Will be using Plaid APIs in the future to gather live data and have it visualized in the future along with income and expense usage and additional features to give beneficial feedback regarding the user's finances.

Installation
------------

1.  git clone https://github.com/yourusername/personal-finance-tracker.gitcd personal-finance-tracker
    
2.  pip install -r requirements.txtKey libraries include:
    
    *   dash
        
    *   plotly
        
    *   pandas
        
    *   sqlalchemy
        
    *   psycopg2
        
3.  (Optional) Set up PostgreSQL:
    
    *   Make sure PostgreSQL is installed and running on your system.
        
    *   createdb finance\_db
        
    *   Update the connection string inside process\_data.py if needed (default assumes postgres:password@localhost:5432/finance\_db).
        
4.  python3 app.py
    

The app will be available at http://127.0.0.1:8050/.