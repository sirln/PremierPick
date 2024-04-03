import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
from app.premier_selector import goalkeepers, defenders, midfielders, forwards

# Function to generate table from DataFrame
def generate_table_from_dataframe(df, title):
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
        html.H3(title),
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
            html.Div(id='graphs-container', className="mt-4"),
            dcc.Interval(
                id='interval-component',
                interval=1000,  # Update interval in milliseconds
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
        goalkeepers_df = pd.DataFrame([(p.name, p.form, p.points) for p in goalkeepers], columns=["Name", "Form", "Total Points"])
        defenders_df = pd.DataFrame([(p.name, p.form, p.points) for p in defenders], columns=["Name", "Form", "Total Points"])
        midfielders_df = pd.DataFrame([(p.name, p.form, p.points) for p in midfielders], columns=["Name", "Form", "Total Points"])
        forwards_df = pd.DataFrame([(p.name, p.form, p.points) for p in forwards], columns=["Name", "Form", "Total Points"])

        goalkeepers_table = generate_table_from_dataframe(goalkeepers_df, "Goalkeepers Form and Total Points")
        defenders_table = generate_table_from_dataframe(defenders_df, "Defenders Form and Total Points")
        midfielders_table = generate_table_from_dataframe(midfielders_df, "Midfielders Form and Total Points")
        forwards_table = generate_table_from_dataframe(forwards_df, "Forwards Form and Total Points")

        return dbc.Row([
            dbc.Col(goalkeepers_table, md=6),
            dbc.Col(forwards_table, md=6),
            dbc.Col(defenders_table, md=6),
            dbc.Col(midfielders_table, md=6),
        ])