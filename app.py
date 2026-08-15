import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from tkinter import Tk
from tkinter.filedialog import askopenfilename

Tk().withdraw()
file_path = askopenfilename()

if file_path == "":
    print("No file selected")
    exit()

df = pd.read_csv(file_path, encoding="utf-8-sig", on_bad_lines="skip")

df.columns = df.columns.str.strip()
df["Country"] = df["Country"].astype(str).str.strip()
df["City"] = df["City"].astype(str).str.strip()

numeric_cols = [
    "AQI Value",
    "CO AQI Value",
    "Ozone AQI Value",
    "NO2 AQI Value",
    "PM2.5 AQI Value"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=["Country", "City", "AQI Value", "PM2.5 AQI Value"])
df.to_csv("cleaned_air_quality.csv", index=False)

countries = sorted(df["Country"].unique())
metrics = ["AQI Value", "CO AQI Value", "Ozone AQI Value", "NO2 AQI Value", "PM2.5 AQI Value"]

app = Dash(__name__)

app.layout = html.Div(
    style={"fontFamily": "Arial", "padding": "20px", "backgroundColor": "#f5f7fa"},
    children=[
        html.H1(
            "Air Quality and Pollution Dashboard",
            style={"textAlign": "center"}
        ),

        html.P(
            "Interactive dashboard for analyzing air quality indicators across countries and cities.",
            style={"textAlign": "center"}
        ),

        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "1fr 1fr 1fr",
                "gap": "15px",
                "backgroundColor": "white",
                "padding": "15px",
                "borderRadius": "10px"
            },
            children=[
                html.Div([
                    html.Label("Select Country"),
                    dcc.Dropdown(
                        options=[{"label": c, "value": c} for c in countries],
                        value=countries[0],
                        id="country-dropdown"
                    )
                ]),

                html.Div([
                    html.Label("Select Metric"),
                    dcc.RadioItems(
                        options=[{"label": m, "value": m} for m in metrics],
                        value="AQI Value",
                        id="metric-radio"
                    )
                ]),

                html.Div([
                    html.Label("Number of Cities"),
                    dcc.Slider(
                        min=5,
                        max=50,
                        step=5,
                        value=20,
                        marks={i: str(i) for i in range(5, 51, 10)},
                        id="top-slider"
                    )
                ])
            ]
        ),

        dcc.Graph(id="column-chart"),
        dcc.Graph(id="bar-chart"),
        dcc.Graph(id="stacked-column-chart"),
        dcc.Graph(id="stacked-bar-chart"),
        dcc.Graph(id="clustered-column-chart"),
        dcc.Graph(id="clustered-bar-chart"),
        dcc.Graph(id="scatter-chart"),
        dcc.Graph(id="bubble-chart"),
        dcc.Graph(id="histogram-chart"),
        dcc.Graph(id="box-chart"),
        dcc.Graph(id="violin-chart"),
        dcc.Graph(id="line-chart"),
        dcc.Graph(id="area-chart")
    ]
)


@app.callback(
    Output("column-chart", "figure"),
    Output("bar-chart", "figure"),
    Output("stacked-column-chart", "figure"),
    Output("stacked-bar-chart", "figure"),
    Output("clustered-column-chart", "figure"),
    Output("clustered-bar-chart", "figure"),
    Output("scatter-chart", "figure"),
    Output("bubble-chart", "figure"),
    Output("histogram-chart", "figure"),
    Output("box-chart", "figure"),
    Output("violin-chart", "figure"),
    Output("line-chart", "figure"),
    Output("area-chart", "figure"),
    Input("country-dropdown", "value"),
    Input("metric-radio", "value"),
    Input("top-slider", "value")
)
def update_charts(selected_country, selected_metric, top_n):
    filtered_df = df[df["Country"] == selected_country].copy()
    filtered_df = filtered_df.dropna(subset=[selected_metric])
    filtered_df = filtered_df.sort_values(selected_metric, ascending=False).head(top_n)
    filtered_df["Rank"] = range(1, len(filtered_df) + 1)

    column_fig = px.bar(
        filtered_df,
        x="City",
        y=selected_metric,
        title=f"Column Chart: Top Cities by {selected_metric} in {selected_country}",
        color=selected_metric
    )

    bar_fig = px.bar(
        filtered_df,
        x=selected_metric,
        y="City",
        orientation="h",
        title=f"Bar Chart: {selected_metric} by City in {selected_country}",
        color=selected_metric
    )

    stacked_column_fig = px.bar(
        filtered_df,
        x="City",
        y=selected_metric,
        color="AQI Category",
        title=f"Stacked Column Chart: {selected_metric} by AQI Category"
    )

    stacked_bar_fig = px.bar(
        filtered_df,
        x=selected_metric,
        y="City",
        color="AQI Category",
        orientation="h",
        title=f"Stacked Bar Chart: {selected_metric} by AQI Category"
    )

    clustered_column_fig = px.bar(
        filtered_df,
        x="City",
        y=selected_metric,
        color="AQI Category",
        barmode="group",
        title=f"Clustered Column Chart: {selected_metric} by Category"
    )

    clustered_bar_fig = px.bar(
        filtered_df,
        x=selected_metric,
        y="City",
        color="AQI Category",
        orientation="h",
        barmode="group",
        title=f"Clustered Bar Chart: {selected_metric} by Category"
    )

    scatter_fig = px.scatter(
        filtered_df,
        x="PM2.5 AQI Value",
        y="AQI Value",
        color="AQI Category",
        title=f"Scatter Chart: PM2.5 AQI vs Overall AQI in {selected_country}"
    )

    bubble_fig = px.scatter(
        filtered_df,
        x="PM2.5 AQI Value",
        y="AQI Value",
        size=selected_metric,
        color="AQI Category",
        hover_name="City",
        title=f"Bubble Chart: Pollution Relationship in {selected_country}"
    )

    histogram_fig = px.histogram(
        filtered_df,
        x=selected_metric,
        nbins=15,
        title=f"Histogram: Distribution of {selected_metric}"
    )

    box_fig = px.box(
        filtered_df,
        y=selected_metric,
        title=f"Box Chart: Spread of {selected_metric}"
    )

    violin_fig = px.violin(
        filtered_df,
        y=selected_metric,
        box=True,
        title=f"Violin Chart: Density of {selected_metric}"
    )

    line_fig = px.line(
        filtered_df,
        x="Rank",
        y=selected_metric,
        markers=True,
        title=f"Line Chart: {selected_metric} Trend by City Rank"
    )

    area_fig = px.area(
        filtered_df,
        x="Rank",
        y=selected_metric,
        title=f"Area Chart: Accumulated View of {selected_metric}"
    )

    return (
        column_fig,
        bar_fig,
        stacked_column_fig,
        stacked_bar_fig,
        clustered_column_fig,
        clustered_bar_fig,
        scatter_fig,
        bubble_fig,
        histogram_fig,
        box_fig,
        violin_fig,
        line_fig,
        area_fig
    )


if __name__ == "__main__":
    app.run(debug=False)