from flask import render_template, Blueprint,current_app

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
    m = folium.Map(location=[points[0]['lat'], points[0]['lon']], zoom_start=5,min_zoom=3,max_zoom=100, width='50%', height='400px',left = '10%')

    # Add points to the map
    for point in points:
        folium.Marker(
            location=[point['lat'], point['lon']],
            popup=point['popup']
        ).add_to(m)

    folium.PolyLine(
        locations=[[point["lat"], point["lon"]] for point in points],
        color="blue",
        weight=2.5,
        opacity=0.8
    ).add_to(m)

    # Dynamically resolve the template directory and save map as HTML file
    templates_path = os.path.join(current_app.root_path, 'templates')
    os.makedirs(templates_path, exist_ok=True)  # Ensure the directory exists

    # Save map as HTML file in templates folder
    map_path = os.path.join(templates_path, 'maps/generated_map.html')
    m.save(map_path)
    return map_path

def create_animated_path():
    # Sample data for turtle movements with timestamps
    points = [
        {"lat": 34.0522, "lon": -118.2437, "timestamp": "2023-12-01T08:00:00Z"},
        {"lat": 35.0522, "lon": -118.1437, "timestamp": "2023-12-01T09:00:00Z"},
        {"lat": 36.7783, "lon": -119.4179, "timestamp": "2023-12-01T10:00:00Z"},
        {"lat": 37.7783, "lon": -120.4179, "timestamp": "2023-12-01T11:00:00Z"},
        {"lat": 40.7128, "lon": -74.0060, "timestamp": "2023-12-01T12:00:00Z"},
    ]

    # Prepare GeoJSON structure with features
    features = []
    for point in points:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [point["lon"], point["lat"]]
            },
            "properties": {
                "time": point["timestamp"],
                "popup": f"Location: ({point['lat']}, {point['lon']})",
                "icon": "circle",
                "iconstyle": {
                    "fillColor": "blue",
                    "fillOpacity": 0.6,
                    "stroke": "true",
                    "radius": 5
                }
            }
        }
        features.append(feature)

    # Create Timestamped GeoJSON
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    # Create the base map
    m = folium.Map(
        location=[points[0]["lat"], points[0]["lon"]],
        zoom_start=5,
        width="50%",
        height="400px",
        left="10%"
    )

    # Add animated path layer
    TimestampedGeoJson(
        geojson,
        period="PT1H",  # Animation interval (1 hour per frame)
        add_last_point=True,
        auto_play=True,
        loop=True,
        max_speed=1,
        loop_button=True,
        date_options="YYYY-MM-DD HH:mm:ss"
    ).add_to(m)

    # Save map as HTML file in templates folder
    templates_path = os.path.join(current_app.root_path, "templates")
    os.makedirs(templates_path, exist_ok=True)  # Ensure the directory exists

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
