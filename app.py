import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.graph_objects as go

data = pd.read_csv("avocado.csv")
overall_score = data.AveragePrice.mean()
range_max = data.AveragePrice.max()

data_pivot = pd.pivot_table(data, values="AveragePrice", index="year", columns="type", aggfunc=np.mean, margins=False)
# print(data_pivot)

fig = go.Figure(data=go.Heatmap(
        z=data_pivot.values,
        x=data_pivot.columns,
        y=data_pivot.index,
        colorscale='Viridis',
        colorbar=dict(title="<b>Average Price</b>")
        )
        )

fig.update_layout(
    # title='Average price by year and type',
    xaxis=dict(
        title="<b>Avocado Type</b>"
    ),
    yaxis=dict(
        title="<b>Year</b>", autorange='reversed'
    ),
    )

fig.update_xaxes(side="top")

# fig.write_image("assets/dashboard.png")

app = dash.Dash(__name__)
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
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(id="price_heatmap", figure=fig),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)