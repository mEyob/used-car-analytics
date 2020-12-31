from app import app
from app import server
import pandas as pd
import numpy as np
import data
import estimate
import styles
import helper
import data


# Dash imports
import dash
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# ---------------------------------------------------------------
# styling options
tab_style = {
    "color": "#b7d7e8",
    "borderTopLeftRadius": "3px",
    "borderTopRightRadius": "3px",
    "borderTop": "3px solid transparent",
    "borderLeft": "0px",
    "borderRight": "0px",
    "borderBottom": "0px",
    "backgroundColor": "#fafbfc",
    "padding": "12px",
    "fontFamily": "system-ui",
    "display": "flex",
    "align-items": "center",
    "justify-content": "center",
}

tab_selected_style = {
    "borderTop": "3px solid #87bdd8",
    "boxShadow": "1px 1px 0px white",
    "borderLeft": "1px solid lightgrey",
    "borderRight": "1px solid lightgrey",
    "color": "#87bdd8",
    "fontWeight": "bold",
}

tab_group_style = {
    "borderTopLeftRadius": "3px",
    "backgroundColor": "#f9f9f9",
    "padding": "0px 24px",
    "border-bottom": "1px solid #d6d6d6",
    "width": "85%"
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
    "border-radius": "5px",
    "border-color": "#6e7575",
    "border-width": "1px",
    "border-style": "solid",
}

description_box_style = {
    "color": "#8d9db6",
    "width": "25%",
    "padding": "10px",
    "border-radius": "5px"
}

# ----------------------------------------------------------------
# Get makes and models of cars
all_options = data.make_and_model()
manufacturers = sorted(all_options.keys())

# model years
years = list(range(2020, 2009, -1))
# ----------------------------------------------------------------
# App layout
app.layout = html.Div(
    style=styles.dashboard_style,
    children=[
        html.H2("Used Car Listing Prices in the Boston Metropolitan",
                style={
                    "text-align": "center",
                    "fontWeight": "bold",
                    "color": "#87bdd8"
                }),
        dcc.Tabs(
            id="all-tabs-inline",
            style=styles.tab_group_style,
            children=[
                dcc.Tab(
                    label="Listing Price",
                    value="tab-1",
                    style=styles.tab_style,
                    selected_style=styles.tab_selected_style,
                ),
                dcc.Tab(
                    label="Compare Listing Prices",
                    value="tab-2",
                    style=styles.tab_style,
                    selected_style=styles.tab_selected_style,
                ),
                dcc.Tab(
                    label="Estimate Listing Price",
                    value="tab-3",
                    style=styles.tab_style,
                    selected_style=styles.tab_selected_style,
                ),
                dcc.Tab(
                    label="About the dashboard",
                    value="tab-4",
                    style=styles.tab_style,
                    selected_style=styles.tab_selected_style,
                )
            ],
        ),
        html.Br(),
        html.Br(),
        html.Div(
            [
                html.Div(id="first-car",
                         children=[
                             html.H6(children=["Select vehicle"],
                                     id="first_vehicle_title"),
                             dcc.Dropdown(id="slct_make",
                                          options=[{
                                              "label": make,
                                              "value": make
                                          } for make in manufacturers],
                                          multi=False,
                                          value="Toyota",
                                          placeholder="Select Make",
                                          style=styles.drop_down_style),
                             dcc.Dropdown(id="slct_model",
                                          multi=False,
                                          value="Camry",
                                          placeholder="Select model",
                                          style={
                                              "margin-top": "10px",
                                              "margin-bottom": "10px",
                                              **styles.drop_down_style
                                          }),
                             dcc.Dropdown(id="slct_year",
                                          options=[{
                                              "label": str(year),
                                              "value": year
                                          } for year in years],
                                          multi=False,
                                          placeholder="Select Year",
                                          style=drop_down_style),
                             dcc.Input(id="input_mileage",
                                       type="number",
                                       placeholder="Enter Mileage",
                                       style={
                                           "margin-top": "10px",
                                           "display": "none",
                                           **styles.drop_down_style
                                       }),
                         ],
                         style=styles.drop_down_group_style),
                html.Br(),
                html.Div(
                    id="second-car",
                    children=[
                        html.H6("Vehicle 2", style={"margin-left": "5px"}),
                        dcc.Dropdown(id="slct_make2",
                                     options=[{
                                         "label": make,
                                         "value": make
                                     } for make in manufacturers],
                                     multi=False,
                                     value="Honda",
                                     placeholder="Select Make",
                                     style=styles.drop_down_style),
                        dcc.Dropdown(id="slct_model2",
                                     multi=False,
                                     value="Accord",
                                     placeholder="Select model",
                                     style={
                                         "margin-top": "10px",
                                         "margin-bottom": "10px",
                                         **styles.drop_down_style
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
                            style=styles.drop_down_style),
                    ],
                    style={
                        **styles.drop_down_group_style, "display": "none"
                    },
                )
            ],
            style=styles.input_group_style,
            className="six columns",
        ),
        html.Div(id="graph-div",
                 children=[dcc.Graph(id="mileage_price_plot", figure={})],
                 style={
                     "display": "none",
                     "width": "50%"
                 },
                 className="six columns"),
        html.Div(id="description-div",
                 className="six columns",
                 style={
                     "display": "none",
                     **styles.description_box_style
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
    Output(component_id="graph-div", component_property="style"),
    Output(component_id="description-div", component_property="style"),
    Output(component_id="description-div", component_property="children"),
    Output(component_id="mileage_price_plot", component_property="figure"),
    Output(component_id="first-car", component_property="style"),
    Output(component_id="second-car", component_property="style"),
    Output(component_id="first_vehicle_title", component_property="children"),
    Output(component_id="input_mileage", component_property="style")
], [
    Input(component_id="slct_make", component_property="value"),
    Input(component_id="slct_model", component_property="value"),
    Input(component_id="slct_year", component_property="value"),
    Input(component_id="input_mileage", component_property="value"),
    Input(component_id="slct_make2", component_property="value"),
    Input(component_id="slct_model2", component_property="value"),
    Input(component_id="slct_year2", component_property="value"),
    Input(component_id="all-tabs-inline", component_property="value")
])
def update_graph(make_selected, model_selected, year_selected,
                 trim_selected, mileage_selected, make_selected2, 
                 model_selected2,year_selected2, tab):
    show_first_car = {**styles.drop_down_group_style, "display": "block"}
    show_second_car = {**styles.drop_down_group_style, "display": "none"}
    show_graph = {"display": "none"}
    description = html.P()
    show_description = {"display": "none", **styles.description_box_style}
    mileage_box = {**styles.drop_down_style, "display": "none"}
    trim_box = {**styles.drop_down_style, "display": "none"}
    first_vehicle_title = "Select Vehicle"
    fig = go.Figure()

    if tab == "tab-1":
        if make_selected and model_selected:
            car = " ".join(
                [str(year_selected or ""), make_selected, model_selected])
            df = data.get_grouped_data(make_selected, model_selected,
                                       year_selected)
            fig = go.Figure(
                go.Bar(
                    name="",
                    x=df.Mileage_range,
                    y=df.Average_Price,
                    error_y=dict(array=df.STD_Price.tolist()),
                    marker=dict(color="#d64161"),
                    text=[f"Sample size: {cnt}" for cnt in df.Count.tolist()],
                    hovertemplate="<br><i>Mileage Range</i>: %{x} miles<br>" +
                    "<i>Average Price</i>: $%{y}<br>" + "<i>%{text}</i>",
                    opacity=0.6))
            #fig.update_traces(marker_color="#d64161")
            fig.layout.plot_bgcolor = "#f9f9f9"
            fig.update_layout(hoverlabel_align="right",
                              xaxis_title="Mileage (miles)",
                              yaxis_title="Average Price ($)",
                              title_text=f"{car} Listing Price",
                              title_x=0.5)
            desc = generate_description(df, "#d64161", make_selected,
                                        model_selected, year_selected)
            if desc:
                description = html.P(children=[
                    html.Ul(children=[
                        desc,
                        html.Li(
                            html.Font(
                                "Hover over the bars to check the sample size. Larger sample size has a higher chance of yielding accurate statistics"
                            ))
                    ])
                ])
                show_description["display"] = "inline-block"
            show_graph["display"] = "block"

    elif tab == "tab-2":
        if all(
            [make_selected, model_selected, make_selected2, model_selected2]):
            df = data.get_grouped_data(make_selected,
                                       model_selected,
                                       year_selected,
                                       make2=make_selected2,
                                       model2=model_selected2,
                                       year2=year_selected2)
            # df = df[["MakeModel", "Mileage_range", "Average_Price"]]
            #df.fillna(0, inplace=True)
            try:
                makemodel1, makemodel2 = df.MakeModel.unique().tolist()
            except ValueError:
                makemodel1 = df.MakeModel.unique().tolist()[0]
                makemodel2 = makemodel1
            car1 = df[df["MakeModel"] == makemodel1]
            car2 = df[df["MakeModel"] == makemodel2]

            fig = go.Figure(data=[
                go.Bar(
                    name=makemodel1,
                    x=car1.Mileage_range,
                    y=car1.Average_Price,
                    error_y=dict(array=car1.STD_Price.tolist()),
                    marker=dict(color="rgb(82,188,163)"),
                    text=[
                        f"Sample size: {cnt}" for cnt in car1.Count.tolist()
                    ],
                    hovertemplate="<br><i>Mileage Range</i>: %{x} miles<br>" +
                    "<i>Average Price</i>: $%{y}<br>" + "<i>%{text}</i>",
                    opacity=0.7),
                go.Bar(
                    name=makemodel2,
                    x=car2.Mileage_range,
                    y=car2.Average_Price,
                    error_y=dict(array=car2.STD_Price.tolist()),
                    marker=dict(color="#d64161"),
                    text=[
                        f"Sample size: {cnt}" for cnt in car2.Count.tolist()
                    ],
                    hovertemplate="<br><i>Mileage Range</i>: %{x} miles<br>" +
                    "<i>Average Price</i>: $%{y}<br>" + "<i>%{text}</i>",
                    opacity=0.7)
            ])
            fig.layout.plot_bgcolor = "#f9f9f9"
            fig.update_layout(barmode="group",
                              hoverlabel_align="right",
                              xaxis_title="Mileage (miles)",
                              yaxis_title="Average Price ($)",
                              title_text=f"{makemodel1} vs {makemodel2}",
                              title_x=0.5)
            desc1 = generate_description(car1, "rgb(82,188,163)",
                                         make_selected, model_selected,
                                         year_selected)
            desc2 = generate_description(car2, "#d64161", make_selected2,
                                         model_selected2, year_selected2)
            if desc1 or desc2:
                description = html.P(children=[
                    html.Ul(children=[
                        desc1, desc2,
                        html.Li(
                            html.Font(
                                "Hover over the bars to check the sample size. Larger sample size has a higher chance of yielding accurate statistics"
                            ))
                    ])
                ])
                show_description["display"] = "inline-block"
            show_graph["display"] = "block"
        show_second_car = {**styles.drop_down_group_style, "display": "block"}
        first_vehicle_title = "Vehicle 1"

    elif tab == "tab-3":
        if all(
            [make_selected, model_selected, year_selected, mileage_selected]):
            df = data.get_data(Make=make_selected, Model=model_selected)
            df.sort_values(by="Mileage", inplace=True)
            mileage_per_year = 12000
            predicted, model, transform, score = estimate.main(
                df, mileage_per_year)

            mileage_std = df.Mileage.std()

            fig = go.Figure(
                go.Scatter(
                    x=df.Mileage,
                    y=df.Price,
                    mode="markers",
                    name="Data points",
                    marker=dict(color="rgb(82,188,163)"),
                    text=[f"Year: {year}" for year in df.Year.astype("int")],
                    hovertemplate="<br><i>Mileage</i>: %{x}<br>" +
                    "<i>%{text}</i>" + "<br><i>Price</i>: $%{y}<br>",
                    opacity=0.5))
            mileage_selected = int(mileage_selected)
            if transform == "std":
                mileage = (mileage_selected - df.Mileage.mean()) / mileage_std
            elif transform == "log":
                mileage = np.log2(mileage_selected)
            estimated = int(
                model.predict([[mileage,
                                df.Year.max() - year_selected]])[0])
            print(f"Estimated Price {estimated}")
            print(
                f"R2 on Test {score}",
                f"Mileage coeff = {model.coef_[0]}, Year coff = {model.coef_[1]}"
            )
            fig.add_trace(
                go.Scatter(
                    x=[mileage_selected],
                    y=[estimated],
                    mode="markers",
                    marker=dict(color="#d64161", size=10),
                    name=f"Est. Average Price",
                    text=[f"Year: {year_selected}"],
                    hovertemplate="<br><i>Mileage</i>: %{x}<br>" +
                    "<i>%{text}</i>" +
                    "<br><i>Estimated Avg. Price</i>: $%{y}<br>",
                ))
            generated_mileage = list(range(0, 150000, mileage_per_year))
            generated_year = [
                int(df.Year.max() - (mileage // mileage_per_year))
                for mileage in generated_mileage
            ]
            fig.add_trace(
                go.Scatter(x=generated_mileage,
                           y=predicted,
                           mode="lines",
                           line=dict(
                               color="#d64161",
                               width=4,
                           ),
                           text=[f"Year: {year}" for year in generated_year],
                           hovertemplate="<br><i>Mileage</i>: %{x}<br>" +
                           "<i>%{text}</i>" +
                           "<br><i>Estimated Avg. Price<i>: $%{y}<br>",
                           name="Regression line"))
            fig.layout.plot_bgcolor = "#f9f9f9"
            fig.update_layout(
                xaxis_title="Mileage (miles)",
                yaxis_title="Price ($)",
                title=
                "Regression line: <i>Avg. Price = <b>a</b> f(Year) + <b>b</b> g(Mileage) + <b>c</b></i>",
                title_x=0.5,
                showlegend=True,
                hoverlabel=dict(font_size=14, font_family="Rockwell"))
            description = generate_description(df, "#d64161", make_selected,
                                               model_selected, year_selected,
                                               model, mileage_selected,
                                               estimated, score, mileage_std)
            show_description["display"] = "inline-block"
            show_graph["display"] = "block"

        mileage_box = {
            **styles.drop_down_style, "margin-top": "10px",
            "width": "100%",
            "display": "block"
        }
        trim_box = {**styles.drop_down_style, "margin-top": "10px", "display": "block"}
    elif tab == "tab-4":
        show_first_car["display"] = "none"

    return show_graph, show_description, description, fig, show_first_car, show_second_car, first_vehicle_title, mileage_box


@app.callback([Output("slct_model", "options"),
               Output("slct_model", "value")], [Input("slct_make", "value")])
def update_models_dropdown(make):
    if make:
        return [{"label": i, "value": i} for i in all_options[make]], None
    else:
        return [], None


@app.callback(
    [Output("slct_model2", "options"),
     Output("slct_model2", "value")], [Input("slct_make2", "value")])
def update_models2_dropdown(make):
    if make:
        return [{"label": i, "value": i} for i in all_options[make]], None
    else:
        return [], None


def generate_description(df,
                         color,
                         make_selected,
                         model_selected,
                         year_selected,
                         reg_model=None,
                         mileage=None,
                         predicted=None,
                         score=None,
                         mileage_std=None):
    """
    """
    desc = None
    if reg_model:
        depr_mileage = -1 * round(reg_model.coef_[0] / 500) * 500
        depr_year = -1 * round(reg_model.coef_[1] / 100) * 100
        mileage_std = round(mileage_std / 5000) * 5000
        desc = [
            html.Br(),
            html.Br(),
            html.Li(children=[
                html.Font(f"The  estimated avg. listing price of a "),
                html.Font(f"{year_selected} {make_selected} {model_selected} ",
                          style=dict(color=color)),
                html.Font(f"at {mileage:,} miles is "),
                html.Font(f"${predicted:,}.", style=dict(color=color)),
            ]),
            html.Li(children=[
                html.Font(f"Within the first {100000:,} miles, "),
                html.Font(f"{make_selected} {model_selected} ",
                          style=dict(color=color)),
                html.Font(f"cars depreciate by about "),
                html.Font(f"${depr_mileage:,} ", style=dict(color=color)),
                html.Font(f"for every "),
                html.Font(f"{mileage_std:,} ", style=dict(color=color)),
                html.Font("miles")
            ]),
            html.Li(children=[
                html.Font(f"A further depreciation of "),
                html.Font(f"${depr_year:,} ", style=dict(color=color)),
                html.Font("also happens as the model gets older by a year")
            ]),
            html.Li(children=[
                html.Font(
                    "The estimates are based on the multiple linear regression"
                ),
                html.Font("statistical method, which has "),
                html.
                A("these assumptions",
                  href=
                  "https://statisticsbyjim.com/regression/ols-linear-regression-assumptions/",
                  target="_blank")
            ])
        ]
        return desc
    newer_price, older_price = None, None
    newer_mileage, older_mileage = None, None
    year = year_selected or ""
    df = df[~df.Average_Price.isna()]
    try:
        newer_price, older_price = df[~df.Average_Price.isna()].iloc[
            [0, -1], 2].tolist()
        newer_mileage, older_mileage = df[~df.Average_Price.isna()].iloc[
            [0, -1], 0].tolist()
    except IndexError:
        pass
    if newer_price and older_price:
        value_lost = int(100 * (newer_price - older_price) / newer_price)
        desc = html.Li(children=[
            html.Font(f"As mileage increases from "),
            html.I(f'"{newer_mileage}" to "{older_mileage}", '),
            html.Font(f"{year} {make_selected} {model_selected} ",
                      style=dict(color=color)),
            html.Font("cars lose about "),
            html.Font(f"{value_lost}% ", style=dict(color=color)),
            html.Font(f"of their value.")
        ])
    return desc


if __name__ == "__main__":
    app.run_server(debug=True, port=8080)
