import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html, callback_context, ALL
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from app.player_stats_layout import load_player_stats
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
    df['Name'] = df['Name'].apply(lambda name: html.A(name, href=f"/player/{name}", id={'type': 'player-link', 'index': name}))

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
            dcc.Location(id='url', refresh=False),
            dbc.Row(
                dbc.Col(
                    html.H1("Premier Pick Dashboard", className="mt-4 text-center") 
                )
            ),
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
        [Input('interval-component', 'n_intervals'),
         Input('url', 'pathname')]
    )
    def update_layout(n, pathname):
        if pathname and pathname.startswith("/player/"):
            player_name = pathname.split("/player/")[-1]
            return load_player_stats(player_name)
        else:
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

    @app.callback(
        Output('url', 'pathname'),
        [Input({'type': 'player-link', 'index': ALL}, 'n_clicks')],
        [State({'type': 'player-link', 'index': ALL}, 'id')]
    )
    def navigate_to_player_dashboard(n_clicks, ids):
        ctx = callback_context
        if not ctx.triggered:
            raise PreventUpdate

        link_id = ctx.triggered[0]['prop_id'].split('.')[0]
        player_name = None
        for i, id_dict in enumerate(ids):
            if id_dict['type'] == 'player-link' and id_dict['index'] == link_id:
                player_name = ids[i]['index']
                break

        if player_name:
            return f"/player/{player_name}"
        else:
            raise PreventUpdate





# import pandas as pd
# import dash_bootstrap_components as dbc
# from dash import dcc, html, callback_context, ALL
# from dash.exceptions import PreventUpdate
# from dash.dependencies import Input, Output, State
# from app.player_stats_layout import load_player_stats
# from app.premier_selector import goalkeepers, defenders, midfielders, forwards

# background_color = 'darkgray'
# text_color = 'black' if background_color == 'darkgray' else 'white'
# title_style = {
#     'color': text_color,
#     'font-size': '1.2rem',
#     'font-family': 'Arial, sans-serif',
#     'display': 'flex',
#     'justify-content': 'center',
#     'align-items': 'center',
#     'margin-top': '30px',
# }

# # Function to generate table from DataFrame
# def generate_table_from_dataframe(df, title):
#     # Modify the DataFrame to make player names clickable
#     # df['Name'] = df['Name'].apply(lambda name: html.A(name, href=f"/player/{name}"))
#     df['Name'] = df['Name'].apply(lambda name: html.A(name, href=f"/player/{name}", id={'type': 'player-link', 'index': name}))

#     # Convert DataFrame to HTML table
#     table = dbc.Table.from_dataframe(
#         df,
#         striped=True,
#         bordered=True,
#         hover=True,
#         responsive=True,
#         className="mt-4"
#     )

#     return html.Div([
#         html.H3(title, style=title_style),
#         table
#     ])


# # Function to create the layout of your Dash app
# def create_dash_layout(app):
#     app.layout = dbc.Container(
#         [
#             dcc.Location(id='url', refresh=False),
#             dbc.Row(
#                 dbc.Col(
#                     html.H1("Premier Pick Dashboard", className="mt-4 text-center") 
#                 )
#             ),
#             html.Div(id='graphs-container', className="mt-4"),
#             dcc.Interval(
#                 id='interval-component',
#                 interval=300000,  # Update interval in milliseconds
#                 n_intervals=0
#             )
#         ],
#         fluid=True,
#     )

#     @app.callback(
#         Output('graphs-container', 'children'),
#         [Input('interval-component', 'n_intervals'),
#           Input('url', 'pathname')]
#     )
#     def update_layout(n, pathname):
#         if pathname and pathname.startswith("/player/"):
#             player_name = pathname.split("/player/")[-1]
#             return load_player_stats(player_name)
#         else:
#             # Convert player data to DataFrame
#             goalkeepers_df = pd.DataFrame([(p.name, p.form, p.points, (p.value/10)) for p in goalkeepers], columns=["Name", "Form", "Total Points", "Player Value"])
#             defenders_df = pd.DataFrame([(p.name, p.form, p.points, (p.value/10)) for p in defenders], columns=["Name", "Form", "Total Points", "Player Value"])
#             midfielders_df = pd.DataFrame([(p.name, p.form, p.points, (p.value/10)) for p in midfielders], columns=["Name", "Form", "Total Points", "Player Value"])
#             forwards_df = pd.DataFrame([(p.name, p.form, p.points, (p.value/10)) for p in forwards], columns=["Name", "Form", "Total Points", "Player Value"])

#             goalkeepers_table = generate_table_from_dataframe(goalkeepers_df, "Goalkeepers Form and Total Points")
#             defenders_table = generate_table_from_dataframe(defenders_df, "Defenders Form and Total Points")
#             midfielders_table = generate_table_from_dataframe(midfielders_df, "Midfielders Form and Total Points")
#             forwards_table = generate_table_from_dataframe(forwards_df, "Forwards Form and Total Points")

#             return html.Div([
#                 dbc.Row([
#                     dbc.Col(goalkeepers_table, md=6),
#                     dbc.Col(forwards_table, md=6),
#                 ], style={'margin-bottom': '20px', 'background-color': background_color}),
#                 dbc.Row([
#                     dbc.Col(defenders_table, md=6),
#                     dbc.Col(midfielders_table, md=6),
#                 ], style={'background-color': background_color}),
#             ])


#     # # Callback to update the URL when player name is clicked
#     # @app.callback(
#     #     Output('url', 'pathname'),
#     #     [Input({'type': 'player-link', 'index': ALL}, 'n_clicks')],
#     #     [State({'type': 'player-link', 'index': ALL}, 'id')]
#     # )
#     # def update_url(n_clicks, ids):
#     #     if callback_context.triggered:
#     #         # player_name = callback_context.triggered[0]['prop_id'].split('.')[0]['index']
#     #         player_name = callback_context.triggered[0]['prop_id'].split('.')[0]
#     #         return f"/player/{player_name}"
#     #     else:
#     #         raise PreventUpdate  