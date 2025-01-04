from flask import render_template, Blueprint, current_app
import os
from flask import current_app
import folium
from folium.plugins import TimestampedGeoJson
from folium import Popup
from branca.element import Template, MacroElement
import folium
from folium.plugins import TimestampedGeoJson
import os

main_bp = Blueprint('main', __name__)


@main_bp.route('/create_map')
def create_interactive_map(positions):
    """
    Generate an interactive map based on a list of TurtlePosition objects.

    Args:
        positions (list): A list of TurtlePosition objects containing `x`, `y`, and `turtle_id`.

    Returns:
        str: The path to the generated HTML map.
    """

    # Ensure positions is not empty
    if not positions:
        raise ValueError("No positions provided to create the map.")

    # Create a map centered at the first position
    first_position = positions[0]
    m = folium.Map(location=[first_position.x, first_position.y], zoom_start=5, min_zoom=3, max_zoom=100)

    # Add markers and collect points for the polyline
    polyline_points = []
    for position in positions:
        # Add each position as a marker
        folium.Marker(
            location=[position.x, position.y],
            popup=f"Turtle ID: {position.turtle_id}"
        ).add_to(m)

        # Collect points for the polyline
        polyline_points.append([position.x, position.y])

    # Add polyline to connect all positions
    folium.PolyLine(
        locations=polyline_points,
        color="blue",
        weight=2.5,
        opacity=0.8
    ).add_to(m)

    map_path = os.path.join(current_app.config.get('STORAGE_PATH'), "maps")
    m.save(map_path + '\generated_map.html')

    return map_path


def create_animated_path():
    points = [
        [34.0522, -118.2437],
        [35.0522, -118.1437],
        [36.7783, -119.4179],
        [37.7783, -120.4179],
        [40.7128, -74.0060],
    ]

    # Create map
    m = folium.Map(location=points[0], zoom_start=6)

    # Add points
    for point in points:
        folium.CircleMarker(location=point, radius=5, color="blue", fill=True).add_to(m)

    # Add polyline (path)
    path = folium.PolyLine(points, color="blue", weight=3)
    m.add_child(path)

    # Add custom JavaScript for animationy
    js = """
    var polyline = L.polyline(
        {{ coordinates }},
        {color: 'blue', weight: 3}
    ).addTo(map);

    var index = 1;
    var interval = 500; // Animation speed in milliseconds

    function drawSegment() {
        if (index < polyline.getLatLngs().length) {
            var segment = polyline.getLatLngs().slice(0, index + 1);
            polyline.setLatLngs(segment);
            index++;
            setTimeout(drawSegment, interval);
        }
    }

    drawSegment();
    """.replace(
        "{{ coordinates }}", str(points)
    )

    m.get_root().html.add_child(folium.Element(f"<script>{js}</script>"))

    # Save the map as an HTML file in the templates folder
    templates_path = os.path.join(current_app.root_path, "templates")
    os.makedirs(templates_path, exist_ok=True)

    map_path = os.path.join(templates_path, "maps/animated_map.html")
    m.save(map_path)
    return map_path


@main_bp.route('/')
def index():
    return render_template('index.html')
