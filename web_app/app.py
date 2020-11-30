import dash

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(
    "Used Car Statistics Dashboard",
    external_stylesheets=external_stylesheets,
)
server = app.server
app.config.suppress_callback_exceptions = True
app.title = "Used Car Statistics Dashboard"
app.description = """A dashboard that illustrates price and other relevant information
of used cars from popular manufacturers."""
