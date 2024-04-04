import requests
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
from app.premier_selector import goalkeepers, defenders, midfielders, forwards

background_color = 'darkgray'
text_color = 'black' if background_color == 'darkgray' else 'white'
title_style = {
    'color': text_color,
    'font-size': '1.2rem',
    'font-family': 'Arial, sans-serif',
    'display': 'flex',
    'justify-content': 'center',
    'align-items': 'center',
    'margin-top': '30px',
}

# Function to generate table from DataFrame
def generate_table_from_dataframe(df, title):
    # Modify the DataFrame to make player names clickable
    df['Name'] = df['Name'].apply(lambda name: html.A(name, href=f"/player/{name}"))

    # Convert DataFrame to HTML table
    table = dbc.Table.from_dataframe(
        df,
        striped=True,
        bordered=True,
        hover=True,
        responsive=True,
        className="mt-4"
    )

    return html.Div([
        html.H3(title, style=title_style),
        table
    ])


# Function to create the layout of your Dash app
def create_dash_layout(app):
    app.layout = dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    html.H1("Premier Pick Dashboard", className="mt-4 text-center") 
                )
            ),
            dcc.Location(id='url', refresh=False),
            html.Div(id='page-content', className="mt-4"),
            html.Div(id='graphs-container', className="mt-4"),
            dcc.Interval(
                id='interval-component',
                interval=300000,  # Update interval in milliseconds
                n_intervals=0
            )
        ],
        fluid=True,
    )

    @app.callback(
        Output('graphs-container', 'children'),
        [Input('interval-component', 'n_intervals')]
    )
    def update_layout(n):
        print("Callback triggered with n_intervals:", n)
        # Convert player data to DataFrame
        goalkeepers_df = pd.DataFrame([(p.name, p.form, p.points, (p.value/10)) for p in goalkeepers], columns=["Name", "Form", "Total Points", "Player Value"])
        defenders_df = pd.DataFrame([(p.name, p.form, p.points, (p.value/10)) for p in defenders], columns=["Name", "Form", "Total Points", "Player Value"])
        midfielders_df = pd.DataFrame([(p.name, p.form, p.points, (p.value/10)) for p in midfielders], columns=["Name", "Form", "Total Points", "Player Value"])
        forwards_df = pd.DataFrame([(p.name, p.form, p.points, (p.value/10)) for p in forwards], columns=["Name", "Form", "Total Points", "Player Value"])

        goalkeepers_table = generate_table_from_dataframe(goalkeepers_df, "Goalkeepers Form and Total Points")
        defenders_table = generate_table_from_dataframe(defenders_df, "Defenders Form and Total Points")
        midfielders_table = generate_table_from_dataframe(midfielders_df, "Midfielders Form and Total Points")
        forwards_table = generate_table_from_dataframe(forwards_df, "Forwards Form and Total Points")

        return html.Div([
            dbc.Row([
                dbc.Col(goalkeepers_table, md=6),
                dbc.Col(forwards_table, md=6),
            ], style={'margin-bottom': '20px', 'background-color': background_color}),
            dbc.Row([
                dbc.Col(defenders_table, md=6),
                dbc.Col(midfielders_table, md=6),
            ], style={'background-color': background_color}),
        ])