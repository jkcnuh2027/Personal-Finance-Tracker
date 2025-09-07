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

# Modern blue palette
COLOR_SEQ = ['#1f77b4', '#1ca3ec', '#3fa7d6', '#4aa3f0', '#6bb9ff', '#89c5ff']

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

