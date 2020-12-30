import plotly.graph_objects as go
import dash_html_components as html


def create_plot(plot_type,
                x,
                y,
                *,
                error_y=None,
                mode=None,
                marker=None,
                text=None,
                template=None,
                title=None,
                name=None,
                xaxis_title=None,
                yaxis_title=None,
                opacity=None,
                line=None,
                base_fig=None):
    """
    """
    fig = go.Figure()
    if plot_type == "bar":
        fig = go.Figure(
            go.Bar(name="",
                   x=x,
                   y=y,
                   error_y=error_y,
                   marker=marker,
                   text=text,
                   hovertemplate=template,
                   opacity=opacity))
        fig.layout.plot_bgcolor = "#f9f9f9"
        fig.update_layout(hoverlabel_align="right",
                          xaxis_title=xaxis_title,
                          yaxis_title=yaxis_title,
                          title_text=title,
                          title_x=0.5)
    elif plot_type == "groupbar":
        fig = go.Figure(data=[
            go.Bar(name=name[0],
                   x=x[0],
                   y=y[0],
                   error_y=error_y[0],
                   marker=marker[0],
                   text=text[0],
                   hovertemplate=template,
                   opacity=opacity),
            go.Bar(name=name[1],
                   x=x[1],
                   y=y[1],
                   error_y=error_y[1],
                   marker=marker[1],
                   text=text[1],
                   hovertemplate=template,
                   opacity=opacity)
        ])
        fig.layout.plot_bgcolor = "#f9f9f9"
        fig.update_layout(barmode="group",
                          hoverlabel_align="right",
                          xaxis_title=xaxis_title,
                          yaxis_title=yaxis_title,
                          title_text=title,
                          title_x=0.5)
    elif plot_type == "scatter":
        if base_fig is None:
            fig = go.Figure(
                go.Scatter(x=x,
                           y=y,
                           mode=mode,
                           name=name,
                           marker=marker,
                           text=text,
                           hovertemplate=template,
                           opacity=opacity))
            fig.layout.plot_bgcolor = "#f9f9f9"
            fig.update_layout(hoverlabel_align="right",
                              xaxis_title=xaxis_title,
                              yaxis_title=yaxis_title,
                              title_text=title,
                              title_x=0.5)
        elif isinstance(base_fig, go.Figure):
            base_fig.add_trace(
                go.Scatter(x=x,
                           y=y,
                           mode=mode,
                           name=name,
                           marker=marker,
                           line=line,
                           text=text,
                           hovertemplate=template,
                           opacity=opacity))
            return base_fig

    return fig


def generate_description(df,
                         color,
                         make_selected,
                         model_selected,
                         year_selected,
                         reg_model=None,
                         mileage=None,
                         predicted=None,
                         score=None,
                         mileage_std=None,
                         style=None):
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
            html.P(children=[
                html.Font(f"The  estimated avg. listing price of a "),
                html.Font(f"{year_selected} {make_selected} {model_selected} ",
                          style=dict(color=color)),
                html.Font(f"at {mileage:,} miles is "),
                html.Font(f"${predicted:,}.", style=dict(color=color)),
            ],
                   style=style),
            html.P(children=[
                html.Font(f"Within the first {100000:,} miles, "),
                html.Font(f"{make_selected} {model_selected} ",
                          style=dict(color=color)),
                html.Font(f"cars depreciate by about "),
                html.Font(f"${depr_mileage:,} ", style=dict(color=color)),
                html.Font(f"for every "),
                html.Font(f"{mileage_std:,} ", style=dict(color=color)),
                html.Font("miles")
            ],
                   style=style),
            html.P(children=[
                html.Font(f"A further depreciation of "),
                html.Font(f"${depr_year:,} ", style=dict(color=color)),
                html.Font("also happens as the model gets older by a year")
            ],
                   style=style),
            html.P(children=[
                html.Font(
                    "The estimates are based on the statistical method known as "
                ),
                html.Font("multiple linear regression",
                          style=dict(color=color)),
                html.Font(", which has "),
                html.
                A("these assumptions",
                  href=
                  "https://statisticsbyjim.com/regression/ols-linear-regression-assumptions/",
                  target="_blank")
            ],
                   style=style)
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
        desc = html.P(children=[
            html.Font(f"As mileage increases from "),
            html.I(f'"{newer_mileage}" to "{older_mileage}", '),
            html.Font(f"{year} {make_selected} {model_selected} ",
                      style=dict(color=color)),
            html.Font("cars lose about "),
            html.Font(f"{value_lost}% ", style=dict(color=color))
        ],
                      style=style)
    return desc
