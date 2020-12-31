from app import app
from app import server
import pandas as pd
import numpy as np
import estimate
import styles
import helper
import data

# Dash imports
import dash
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Get makes and models of cars
make_model_options = data.make_and_model()
manufacturers = sorted(make_model_options.keys())

# model years
years = list(range(2020, 2009, -1))

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
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
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
                                          style=styles.drop_down_style),
                             dcc.Dropdown(id="slct_trim",
                                          multi=False,
                                          placeholder="Select trim",
                                          style={
                                              "margin-top": "10px",
                                              "margin-bottom": "10px",
                                              **styles.drop_down_style
                                          }),
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
                 children=[])
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
    Output(component_id="input_mileage", component_property="style"),
    Output(component_id="slct_trim", component_property="style")
], [
    Input(component_id="slct_make", component_property="value"),
    Input(component_id="slct_model", component_property="value"),
    Input(component_id="slct_year", component_property="value"),
    Input(component_id="slct_trim", component_property="value"),
    Input(component_id="input_mileage", component_property="value"),
    Input(component_id="slct_make2", component_property="value"),
    Input(component_id="slct_model2", component_property="value"),
    Input(component_id="slct_year2", component_property="value"),
    Input(component_id="all-tabs-inline", component_property="value")
])
def update_graph(make_selected, model_selected, year_selected, trim_selected,
                 mileage_selected, make_selected2, model_selected2,
                 year_selected2, tab):
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

            marker = dict(color="#d64161")
            text = [f"Sample size: {cnt}" for cnt in df.Count.tolist()]
            hovertemplate = "<br><i>Mileage Range</i>: %{x} miles<br>" + \
            "<i>Average Price</i>: $%{y}<br>" + "<i>%{text}</i>"

            fig = helper.create_plot("bar",
                                     df.Mileage_range,
                                     df.Average_Price,
                                     error_y=dict(array=df.STD_Price.tolist()),
                                     marker=marker,
                                     text=text,
                                     template=hovertemplate,
                                     title=f"{car} Listing Price",
                                     xaxis_title="Mileage (miles)",
                                     yaxis_title="Average Price ($)",
                                     opacity=0.7)
            desc = helper.generate_description(
                df,
                "#d64161",
                make_selected,
                model_selected,
                year_selected,
                style=styles.description_tablets_style)
            if desc:
                description = [
                    html.Br(),
                    html.Br(), desc,
                    html.
                    P("Hover over the bars to check the sample size. " +
                      "Larger sample size has a higher chance of yielding accurate statistics",
                      style=styles.description_tablets_style)
                ]
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
            try:
                makemodel1, makemodel2 = df.MakeModel.unique().tolist()
            except ValueError:
                makemodel1 = df.MakeModel.unique().tolist()[0]
                makemodel2 = makemodel1
            car1 = df[df["MakeModel"] == makemodel1]
            car2 = df[df["MakeModel"] == makemodel2]

            name = [makemodel1, makemodel2]
            x = [car1.Mileage_range, car2.Mileage_range]
            y = [car1.Average_Price, car2.Average_Price]
            error_y = [
                dict(array=car1.STD_Price.tolist()),
                dict(array=car2.STD_Price.tolist())
            ]
            marker = [dict(color="rgb(82,188,163)"), dict(color="#d64161")]
            text = [[f"Sample size: {cnt}" for cnt in car1.Count.tolist()],
                    [f"Sample size: {cnt}" for cnt in car2.Count.tolist()]]
            hovertemplate = "<br><i>Mileage Range</i>: %{x} miles<br>" + \
            "<i>Average Price</i>: $%{y}<br>" + "<i>%{text}</i>"

            fig = helper.create_plot("groupbar",
                                     x,
                                     y,
                                     error_y=error_y,
                                     marker=marker,
                                     text=text,
                                     template=hovertemplate,
                                     name=name,
                                     title=f"{makemodel1} vs {makemodel2}",
                                     xaxis_title="Mileage (miles)",
                                     yaxis_title="Average Price ($)",
                                     opacity=0.7)

            desc1 = helper.generate_description(
                car1,
                "rgb(82,188,163)",
                make_selected,
                model_selected,
                year_selected,
                style=styles.description_tablets_style)
            desc2 = helper.generate_description(
                car2,
                "#d64161",
                make_selected2,
                model_selected2,
                year_selected2,
                style=styles.description_tablets_style)
            if desc1 or desc2:
                description = [
                    html.Br(),
                    html.Br(), desc1, desc2,
                    html.
                    P("Hover over the bars to check the sample size. " +
                      "Larger sample size has a higher chance of yielding accurate statistics",
                      style=styles.description_tablets_style)
                ]
                show_description["display"] = "inline-block"
            show_graph["display"] = "block"
        show_second_car = {**styles.drop_down_group_style, "display": "block"}
        first_vehicle_title = "Vehicle 1"

    elif tab == "tab-3":
        if all([
                make_selected, model_selected, year_selected, trim_selected,
                mileage_selected
        ]):
            df = data.get_data(Make=make_selected, Model=model_selected)
            df.sort_values(by="Mileage", inplace=True)
            mileage_per_year = 12000
            mileage_std = df.Mileage.std()
            mileage_std = round(mileage_std / 5000) * 5000

            # Select only the dataframe columns relevant for estimating price
            df = df[["Mileage", "Year", "Price", "clean_trim"]]
            predicted, model, transform, score, trim_columns = estimate.main(
                df, mileage_per_year)

            # A scatter plot of mileage vs price
            marker = dict(color="rgb(82,188,163)")
            text = [
                f"Year: {year}<br>Trim: {trim}"
                for year, trim in zip(df.Year.astype("int"), df.clean_trim)
            ]
            hovertemplate = "<br><i>Mileage</i>: %{x}<br>" + "<i>%{text}</i>" + \
            "<br><i>Price</i>: $%{y}<br>"
            title = f"Regression Estimator: {year_selected} {make_selected} {model_selected}"
            fig = helper.create_plot("scatter",
                                     df.Mileage,
                                     df.Price,
                                     mode="markers",
                                     name="Data points",
                                     marker=marker,
                                     text=text,
                                     template=hovertemplate,
                                     title=title,
                                     xaxis_title="Mileage (miles)",
                                     yaxis_title="Price ($)",
                                     opacity=0.5)

            # Compute estimated average price using the reg. model
            mileage_selected = int(mileage_selected)
            if transform == "std":
                mileage = (mileage_selected - df.Mileage.mean()) / mileage_std
            elif transform == "log":
                mileage = np.log2(mileage_selected)
            trim_columns.remove("clean_trim_Other")
            trim_binary = [
                1 if column.strip("clean_trim_") == trim_selected else 0
                for column in trim_columns
            ]
            estimated = int(
                model.predict(
                    [[mileage,
                      df.Year.max() - year_selected, *trim_binary]])[0])
            print(f"Estimated Price {estimated}")
            print(
                f"R2 on Test {score}",
                f"Mileage coeff = {model.coef_[0]}, Year coff = {model.coef_[1]}",
                f"Other coefs: {model.coef_[2:]}")

            # Show estimate as a scatter plot
            marker = dict(color="#d64161", size=10)
            text = [f"Year: {year_selected}<br>Trim: {trim_selected}"]
            hovertemplate = "<br><i>Mileage</i>: %{x}<br>" + "<i>%{text}</i>" + \
            "<br><i>Estimated Avg. Price</i>: $%{y}<br>"
            helper.create_plot("scatter", [mileage_selected], [estimated],
                               mode="markers",
                               name="Est. Average Price",
                               marker=marker,
                               text=text,
                               template=hovertemplate,
                               title=title,
                               xaxis_title="Mileage (miles)",
                               yaxis_title="Price ($)",
                               base_fig=fig)

            # Generate and plot a 'trend line' using the reg model
            generated_mileage = list(range(0, 150000, mileage_per_year))
            generated_year = [
                int(df.Year.max() - (mileage // mileage_per_year))
                for mileage in generated_mileage
            ]
            text = [f"Year: {year}" for year in generated_year]
            line = dict(color="#d64161", width=3)
            hovertemplate = "<br><i>Mileage</i>: %{x}<br>" + "<i>%{text}</i>" + \
            "<br><i>Estimated Avg. Price</i>: $%{y}<br>"
            helper.create_plot("scatter",
                               generated_mileage,
                               predicted,
                               mode="lines",
                               name="Regression line",
                               text=text,
                               template=hovertemplate,
                               line=line,
                               base_fig=fig)

            description = helper.generate_description(
                df,
                "#d64161",
                make_selected,
                model_selected,
                year_selected,
                model,
                mileage_selected,
                estimated,
                score,
                mileage_std,
                style=styles.description_tablets_style)
            show_description["display"] = "inline-block"
            show_graph["display"] = "block"

        mileage_box = {
            **styles.drop_down_style, "margin-top": "10px",
            "width": "100%",
            "display": "block"
        }
        trim_box = {
            **styles.drop_down_style, "margin-top": "10px",
            "display": "block"
        }
    elif tab == "tab-4":
        show_first_car["display"] = "none"

    return show_graph, show_description, description, fig, show_first_car, show_second_car, first_vehicle_title, mileage_box, trim_box


@app.callback([Output("slct_model", "options"),
               Output("slct_model", "value")], [Input("slct_make", "value")])
def update_models_dropdown(make):
    if make:
        return [{
            "label": i,
            "value": i
        } for i in make_model_options[make]["Models"]], None
    else:
        return [], None


@app.callback(
    [Output("slct_model2", "options"),
     Output("slct_model2", "value")], [Input("slct_make2", "value")])
def update_models2_dropdown(make):
    if make:
        return [{
            "label": i,
            "value": i
        } for i in make_model_options[make]["Models"]], None
    else:
        return [], None


@app.callback([Output("slct_trim", "options"),
               Output("slct_trim", "value")], [Input("slct_make", "value")])
def update_models2_dropdown(make):
    if make:
        return [{
            "label": i,
            "value": i
        } for i in make_model_options[make]["Trims"]], None
    else:
        return [], None


if __name__ == "__main__":
    app.run_server(debug=True, port=8080)
