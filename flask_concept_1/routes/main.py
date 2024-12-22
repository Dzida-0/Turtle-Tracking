from flask import render_template, Blueprint,current_app
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



def create_interactive_map():
    # Sample coordinates for turtle movements
    points = [
        {"lat": 34.0522, "lon": -118.2437, "popup": "Los Angeles"},
        {"lat": 36.7783, "lon": -119.4179, "popup": "California"},
        {"lat": 40.7128, "lon": -74.0060, "popup": "New York"}
    ]

    # Create a map centered at the first point
    m = folium.Map(location=[points[0]['lat'], points[0]['lon']], zoom_start=5, min_zoom=3, max_zoom=100)

    # Add points to the map
    for point in points:
        folium.Marker(
            location=[point['lat'], point['lon']],
            popup=point['popup']
        ).add_to(m)

    # Add polyline
    folium.PolyLine(
        locations=[[point["lat"], point["lon"]] for point in points],
        color="blue",
        weight=2.5,
        opacity=0.8
    ).add_to(m)

    # Save map as HTML file in templates folder
    templates_path = os.path.join(current_app.root_path, 'templates')
    os.makedirs(templates_path, exist_ok=True)  # Ensure the directory exists

    map_path = os.path.join(templates_path, 'maps/generated_map.html')
    m.save(map_path)

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

    # Add custom JavaScript for animation
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
    map_path = create_interactive_map()
    return render_template('index.html')

@main_bp.route('/i2')
def i2():
    map_path = create_animated_path()
    return render_template('i2.html')
