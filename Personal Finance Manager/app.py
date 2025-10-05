import pandas as pd
from dash import Dash, dcc, html, Input, Output, State, callback_context
import dash
import plotly.graph_objects as go
from datetime import datetime, timedelta
import calendar

from modules.charts import (
    create_area_chart,
    create_bar_chart,
    create_line_chart,
    create_pie_chart,
    create_funnel_chart,
    create_advanced_area_chart,
    create_advanced_pie_chart,
    create_trend_chart,
    create_comparison_chart
)
from modules.process_data import load_transactions, filter_by_category, insert_transaction, get_monthly_stats, get_daily_averages, get_percentage_changes

app = Dash(__name__)

# Add custom CSS for responsive design
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
            * {
                box-sizing: border-box;
            }
            
            body {
                margin: 0;
                padding: 0;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }
            
            /* Responsive grid system */
            .responsive-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1rem;
            }
            
            .responsive-flex {
                display: flex;
                flex-wrap: wrap;
                gap: 1rem;
            }
            
            .responsive-flex > * {
                flex: 1;
                min-width: 250px;
            }
            
            /* Mobile optimizations */
            @media (max-width: 768px) {
                .responsive-grid {
                    grid-template-columns: 1fr;
                }
                
                .responsive-flex {
                    flex-direction: column;
                }
                
                .responsive-flex > * {
                    min-width: 100%;
                }
                
                .metric-card {
                    margin-bottom: 1rem;
                }
                
                .chart-container {
                    width: 100% !important;
                    margin-left: 0 !important;
                }
                
                .stats-panel {
                    width: 100% !important;
                    margin-left: 0 !important;
                    margin-top: 1rem;
                }
            }
            
            /* Enhanced hover effects */
            .card-hover {
                transition: all 0.3s ease;
            }
            
            .card-hover:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            }
            
            /* Custom scrollbar */
            ::-webkit-scrollbar {
                width: 8px;
            }
            
            ::-webkit-scrollbar-track {
                background: #f1f5f9;
            }
            
            ::-webkit-scrollbar-thumb {
                background: #cbd5e1;
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: #94a3b8;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Initial data
df = load_transactions()

# ----- Modern Design System -----
APP_STYLE = {
    'fontFamily': "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    'backgroundColor': '#f8fafc',
    'minHeight': '100vh',
    'margin': 0,
    'padding': 0
}

HEADER_STYLE = {
    'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'color': 'white',
    'padding': '2rem 0',
    'marginBottom': '2rem',
    'boxShadow': '0 4px 20px rgba(0,0,0,0.1)'
}

CARD_STYLE = {
    'backgroundColor': '#ffffff',
    'padding': '1.5rem',
    'borderRadius': '16px',
    'boxShadow': '0 4px 20px rgba(0,0,0,0.08)',
    'border': '1px solid #e2e8f0',
    'transition': 'all 0.3s ease'
}

METRIC_CARD = {
    **CARD_STYLE,
    'textAlign': 'center',
    'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'color': 'white',
    'border': 'none'
}

BUTTON_STYLE = {
    'backgroundColor': '#667eea',
    'color': 'white',
    'border': 'none',
    'padding': '12px 24px',
    'borderRadius': '8px',
    'fontSize': '14px',
    'fontWeight': '600',
    'cursor': 'pointer',
    'transition': 'all 0.3s ease',
    'boxShadow': '0 2px 8px rgba(102, 126, 234, 0.3)'
}

INPUT_STYLE = {
    'width': '100%',
    'padding': '12px 16px',
    'border': '2px solid #e2e8f0',
    'borderRadius': '8px',
    'fontSize': '14px',
    'transition': 'all 0.3s ease',
    'marginBottom': '12px'
}

def to_plot_columns(dframe: pd.DataFrame) -> pd.DataFrame:
    """Rename to the TitleCase columns expected by chart functions."""
    return dframe.rename(columns={'date': 'Date', 'amount': 'Amount', 'category': 'Category'})

app.layout = html.Div([
    # Header Section
    html.Div([
        html.Div([
            html.H1("💰 Personal Finance Tracker", style={
                'fontSize': '2.5rem',
                'fontWeight': '700',
                'margin': 0,
                'textAlign': 'center'
            }),
            html.P("Advanced Analytics & Modern Dashboard", style={
                'fontSize': '1.1rem',
                'opacity': 0.9,
                'margin': '0.5rem 0 0 0',
                'textAlign': 'center'
            })
        ], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '0 2rem'})
    ], style=HEADER_STYLE),

    # Main Container
    html.Div([
        # Key Metrics Row
        html.Div([
            html.Div([
                html.Div([
                    html.H3("💰 Total Income", style={'margin': '0 0 0.5rem 0', 'fontSize': '1.1rem'}),
                    html.H2(id='total-income', style={'margin': 0, 'fontSize': '2rem', 'fontWeight': '700'})
                ], style={**METRIC_CARD, 'className': 'metric-card card-hover'}),
                html.Div([
                    html.H3("💸 Total Expenses", style={'margin': '0 0 0.5rem 0', 'fontSize': '1.1rem'}),
                    html.H2(id='total-expenses', style={'margin': 0, 'fontSize': '2rem', 'fontWeight': '700'})
                ], style={**METRIC_CARD, 'className': 'metric-card card-hover'}),
                html.Div([
                    html.H3("📊 Net Balance", style={'margin': '0 0 0.5rem 0', 'fontSize': '1.1rem'}),
                    html.H2(id='net-balance', style={'margin': 0, 'fontSize': '2rem', 'fontWeight': '700'})
                ], style={**METRIC_CARD, 'className': 'metric-card card-hover'}),
                html.Div([
                    html.H3("📈 Daily Average", style={'margin': '0 0 0.5rem 0', 'fontSize': '1.1rem'}),
                    html.H2(id='daily-average', style={'margin': 0, 'fontSize': '2rem', 'fontWeight': '700'})
                ], style={**METRIC_CARD, 'className': 'metric-card card-hover'})
            ], className='responsive-grid', style={'marginBottom': '2rem'})
        ]),

        # Filters and Controls Row
        html.Div([
            html.Div([
                html.H4("📅 Time Range", style={'marginBottom': '1rem', 'color': '#374151'}),
                dcc.DatePickerRange(
                    id='date-range',
                    start_date=df['date'].min() if not df.empty else datetime.now() - timedelta(days=30),
                    end_date=df['date'].max() if not df.empty else datetime.now(),
                    display_format='YYYY-MM-DD',
                    style={'width': '100%'}
                )
            ], style={**CARD_STYLE, 'className': 'card-hover'}),
            
            html.Div([
                html.H4("📊 Chart Type", style={'marginBottom': '1rem', 'color': '#374151'}),
                dcc.Dropdown(
                    id='chart-type',
                    options=[
                        {'label': '📈 Area Chart', 'value': 'area'},
                        {'label': '📊 Bar Chart', 'value': 'bar'},
                        {'label': '📉 Line Chart', 'value': 'line'},
                        {'label': '🥧 Pie Chart', 'value': 'pie'},
                        {'label': '📊 Trend Analysis', 'value': 'trend'},
                        {'label': '📊 Month Comparison', 'value': 'comparison'}
                    ],
                    value='area',
                    clearable=False,
                    style={'width': '100%'}
                )
            ], style={**CARD_STYLE, 'className': 'card-hover'}),
            
            html.Div([
                html.H4("🏷️ Categories", style={'marginBottom': '1rem', 'color': '#374151'}),
                dcc.Dropdown(
                    id='categories',
                    options=[{'label': c, 'value': c} for c in df['category'].unique()],
                    value=list(df['category'].unique()),
                    multi=True,
                    style={'width': '100%'}
                )
            ], style={**CARD_STYLE, 'className': 'card-hover'})
        ], className='responsive-flex', style={'marginBottom': '2rem'}),

        # Main Charts Section
        html.Div([
            # Left Chart
            html.Div([
                html.Div([
                    dcc.Graph(id='main-chart', style={'height': '500px'})
                ], style={**CARD_STYLE, 'className': 'card-hover'})
            ], className='chart-container', style={'width': '65%', 'display': 'inline-block', 'verticalAlign': 'top'}),

            # Right Stats Panel
            html.Div([
                html.Div([
                    html.H4("📊 Monthly Statistics", style={'marginBottom': '1rem', 'color': '#374151'}),
                    html.Div(id='monthly-stats')
                ], style={**CARD_STYLE, 'className': 'card-hover'}),
                
                html.Div([
                    html.H4("📈 Trend Analysis", style={'marginBottom': '1rem', 'color': '#374151'}),
                    html.Div(id='trend-analysis')
                ], style={**CARD_STYLE, 'className': 'card-hover', 'marginTop': '1rem'})
            ], className='stats-panel', style={'width': '32%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginLeft': '3%'})
        ], style={'marginBottom': '2rem'}),

        # Add Transaction Section
        html.Div([
            html.Div([
                html.H3("➕ Add New Transaction", style={'marginBottom': '1.5rem', 'color': '#374151', 'textAlign': 'center'}),
                html.Div([
                    html.Div([
                        html.Label("📅 Date", style={'fontWeight': '600', 'marginBottom': '0.5rem', 'display': 'block'}),
                        dcc.DatePickerSingle(
                            id='input-date',
                            date=datetime.now().date(),
                            display_format='YYYY-MM-DD',
                            style={'width': '100%'}
                        )
                    ], style={'width': '25%', 'marginRight': '1rem'}),
                    
                    html.Div([
                        html.Label("🏷️ Category", style={'fontWeight': '600', 'marginBottom': '0.5rem', 'display': 'block'}),
                        dcc.Dropdown(
                            id='input-category',
                            options=[{'label': c, 'value': c} for c in df['category'].unique()],
                            placeholder='Select Category',
                            style={'width': '100%'}
                        )
                    ], style={'width': '25%', 'marginRight': '1rem'}),
                    
                    html.Div([
                        html.Label("💰 Amount", style={'fontWeight': '600', 'marginBottom': '0.5rem', 'display': 'block'}),
                        dcc.Input(id='input-amount', type='number', placeholder='0.00', style=INPUT_STYLE)
                    ], style={'width': '25%', 'marginRight': '1rem'}),
                    
                    html.Div([
                        html.Label("📝 Description", style={'fontWeight': '600', 'marginBottom': '0.5rem', 'display': 'block'}),
                        dcc.Input(id='input-desc', type='text', placeholder='Optional', style=INPUT_STYLE)
                    ], style={'width': '25%'})
                ], className='responsive-flex', style={'marginBottom': '1.5rem'}),
                
                html.Button('➕ Add Transaction', id='add-btn', n_clicks=0, style={**BUTTON_STYLE, 'width': '100%', 'fontSize': '16px', 'padding': '14px'})
            ], style={**CARD_STYLE, 'maxWidth': '800px', 'margin': '0 auto'})
        ]),

        # Hidden div for form output
        html.Div(id='form-output', style={'textAlign': 'center', 'marginTop': '1rem', 'fontWeight': '600'})
    ], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '0 2rem 2rem 2rem'})
], style=APP_STYLE)


# ----- Advanced Callbacks -----

# Update key metrics
@app.callback(
    [Output('total-income', 'children'),
     Output('total-expenses', 'children'),
     Output('net-balance', 'children'),
     Output('daily-average', 'children')],
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('categories', 'value')]
)
def update_metrics(start_date, end_date, selected_categories):
    data = load_transactions()
    
    # Filter by date range
    if start_date and end_date:
        data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]
    
    # Filter by categories
    if selected_categories:
        data = filter_by_category(data, selected_categories)
    
    if data.empty:
        return "$0", "$0", "$0", "$0"
    
    # Calculate metrics
    income = data[data['category'] == 'Income']['amount'].sum() if 'Income' in data['category'].values else 0
    expenses = data[data['category'] != 'Income']['amount'].sum()
    net_balance = income - expenses
    
    # Calculate daily average
    if start_date and end_date:
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date)
        days = (end_dt - start_dt).days + 1
        daily_avg = expenses / days if days > 0 else 0
    else:
        daily_avg = 0
    
    return f"${income:,.2f}", f"${expenses:,.2f}", f"${net_balance:,.2f}", f"${daily_avg:,.2f}"

# Update main chart
@app.callback(
    Output('main-chart', 'figure'),
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('chart-type', 'value'),
     Input('categories', 'value')]
)
def update_main_chart(start_date, end_date, chart_type, selected_categories):
    data = load_transactions()
    
    # Filter by date range
    if start_date and end_date:
        data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]
    
    # Filter by categories
    if selected_categories:
        data = filter_by_category(data, selected_categories)
    
    if data.empty:
        return go.Figure().add_annotation(text="No data available", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
    
    plot_data = to_plot_columns(data)
    
    if chart_type == 'area':
        return create_advanced_area_chart(plot_data)
    elif chart_type == 'bar':
        return create_bar_chart(plot_data)
    elif chart_type == 'line':
        return create_line_chart(plot_data)
    elif chart_type == 'pie':
        return create_advanced_pie_chart(plot_data)
    elif chart_type == 'trend':
        return create_trend_chart(plot_data)
    elif chart_type == 'comparison':
        return create_comparison_chart(plot_data)
    else:
        return create_advanced_area_chart(plot_data)

# Update monthly statistics
@app.callback(
    Output('monthly-stats', 'children'),
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('categories', 'value')]
)
def update_monthly_stats(start_date, end_date, selected_categories):
    data = load_transactions()
    
    # Filter by date range
    if start_date and end_date:
        data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]
    
    # Filter by categories
    if selected_categories:
        data = filter_by_category(data, selected_categories)
    
    if data.empty:
        return html.P("No data available", style={'color': '#6b7280'})
    
    stats = get_monthly_stats(data)
    return html.Div([
        html.Div([
            html.Span(f"📅 {month}", style={'fontWeight': '600', 'color': '#374151'}),
            html.Br(),
            html.Span(f"Income: ${income:,.2f}", style={'color': '#10b981', 'fontSize': '0.9rem'}),
            html.Br(),
            html.Span(f"Expenses: ${expenses:,.2f}", style={'color': '#ef4444', 'fontSize': '0.9rem'}),
            html.Br(),
            html.Span(f"Net: ${net:,.2f}", style={'color': '#3b82f6' if net >= 0 else '#ef4444', 'fontSize': '0.9rem', 'fontWeight': '600'})
        ], style={'padding': '0.75rem', 'border': '1px solid #e5e7eb', 'borderRadius': '8px', 'marginBottom': '0.5rem'})
        for month, income, expenses, net in stats
    ])

# Update trend analysis
@app.callback(
    Output('trend-analysis', 'children'),
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('categories', 'value')]
)
def update_trend_analysis(start_date, end_date, selected_categories):
    data = load_transactions()
    
    # Filter by date range
    if start_date and end_date:
        data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]
    
    # Filter by categories
    if selected_categories:
        data = filter_by_category(data, selected_categories)
    
    if data.empty:
        return html.P("No data available", style={'color': '#6b7280'})
    
    changes = get_percentage_changes(data)
    daily_avg = get_daily_averages(data)
    
    return html.Div([
        html.Div([
            html.H5("📈 Month-over-Month Changes", style={'marginBottom': '0.5rem', 'color': '#374151'}),
            *[html.Div([
                html.Span(f"{category}: ", style={'fontWeight': '600'}),
                html.Span(f"{change:+.1f}%", style={'color': '#10b981' if change > 0 else '#ef4444'})
            ], style={'marginBottom': '0.25rem'})
            for category, change in changes.items()]
        ]),
        html.Hr(style={'margin': '1rem 0'}),
        html.Div([
            html.H5("📊 Daily Averages", style={'marginBottom': '0.5rem', 'color': '#374151'}),
            *[html.Div([
                html.Span(f"{category}: ", style={'fontWeight': '600'}),
                html.Span(f"${avg:.2f}/day", style={'color': '#3b82f6'})
            ], style={'marginBottom': '0.25rem'})
            for category, avg in daily_avg.items()]
        ])
    ])

# Add transaction callback
@app.callback(
    [Output('form-output', 'children'),
     Output('categories', 'options'),
     Output('categories', 'value'),
     Output('input-category', 'options')],
    [Input('add-btn', 'n_clicks')],
    [State('input-date', 'date'),
     State('input-category', 'value'),
     State('input-amount', 'value'),
     State('input-desc', 'value')]
)
def add_transaction_callback(n_clicks, date, category, amount, desc):
    if n_clicks and n_clicks > 0 and date and category and amount is not None:
        try:
            insert_transaction(date, category, amount, desc)
            df_new = load_transactions()
            cats = list(df_new['category'].unique())
            opts = [{'label': c, 'value': c} for c in cats]
            return "✅ Transaction added successfully!", opts, cats, opts
        except Exception as e:
            return f"❌ Error: {e}", dash.no_update, dash.no_update, dash.no_update
    return "", dash.no_update, dash.no_update, dash.no_update


if __name__ == '__main__':
    app.run(debug=True)

