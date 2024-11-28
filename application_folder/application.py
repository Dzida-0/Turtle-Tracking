import dash
from dash import dcc, html, Input, Output
import io
import pandas as pd

from src.data_gathering.download_data import download_turtles_info

# Sample data for download
df = pd.DataFrame({
    "Column 1": [1, 2, 3],
    "Column 2": ["A", "B", "C"]
})

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout with navigation and download buttons
app.layout = html.Div([
    html.H1("My Dash App"),

    # Navigation buttons
    html.Div([
        html.Button("Go to Home", id="home-btn", n_clicks=0),
        html.Button("Go to About", id="about-btn", n_clicks=0),
    ], style={"margin-bottom": "20px"}),

    # Dynamic content area
    html.Div(id="page-content"),

    # Download button
    html.Div([
        html.Button("Download Data", id="download-btn")
    ])
])


# Callbacks for navigation
@app.callback(
    Output("page-content", "children"),
    [Input("home-btn", "n_clicks"),
     Input("about-btn", "n_clicks")]
)
def render_page(home_clicks, about_clicks):
    # Determine which button was clicked
    if home_clicks > about_clicks:
        return html.Div([
            html.H2("Home Page"),
            html.P("Welcome to the home page!")
        ])
    elif about_clicks > home_clicks:
        return html.Div([
            html.H2("About Page"),
            html.P("This is the about page.")
        ])
    else:
        return html.Div([
            html.H2("Default Page"),
            html.P("Click a button to navigate.")
        ])


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
