# import plotly.express as px

# def create_area_chart(df):
#     fig = px.area(df, x='Date', y='Amount', color='Category', title='Expenses Over Time')
#     fig.update_layout(xaxis_title='Date', yaxis_title='Amount ($)')
#     return fig

# def create_bar_chart(df):
#     fig = px.bar(df, x='Date', y='Amount', color='Category', title='Expenses Over Time')
#     fig.update_layout(xaxis_title='Date', yaxis_title='Amount ($)')
#     return fig

# def create_line_chart(df):
#     fig = px.line(df, x='Date', y='Amount', color='Category', title='Expenses Over Time')
#     fig.update_layout(xaxis_title='Date', yaxis_title='Amount ($)')
#     return fig

# def create_pie_chart(df):
#     fig = px.pie(df, names='Category', values='Amount', title='Expense Distribution')
#     return fig

# def create_funnel_chart(df):
#     fig = px.funnel(df, x = 'Category', y = 'Amount', title='Expense Distribution')
#     return fig

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime

# Modern sophisticated color palette
COLOR_SEQ = [
    '#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe',
    '#43e97b', '#38f9d7', '#ffecd2', '#fcb69f', '#a8edea', '#fed6e3'
]

# Gradient colors for modern look
GRADIENT_COLORS = [
    'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
]

def create_area_chart(df):
    fig = px.area(
        df, 
        x='Date', 
        y='Amount', 
        color='Category', 
        template='plotly_white',
        color_discrete_sequence=COLOR_SEQ
    )
    fig.update_layout(
        title='Expenses Over Time',
        font=dict(family='Inter, sans-serif', size=14, color='#0a1f44'),
        plot_bgcolor='#f8f9fa',
        paper_bgcolor='#f8f9fa',
        xaxis=dict(showgrid=True, gridcolor='lightblue'),
        yaxis=dict(showgrid=True, gridcolor='lightblue'),
        legend=dict(title='', orientation='h', y=-0.2),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig

def create_bar_chart(df):
    fig = px.bar(
        df,
        x='Date',
        y='Amount',
        color='Category',
        title='Expenses Over Time',
        template='plotly_white',
        color_discrete_sequence=COLOR_SEQ
    )
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Amount ($)',
        font=dict(family='Inter, sans-serif', size=14, color='#0a1f44'),
        plot_bgcolor='#f8f9fa',
        paper_bgcolor='#f8f9fa',
        xaxis=dict(showgrid=True, gridcolor='lightblue'),
        yaxis=dict(showgrid=True, gridcolor='lightblue'),
        legend=dict(title='', orientation='h', y=-0.2),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig





def create_line_chart(df):
    fig = px.line(
        df,
        x='Date',
        y='Amount',
        color='Category',
        template='plotly_white',
        color_discrete_sequence=COLOR_SEQ
    )
    fig.update_layout(
        title='Expenses Over Time',
        font=dict(family='Inter, sans-serif', size=14, color='#0a1f44'),
        plot_bgcolor='#f8f9fa',
        paper_bgcolor='#f8f9fa',
        xaxis=dict(showgrid=True, gridcolor='lightblue'),
        yaxis=dict(showgrid=True, gridcolor='lightblue'),
        legend=dict(title='', orientation='h', y=-0.2),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig

def create_pie_chart(df):
    fig = px.pie(
        df,
        names='Category',
        values='Amount',
        title='Expense Distribution',
        template='plotly_white',
        color_discrete_sequence=COLOR_SEQ
    )
    fig.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#f8f9fa', width=2)))
    fig.update_layout(
        font=dict(family='Inter, sans-serif', size=14, color='#0a1f44'),
        plot_bgcolor='#f8f9fa',
        paper_bgcolor='#f8f9fa',
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig

def create_funnel_chart(df):
    fig = px.funnel(
        df,
        x='Amount',
        y='Category',
        template='plotly_white',
        color_discrete_sequence=COLOR_SEQ
    )
    fig.update_layout(
        title='Expense Funnel',
        font=dict(family='Inter, sans-serif', size=14, color='#0a1f44'),
        plot_bgcolor='#f8f9fa',
        paper_bgcolor='#f8f9fa',
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig

# Advanced Chart Functions
def create_advanced_area_chart(df):
    """Modern area chart with gradients and enhanced styling"""
    fig = px.area(
        df, 
        x='Date', 
        y='Amount', 
        color='Category',
        template='plotly_white',
        color_discrete_sequence=COLOR_SEQ
    )
    
    # Enhanced styling
    fig.update_layout(
        title=dict(
            text='📈 Financial Trends Over Time',
            font=dict(size=20, color='#1f2937'),
            x=0.5
        ),
        font=dict(family='Inter, sans-serif', size=14, color='#374151'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=True, 
            gridcolor='#e5e7eb',
            title_font=dict(size=14, color='#6b7280'),
            tickfont=dict(size=12, color='#6b7280')
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor='#e5e7eb',
            title_font=dict(size=14, color='#6b7280'),
            tickfont=dict(size=12, color='#6b7280')
        ),
        legend=dict(
            title='',
            orientation='h',
            y=-0.15,
            x=0.5,
            xanchor='center',
            font=dict(size=12, color='#374151')
        ),
        margin=dict(l=20, r=20, t=60, b=80),
        hovermode='x unified'
    )
    
    # Add gradient fills
    for i, trace in enumerate(fig.data):
        trace.update(fill='tonexty' if i > 0 else 'tozeroy')
        trace.update(line=dict(width=2))
    
    return fig

def create_advanced_pie_chart(df):
    """Modern pie chart with enhanced styling and animations"""
    fig = px.pie(
        df,
        names='Category',
        values='Amount',
        template='plotly_white',
        color_discrete_sequence=COLOR_SEQ
    )
    
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        marker=dict(
            line=dict(color='#ffffff', width=2),
            opacity=0.9
        ),
        hovertemplate='<b>%{label}</b><br>Amount: $%{value:,.2f}<br>Percentage: %{percent}<extra></extra>'
    )
    
    fig.update_layout(
        title=dict(
            text='🥧 Expense Distribution',
            font=dict(size=20, color='#1f2937'),
            x=0.5
        ),
        font=dict(family='Inter, sans-serif', size=14, color='#374151'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=60, b=20),
        showlegend=True,
        legend=dict(
            orientation='v',
            yanchor='middle',
            y=0.5,
            xanchor='left',
            x=1.01,
            font=dict(size=12, color='#374151')
        )
    )
    
    return fig

def create_trend_chart(df):
    """Advanced trend analysis with moving averages"""
    if df.empty:
        return go.Figure()
    
    # Convert to datetime and sort
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    
    # Calculate daily totals
    daily_totals = df.groupby(['Date', 'Category'])['Amount'].sum().reset_index()
    
    fig = go.Figure()
    
    # Add trend lines for each category
    for i, category in enumerate(daily_totals['Category'].unique()):
        cat_data = daily_totals[daily_totals['Category'] == category]
        cat_data = cat_data.sort_values('Date')
        
        # Calculate 7-day moving average
        cat_data['MA7'] = cat_data['Amount'].rolling(window=7, min_periods=1).mean()
        
        fig.add_trace(go.Scatter(
            x=cat_data['Date'],
            y=cat_data['Amount'],
            mode='markers',
            name=f'{category} (Actual)',
            marker=dict(
                color=COLOR_SEQ[i % len(COLOR_SEQ)],
                size=6,
                opacity=0.7
            ),
            hovertemplate=f'<b>{category}</b><br>Date: %{{x}}<br>Amount: $%{{y:,.2f}}<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=cat_data['Date'],
            y=cat_data['MA7'],
            mode='lines',
            name=f'{category} (Trend)',
            line=dict(
                color=COLOR_SEQ[i % len(COLOR_SEQ)],
                width=3,
                dash='solid'
            ),
            hovertemplate=f'<b>{category} Trend</b><br>Date: %{{x}}<br>7-Day Avg: $%{{y:,.2f}}<extra></extra>'
        ))
    
    fig.update_layout(
        title=dict(
            text='📊 Advanced Trend Analysis',
            font=dict(size=20, color='#1f2937'),
            x=0.5
        ),
        font=dict(family='Inter, sans-serif', size=14, color='#374151'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=True,
            gridcolor='#e5e7eb',
            title='Date',
            title_font=dict(size=14, color='#6b7280')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#e5e7eb',
            title='Amount ($)',
            title_font=dict(size=14, color='#6b7280')
        ),
        legend=dict(
            orientation='v',
            yanchor='top',
            y=1,
            xanchor='left',
            x=1.01,
            font=dict(size=12, color='#374151')
        ),
        margin=dict(l=20, r=20, t=60, b=20),
        hovermode='x unified'
    )
    
    return fig

def create_comparison_chart(df):
    """Month-over-month comparison chart"""
    if df.empty:
        return go.Figure()
    
    # Convert to datetime and extract month-year
    df['Date'] = pd.to_datetime(df['Date'])
    df['MonthYear'] = df['Date'].dt.to_period('M')
    
    # Calculate monthly totals by category
    monthly_data = df.groupby(['MonthYear', 'Category'])['Amount'].sum().reset_index()
    
    # Pivot for comparison
    pivot_data = monthly_data.pivot(index='MonthYear', columns='Category', values='Amount').fillna(0)
    
    fig = go.Figure()
    
    for i, category in enumerate(pivot_data.columns):
        fig.add_trace(go.Bar(
            name=category,
            x=pivot_data.index.astype(str),
            y=pivot_data[category],
            marker_color=COLOR_SEQ[i % len(COLOR_SEQ)],
            hovertemplate=f'<b>{category}</b><br>Month: %{{x}}<br>Amount: $%{{y:,.2f}}<extra></extra>'
        ))
    
    fig.update_layout(
        title=dict(
            text='📊 Month-over-Month Comparison',
            font=dict(size=20, color='#1f2937'),
            x=0.5
        ),
        font=dict(family='Inter, sans-serif', size=14, color='#374151'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=True,
            gridcolor='#e5e7eb',
            title='Month',
            title_font=dict(size=14, color='#6b7280')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#e5e7eb',
            title='Amount ($)',
            title_font=dict(size=14, color='#6b7280')
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.2,
            xanchor='center',
            x=0.5,
            font=dict(size=12, color='#374151')
        ),
        margin=dict(l=20, r=20, t=60, b=80),
        barmode='group',
        hovermode='x unified'
    )
    
    return fig

