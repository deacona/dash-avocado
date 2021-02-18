import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
import plotly.graph_objects as go

data = pd.read_csv("avocado.csv")
# data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
# data.sort_values("Date", inplace=True)
overall_score = data.AveragePrice.mean()
range_max = data.AveragePrice.max()

fig = go.Figure(
    # go.Indicator(
    # mode = "gauge+number",
    # value = overall_score,
    # domain = {'x': [0, 0.5], 'y': [0, 1]},
    # title = {'text': "Overall Average"},
    # gauge = {'axis': {'range': [None, data.AveragePrice.max()]},
    #         #  'steps' : [
    #         #      {'range': [0, 250], 'color': "lightgray"},
    #         #      {'range': [250, 400], 'color': "gray"}],
    #          'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': overall_score}}
    # )
    )

# fig.add_trace(go.Indicator(
#     mode = "number+gauge+delta", 
#     value = overall_score,
#     # delta = {'reference': 200},
#     domain = {'x': [0.2, 1],},# 'y': [0.9, 1.0]},
#     title = {'text' :"Overall"},
#     gauge = {
#         'shape': "bullet",
#         'axis': {'range': [None, data.AveragePrice.max()]},
#         'threshold': {
#             'line': {'color': "black", 'width': 2},
#             'thickness': 0.75,
#             'value': overall_score},
#         # 'steps': [
#         #     {'range': [0, 150], 'color': "gray"},
#         #     {'range': [150, 250], 'color': "lightgray"}],
#         'bar': {'color': "black"}}))
# fig.update_layout(height = 400 , margin = {'t':0, 'b':0, 'l':0})

for j, avtype in enumerate(data.type.unique()):
    # x_divisor = len(data.type.unique()) + 1
    x1 = (0.5 * j) #+ 0.2 # (i * (1 / y_divisor))
    x2 = 0.5 * (1 + j) # (1 - (i * (1 / y_divisor))) - 0.1

    for i, year in enumerate(data.year.unique()):
        y_divisor = len(data.year.unique()) + 1
        y2 = 1 - (i * (1 / y_divisor))
        y1 = (1 - (i * (1 / y_divisor))) - 0.1
        # print(i, avtype, year, x1, x2, y1, y2)

        fig.add_trace(go.Indicator(
            mode = "number+gauge+delta", 
            value = data[(data.year == year) & (data.type == avtype)].AveragePrice.mean(),
            delta = {'reference': overall_score},
            domain = {'x': [x1, x2], 'y': [y1, y2]},
            # title = {'text' :str(year)},
            gauge = {
                'shape': "bullet",
                'axis': {'range': [None, range_max]},
                'threshold': {
                    'line': {'color': "black", 'width': 2},
                    'thickness': 0.75,
                    'value': overall_score},
                'steps': [
                    {'range': [0, 2], 'color': "gray"},
                    {'range': [2, 3], 'color': "lightgray"}],
                'bar': {'color': "black"}}))

# external_stylesheets = [
#     {
#         "href": "https://fonts.googleapis.com/css2?"
#         "family=Lato:wght@400;700&display=swap",
#         "rel": "stylesheet",
#     },
# ]
app = dash.Dash(__name__) #, external_stylesheets=external_stylesheets)
app.title = "Avocado Analytics: Understand Your Avocados!"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🥑", className="header-emoji"),
                html.H1(
                    children="Avocado Analytics", className="header-title"
                ),
                html.P(
                    children="Analyze the behavior of avocado prices"
                    " and the number of avocados sold in the US"
                    " between 2015 and 2018",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        # html.Div(
        #     children=[
        #         html.Div(
        #             children=[
        #                 html.Div(children="Region", className="menu-title"),
        #                 dcc.Dropdown(
        #                     id="region-filter",
        #                     options=[
        #                         {"label": region, "value": region}
        #                         for region in np.sort(data.region.unique())
        #                     ],
        #                     value=["Albany"],
        #                     clearable=True,
        #                     searchable=True,
        #                     className="dropdown",
        #                     multi=True,
        #                 ),
        #             ]
        #         ),
        #         html.Div(
        #             children=[
        #                 html.Div(children="Type", className="menu-title"),
        #                 dcc.Dropdown(
        #                     id="type-filter",
        #                     options=[
        #                         {"label": avocado_type, "value": avocado_type}
        #                         for avocado_type in data.type.unique()
        #                     ],
        #                     value=data.type.unique(),
        #                     clearable=True,
        #                     searchable=False,
        #                     className="dropdown",
        #                     multi=True,
        #                 ),
        #             ],
        #         ),
        #         html.Div(
        #             children=[
        #                 html.Div(children="Year", className="menu-title"),
        #                 dcc.Dropdown(
        #                     id="year-filter",
        #                     options=[
        #                         {"label": year, "value": year}
        #                         for year in data.year.unique()
        #                     ],
        #                     value="2017",
        #                     clearable=True,
        #                     searchable=False,
        #                     className="dropdown",
        #                 ),
        #             ],
        #         ),
        #     ],
        #     className="menu",
        # ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(id="price_bulletts", figure=fig),
                    className="card",
                ),
                # html.Div(
                #     children=dcc.Graph(
                #         id="price-chart", config={"displayModeBar": False},
                #     ),
                #     className="card",
                # ),
                # html.Div(
                #     children=dcc.Graph(
                #         id="volume-chart", config={"displayModeBar": False},
                #     ),
                #     className="card",
                # ),
            ],
            className="wrapper",
        ),
    ]
)


# @app.callback(
    # [Output("price-chart", "figure")], # Output("volume-chart", "figure")],
    # [
    #     Input("region-filter", "value"),
    #     Input("type-filter", "value"),
    #     Input("year-filter", "value"),
    # ],
# )
# def update_charts(region, avocado_type, year):
#     mask = (
#         (data.region.isin(region))
#         & (data.type.isin(avocado_type))
#         & (data.year == year)
#     )
#     filtered_data = data.loc[mask, :]
#     price_chart_figure = {
#         "data": [
#             {
#                 "x": filtered_data["Date"],
#                 "y": filtered_data["AveragePrice"],
#                 "type": "lines",
#                 "hovertemplate": "$%{y:.2f}<extra></extra>",
#             },
#         ],
#         "layout": {
#             "title": {
#                 "text": "Average Price of Avocados",
#                 "x": 0.05,
#                 "xanchor": "left",
#             },
#             "xaxis": {"fixedrange": True},
#             "yaxis": {"tickprefix": "$", "fixedrange": True},
#             "colorway": ["#17B897"],
#         },
#     }

    # volume_chart_figure = {
    #     "data": [
    #         {
    #             "x": filtered_data["Date"],
    #             "y": filtered_data["Total Volume"],
    #             "type": "lines",
    #         },
    #     ],
    #     "layout": {
    #         "title": {"text": "Avocados Sold", "x": 0.05, "xanchor": "left"},
    #         "xaxis": {"fixedrange": True},
    #         "yaxis": {"fixedrange": True},
    #         "colorway": ["#E12D39"],
    #     },
    # }
    # return price_chart_figure, #volume_chart_figure


if __name__ == "__main__":
    app.run_server(debug=True)