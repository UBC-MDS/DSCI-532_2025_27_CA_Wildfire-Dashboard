"""
Dash Application for Visualizing California Wildfire Data

This script initializes and runs a Dash web application that visualizes California wildfire data 
using various interactive components.

Modules:
    - Dash: The core Dash framework for building web applications.
    - dash_bootstrap_components (dbc): Provides Bootstrap components for styling.
    - callbacks: Custom module for handling application callbacks.
    - components: Custom module that contains UI components such as maps, charts, and widgets.

Attributes:
    app (Dash): The main Dash application instance.
    server (Flask): The Flask server instance used to deploy the app.

Layout:
    - `title`: The main title of the dashboard.
    - `info_section`: An informational section providing context.
    - `global_widgets`: Interactive input elements.
    - `cali_map`: A map visualization of wildfire impact.
    - `summary_card`: A summary card displaying key statistics.
    - `hover_info`: Displays additional details on hover.
    - `roof_chart`: Visualization of roof types affected by fires.
    - `damage_level`: Displays the severity of damage levels.
    - `structure_count`: A chart showing the number of structures affected.
    - `timeseries_chart`: A time-series visualization of wildfire occurrences.
    - `reference_info`: Additional reference information.

Usage:
    Run the script to start the Dash web application:
    
    ```bash
    python -m app.py
    ```

    Or, if embedded in a larger project, import and use the `app` and `server` instances as needed.

Example:
    ```python
    from app import app
    app.run_server(debug=True)
    ```

Authors:
    Forgive Agbesi, Thamer Aldawood, Elaine Chu, Gunisha Kaur

Date:
    [2025-03-15]
"""

from dash import Dash, html
import dash_bootstrap_components as dbc
from . import callbacks
from .components import title, global_widgets, cali_map, summary_card, damage_level, timeseries_chart, structure_count, roof_chart, info_section, reference_info, hover_info

# Initiatlize the app
app = Dash(__name__, 
           external_stylesheets=[dbc.themes.FLATLY])
server = app.server

# Layout
app.layout = dbc.Container([
    title, 
    info_section, 
     dbc.Row([
        global_widgets, 
        dbc.Col(
            [cali_map, 
            summary_card, 
            hover_info, 
            dbc.Row([
                roof_chart,
                damage_level],
            style={"marginTop": "20px"}),
            dbc.Row([
                structure_count,
                timeseries_chart],
            style={"marginTop": "20px"})])
            ]),
    reference_info],
    fluid=True,
    style={'margin': 0,
           'padding': 0,
           'overflow-x': 'hidden'}
    )
      


# Run the app/dashboard
if __name__ == '__main__':
    app.server.run(debug=True)
