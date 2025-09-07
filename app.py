import pandas as pd
from dash import Dash, dcc, html, Input, Output
from modules.charts import (
    create_area_chart,
    create_pie_chart,
    create_bar_chart,
    create_line_chart,
    create_funnel_chart
)
from modules.process_data import load_transactions, filter_by_category

# Load data
df = load_transactions("data/transactions.csv")

app = Dash(__name__)

# Global styles
APP_STYLE = {
    'fontFamily': 'Inter, sans-serif',
    'backgroundColor': '#eef2f7',
    'padding': '20px'
}

CARD_STYLE = {
    'backgroundColor': 'white',
    'padding': '20px',
    'borderRadius': '12px',
    'boxShadow': '0 4px 12px rgba(0,0,0,0.1)',
    'marginBottom': '20px'
}

app.layout = html.Div([
    html.H1(
        "Personal Finance Tracker",
        style={'textAlign': 'center', 'fontSize': '36px', 'marginBottom': '40px', 'color': '#0a1f44'}
    ),

    html.Div([
        # Left panel
        html.Div([
            html.Div([
                html.Label("Select left chart type:", style={'fontSize': '16px', 'marginBottom': '5px'}),
                dcc.Dropdown(
                    id='chart-type-dropdown',
                    options=[
                        {'label': 'Area', 'value': 'area'},
                        {'label': 'Bar', 'value': 'bar'},
                        {'label': 'Line', 'value': 'line'}
                    ],
                    value='area',
                    clearable=False,
                    style={'marginBottom': '15px'}
                ),
                html.Label("Select categories:", style={'fontSize': '16px', 'marginBottom': '5px'}),
                dcc.Dropdown(
                    id='category-dropdown',
                    options=[{'label': c, 'value': c} for c in df['Category'].unique()],
                    value=list(df['Category'].unique()),
                    multi=True,
                    style={'marginBottom': '15px'}
                )
            ], style=CARD_STYLE),
            html.Div([
                dcc.Graph(id='expense-chart', style={'height': '500px'})
            ], style=CARD_STYLE)
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),

        # Right panel
        html.Div([
            html.Div([
                html.Label("Select right chart type:", style={'fontSize': '16px', 'marginBottom': '5px'}),
                dcc.Dropdown(
                    id='chart2-type-dropdown',
                    options=[
                        {'label': 'Pie', 'value': 'pie'},
                        {'label': 'Funnel', 'value': 'funnel'}
                    ],
                    value='pie',
                    clearable=False
                )
            ], style=CARD_STYLE),
            html.Div([
                dcc.Graph(id='expense-pie-chart', style={'height': '500px'})
            ], style=CARD_STYLE)
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginLeft': '4%'})
    ], style={'width': '95%', 'margin': 'auto'})
], style=APP_STYLE)


@app.callback(
    Output('expense-chart', 'figure'),
    Output('expense-pie-chart', 'figure'),
    Input('category-dropdown', 'value'),
    Input('chart-type-dropdown', 'value'),
    Input('chart2-type-dropdown', 'value')
)
def update_charts(selected_categories, selected_chart_type, selected_chart2_type):
    filtered_df = filter_by_category(df, selected_categories)

    # Left chart
    if selected_chart_type == 'area':
        fig1 = create_area_chart(filtered_df)
    elif selected_chart_type == 'bar':
        fig1 = create_bar_chart(filtered_df)
    elif selected_chart_type == 'line':
        fig1 = create_line_chart(filtered_df)
    else:
        fig1 = create_area_chart(filtered_df)

    # Right chart
    if selected_chart2_type == 'pie':
        fig2 = create_pie_chart(filtered_df)
    elif selected_chart2_type == 'funnel':
        fig2 = create_funnel_chart(filtered_df)
    else:
        fig2 = create_pie_chart(filtered_df)

    return fig1, fig2


if __name__ == '__main__':
    app.run(debug=True)
