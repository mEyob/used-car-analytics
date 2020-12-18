from app import app
from app import server
import pandas as pd
import data

# Dash imports
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# ---------------------------------------------------------------
# styling options
tab_style = {"color": "#b7d7e8"}

tab_selected_style = {
    "borderTop": "3px solid #87bdd8",
    "color": "#87bdd8",
    "fontWeight": "bold",
}

drop_down_style = {
    "color": "#588c7e",
    "background": "transparent",
    "border-color": "white"
}

drop_down_group_style = {
    "color": "white",
    "padding": "5px 25px 10px 25px",
    "background-color": "#b7d7e8",
    "border-radius": "10px"
}

# ----------------------------------------------------------------
# Get makes and models of cars
all_options = data.make_and_model()

# model years
years = list(range(2020, 2009, -1))
# ----------------------------------------------------------------
# App layout
app.layout = html.Div(
    style={"font-family": "Arial"},
    children=[
        html.H2("Used Car Listing Prices in the Boston Metropolitan",
                style={
                    'text-align': 'center',
                    'fontWeight': 'bold',
                    "color": "#87bdd8"
                }),
        dcc.Tabs(
            id="all-tabs-inline",
            className="all-tabs-inline",
            value="tab-1",
            children=[
                dcc.Tab(
                    label="Listing Price",
                    value="tab-1",
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                dcc.Tab(
                    label="Compare Listing Prices",
                    value="tab-2",
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                dcc.Tab(
                    label="Estimate Listing Price",
                    value="tab-3",
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                dcc.Tab(
                    label="About the dashboard",
                    value="tab-4",
                    style=tab_style,
                    selected_style=tab_selected_style,
                )
            ],
        ),
        html.Br(),
        html.Div(
            [
                html.Div([
                    html.H6(children=["Select vehicle"],
                            id="first_vehicle_title"),
                    dcc.Dropdown(id="slct_make",
                                 options=[{
                                     "label": make,
                                     "value": make
                                 } for make in all_options.keys()],
                                 multi=False,
                                 value="Toyota",
                                 placeholder="Select Make",
                                 style=drop_down_style),
                    dcc.Dropdown(id="slct_model",
                                 multi=False,
                                 value="Camry",
                                 placeholder="Select model",
                                 style={
                                     'margin-top': '10px',
                                     'margin-bottom': '10px',
                                     **drop_down_style
                                 }),
                    dcc.Dropdown(id="slct_year",
                                 options=[{
                                     "label": str(year),
                                     "value": year
                                 } for year in years],
                                 multi=False,
                                 placeholder="Select Year",
                                 style=drop_down_style),
                ],
                         style=drop_down_group_style),
                html.Br(),
                html.Div(
                    id="second-car",
                    children=[
                        html.H6("Vehicle 2", style={'margin-left': '5px'}),
                        dcc.Dropdown(id="slct_make2",
                                     options=[{
                                         "label": make,
                                         "value": make
                                     } for make in all_options.keys()],
                                     multi=False,
                                     value="Honda",
                                     placeholder="Select Make",
                                     style=drop_down_style),
                        dcc.Dropdown(id="slct_model2",
                                     multi=False,
                                     value="Accord",
                                     placeholder="Select model",
                                     style={
                                         'margin-top': '10px',
                                         'margin-bottom': '10px',
                                         **drop_down_style
                                     }),
                        dcc.Dropdown(
                            id="slct_year2",
                            options=[{
                                "label": str(year),
                                "value": year
                            } for year in years],
                            multi=False,
                            #value=2015,
                            placeholder="Select year",
                            style=drop_down_style),
                    ],
                    style={
                        **drop_down_group_style, "display": "none"
                    },
                )
            ],
            style={
                "display": "inline-block",
                "width": "15%",
            },
            className="six columns",
        ),
        html.Div([dcc.Graph(id='mileage_price_plot', figure={})],
                 id="chart-div",
                 style={
                     "display": "inline-block",
                     "width": "50%"
                 },
                 className="six columns"),
        html.Div(
            id="description-div",
            className="six columns",
            style={
                "display": "inline-block",
                #"background-color": "#b7d7e8",
                "color": "#8d9db6",
                "width": "20%",
                "padding": "10px",
                "border-radius": "5px"
            },
            children=[
                html.P("The second question and more of two more"),
                html.P("an observation is that is it possible"),
                html.P("to use directly the column names in"),
                html.P("Pandas dataframe function without"),
                html.P("enclosing them inside quotes? I"),
                html.P("understand that the variable names"),
                html.P("are string, so has to be inside quotes,"),
            ])
    ])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback([
    Output(component_id='mileage_price_plot', component_property='figure'),
    Output(component_id='second-car', component_property='style'),
    Output(component_id='first_vehicle_title', component_property='children')
], [
    Input(component_id='slct_make', component_property='value'),
    Input(component_id='slct_model', component_property='value'),
    Input(component_id='slct_year', component_property='value'),
    Input(component_id='slct_make2', component_property='value'),
    Input(component_id='slct_model2', component_property='value'),
    Input(component_id='slct_year2', component_property='value'),
    Input(component_id='all-tabs-inline', component_property='value')
])
def update_graph(make_selected, model_selected, year_selected, make_selected2,
                 model_selected2, year_selected2, tab):
    if tab == "tab-1":
        df = data.get_grouped_data(make_selected, model_selected,
                                   year_selected)
        fig = px.bar(
            data_frame=df,
            x="Mileage_range",
            y="Average_Price",
            hover_data=["Average_Price", "Count", "STD_Price"],
            error_y="STD_Price",
            #color_continuous_scale=px.colors.sequential.YlOrRd,
            labels={
                "STD_Price": "Standard deviation (USD)",
                "Average_Price": "Average Price ($)",
                "Mileage_range": "Mileage (miles)",
                "Count": "Sample size"
            },
            opacity=0.5)
        fig.update_traces(marker_color="#d64161")
        fig.layout.plot_bgcolor = "white"
        show_second_car = {**drop_down_group_style, 'display': 'none'}
        first_vehicle_title = "Select Vehicle"
    elif tab == "tab-2":
        df = data.get_grouped_data(make_selected,
                                   model_selected,
                                   year_selected,
                                   make2=make_selected2,
                                   model2=model_selected2,
                                   year2=year_selected2)
        # df = df[["MakeModel", "Mileage_range", "Average_Price"]]
        df.fillna(0, inplace=True)
        makemodel1, makemodel2 = df.MakeModel.unique().tolist()
        car1 = df[df["MakeModel"] == makemodel1]
        car2 = df[df["MakeModel"] == makemodel2]

        fig = go.Figure(data=[
            go.Bar(name=makemodel1,
                   x=car1.Mileage_range,
                   y=car1.Average_Price,
                   error_y=dict(array=car1.STD_Price.tolist()),
                   text=[f"Sample size: {cnt}" for cnt in car1.Count.tolist()],
                   hovertemplate='<br><i>Mileage Range</i>: %{x} miles<br>' +
                   '<i>Average Price</i>: $%{y}<br>' + '<i>%{text}</i>',
                   opacity=0.7),
            go.Bar(
                name=makemodel2,
                x=car2.Mileage_range,
                y=car2.Average_Price,
                error_y=dict(array=car2.STD_Price.tolist()),
                text=[f"Sample size: {cnt}" for cnt in car2.Count.tolist()],
                hovertemplate='<br><i>Mileage Range</i>: %{x} miles<br>' +
                '<i>Average Price</i>: $%{y}<br>' + '<i>%{text}</i>',
            )
        ])
        #fig.update_traces(marker_color="#d64161")
        fig.layout.plot_bgcolor = "white"
        fig.update_layout(barmode='group',
                          hoverlabel_align='right',
                          xaxis_title="Mileage (miles)",
                          yaxis_title="Average Price ($)",
                          title_text=f"{makemodel1} vs {makemodel2}",
                          title_x=0.5)
        show_second_car = {**drop_down_group_style, 'display': 'block'}
        first_vehicle_title = "Vehicle 1"
    elif tab == "tab-3":
        fig = None
        show_second_car = {**drop_down_group_style, 'display': 'none'}

    # Plotly Express

    return fig, show_second_car, first_vehicle_title


@app.callback(dash.dependencies.Output('slct_model', 'options'),
              [dash.dependencies.Input('slct_make', 'value')])
def update_models_dropdown(make):
    return [{'label': i, 'value': i} for i in all_options[make]]


@app.callback(dash.dependencies.Output('slct_model2', 'options'),
              [dash.dependencies.Input('slct_make2', 'value')])
def update_models2_dropdown(make):
    if make:
        return [{'label': i, 'value': i} for i in all_options[make]]


if __name__ == '__main__':
    app.run_server(debug=True)
