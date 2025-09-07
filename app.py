import pandas as pd
from dash import Dash, dcc, html, Input, Output, State
import dash

from modules.charts import (
    create_area_chart,
    create_bar_chart,
    create_line_chart,
    create_pie_chart,
    create_funnel_chart
)
from modules.process_data import load_transactions, filter_by_category, insert_transaction

app = Dash(__name__)

# Initial data
df = load_transactions()

# ----- Shared styles -----
APP_STYLE = {
    'fontFamily': 'Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif',
    'backgroundColor': '#eef2f7',
    'padding': '20px'
}
CARD = {
    'backgroundColor': '#fff',
    'padding': '16px',
    'borderRadius': '12px',
    'boxShadow': '0 4px 12px rgba(0,0,0,0.08)'
}

def to_plot_columns(dframe: pd.DataFrame) -> pd.DataFrame:
    """Rename to the TitleCase columns expected by chart functions."""
    return dframe.rename(columns={'date': 'Date', 'amount': 'Amount', 'category': 'Category'})

app.layout = html.Div([
    html.H1(
        "Personal Finance Tracker",
        style={'textAlign': 'center', 'fontSize': 36, 'color': '#0a1f44', 'marginBottom': '24px'}
    ),

    # TOP ROW: Left and Right panels
    html.Div([
        # LEFT: Category 1 + Chart 1 (Area/Bar/Line)
        html.Div([
            html.Div([
                html.Label("Categories (Chart 1)", style={'fontWeight': 600}),
                dcc.Dropdown(
                    id='category-left',
                    options=[{'label': c, 'value': c} for c in df['category'].unique()],
                    value=list(df['category'].unique()),
                    multi=True,
                    style={'marginBottom': '12px'}
                ),
                html.Label("Chart Type (Left)", style={'fontWeight': 600}),
                dcc.Dropdown(
                    id='chart-type-left',
                    options=[
                        {'label': 'Area', 'value': 'area'},
                        {'label': 'Bar', 'value': 'bar'},
                        {'label': 'Line', 'value': 'line'}
                    ],
                    value='area',
                    clearable=False
                ),
            ], style=CARD),

            html.Div([
                dcc.Graph(id='chart-left', style={'height': '460px'})
            ], style={**CARD, 'marginTop': '16px'})
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),

        # RIGHT: Category 2 + Chart 2 (Pie/Funnel)
        html.Div([
            html.Div([
                html.Label("Categories (Chart 2)", style={'fontWeight': 600}),
                dcc.Dropdown(
                    id='category-right',
                    options=[{'label': c, 'value': c} for c in df['category'].unique()],
                    value=list(df['category'].unique()),
                    multi=True,
                    style={'marginBottom': '12px'}
                ),
                html.Label("Chart Type (Right)", style={'fontWeight': 600}),
                dcc.Dropdown(
                    id='chart-type-right',
                    options=[
                        {'label': 'Pie', 'value': 'pie'},
                        {'label': 'Funnel', 'value': 'funnel'}
                    ],
                    value='pie',
                    clearable=False
                ),
            ], style=CARD),

            html.Div([
                dcc.Graph(id='chart-right', style={'height': '460px'})
            ], style={**CARD, 'marginTop': '16px'})
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginLeft': '4%'})
    ], style={'width': '95%', 'margin': '0 auto'}),

    # BOTTOM ROW: Add Transaction (centered)
    html.Div([
        html.Div([
            html.H3("Add New Transaction", style={'fontSize': 20, 'marginTop': 0, 'marginBottom': 12}),
            dcc.Input(id='input-date', type='text', placeholder='YYYY-MM-DD', style={'marginBottom': '8px', 'width': '100%'}),
            dcc.Input(id='input-category', type='text', placeholder='Category', style={'marginBottom': '8px', 'width': '100%'}),
            dcc.Input(id='input-amount', type='number', placeholder='Amount', style={'marginBottom': '8px', 'width': '100%'}),
            dcc.Input(id='input-desc', type='text', placeholder='Description (optional)', style={'marginBottom': '12px', 'width': '100%'}),
            html.Button('Add Transaction', id='add-btn', n_clicks=0, style={'width': '100%', 'marginBottom': '8px'}),
            html.Div(id='form-output', style={'color': 'green'})
        ], style={**CARD, 'maxWidth': 480, 'width': '100%'})
    ], style={'display': 'flex', 'justifyContent': 'center', 'marginTop': '24px'})
], style=APP_STYLE)


# ----- Callbacks -----

# Add transaction: update both category dropdowns (options + selected values) after insert
@app.callback(
    Output('form-output', 'children'),
    Output('category-left', 'options'),
    Output('category-left', 'value'),
    Output('category-right', 'options'),
    Output('category-right', 'value'),
    Input('add-btn', 'n_clicks'),
    State('input-date', 'value'),
    State('input-category', 'value'),
    State('input-amount', 'value'),
    State('input-desc', 'value')
)
def add_transaction_callback(n_clicks, date, category, amount, desc):
    if n_clicks and n_clicks > 0 and date and category and amount is not None:
        try:
            insert_transaction(date, category, amount, desc)
            df_new = load_transactions()
            cats = list(df_new['category'].unique())
            opts = [{'label': c, 'value': c} for c in cats]
            return "Transaction added successfully!", opts, cats, opts, cats
        except Exception as e:
            return f"Error: {e}", dash.no_update, dash.no_update, dash.no_update, dash.no_update
    return "", dash.no_update, dash.no_update, dash.no_update, dash.no_update


# Update both charts independently
@app.callback(
    Output('chart-left', 'figure'),
    Output('chart-right', 'figure'),
    Input('category-left', 'value'),
    Input('chart-type-left', 'value'),
    Input('category-right', 'value'),
    Input('chart-type-right', 'value')
)
def update_charts(cat_left, type_left, cat_right, type_right):
    # Always load fresh data (so new inserts show up immediately)
    data = load_transactions()

    # LEFT
    df_left = filter_by_category(data, cat_left)
    plot_left = to_plot_columns(df_left)
    if type_left == 'area':
        fig_left = create_area_chart(plot_left)
    elif type_left == 'bar':
        fig_left = create_bar_chart(plot_left)
    else:
        fig_left = create_line_chart(plot_left)

    # RIGHT
    df_right = filter_by_category(data, cat_right)
    plot_right = to_plot_columns(df_right)
    if type_right == 'pie':
        fig_right = create_pie_chart(plot_right)
    else:
        fig_right = create_funnel_chart(plot_right)

    return fig_left, fig_right


if __name__ == '__main__':
    app.run(debug=True)
