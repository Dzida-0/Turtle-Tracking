import logging
import pandas as pd

import requests


class DownloadTurtles:
    def __init__(self):
        self._last_downloaded_turtle = []
        self._connected = self.check_connection()
        self._possible_turtles = {}
        self._full_data = pd.DataFrame()

    def check_connection(self) -> bool:
        """
        Check if there is an internet connection by pinging Google's website.
        :return: True if successfully connected, False otherwise.
        """
        try:
            response = requests.get("https://www.google.com", timeout=3)
            self._connected = response.status_code == 200
        except requests.ConnectionError:
            self._connected = False
        except requests.Timeout:
            self._connected = False
        return self._connected

    def download_all_turtles_info(self) -> bool:
        """

        :return:
        """
        if not self.check_connection():
            logging.warning("No internet connection")
            return False
        url = "https://stc.mapotic.com/api/v1/poi/"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            turtles_data = []
            for turtle in data:
                self._possible_turtles.update({turtle["id"]: turtle["name"]})
                description = None
                biography = None
                project = None
                for i in turtle["attributes"]:
                    if i["code"] == "Biography":
                        biography = i["value"]
                    elif i["code"] == "Description":
                        description = i["value"]
                    elif i["code"] == "Project":
                        project = i["value"]

                if len(turtle["categories"]) == 0:
                    continue
                turtles_data.append(
                    {
                        "id": turtle["id"],
                        "name": turtle["name"],
                        "species": turtle["categories"][0]["name"],
                        "last_move_datetime": turtle["motion"]["last_move_datetime"],
                        "distance_from_release": turtle["motion"][
                            "distance_from_release"
                        ],
                        "avg_speed_from_release": turtle["motion"][
                            "avg_speed_from_release"
                        ],
                        "time_from_last_move": turtle["motion"]["time_from_last_move"],
                        "time_from_release": turtle["motion"]["time_from_release"],
                        "time_tracked": turtle["motion"]["time_tracked"],
                        "description": description,
                        "project": project,
                        "biography": biography,
                    }
                )
                self._full_data = pd.DataFrame(
                    turtles_data,
                    columns=[
                        "id",
                        "name",
                        "species",
                        "last_move_datetime",
                        "distance_from_release",
                        "avg_speed_from_release",
                        "time_from_last_move",
                        "time_from_release",
                        "time_tracked",
                        "description",
                        "project",
                        "biography",
                    ],
                )
            return True

        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Request error occurred: {req_err}")
        except ValueError:
            logging.error("Failed to decode JSON from response")
        except KeyError as key_err:
            logging.error(f"Key missing in JSON response: {key_err}")
        return False

    def get_possible_turtles(self) -> dict:
        """

        :return:
        """
        return self._possible_turtles

    def download_turtle_data(self, turtle_id) -> bool:
        """

        :param turtle_id:
        :return:
        """
        if not self.check_connection():
            logging.warning("No internet connection")
            return False
        url = f"https://stc.mapotic.com/api/v1/poi/{turtle_id}/move/?page_size=10000"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            turtles_points = []
            if "results" in data:
                for point in data["results"]:
                    point_data = point.get("data", {})
                    turtles_points.append(
                        {
                            "latitude": point_data.get("Lat", None),
                            "longitude": point_data.get("Lng", None),
                            "distance": point_data.get("Distance", None),
                            "duration": point_data.get("Duration", None),
                            "direction": point_data.get("Direction", None),
                            "time": point_data.get("CollectedDateTime", None),
                        }
                    )

                    self._last_downloaded_turtle = [
                        pd.DataFrame(
                            turtles_points,
                            columns=[
                                "latitude",
                                "longitude",
                                "distance",
                                "duration",
                                "direction",
                                "time",
                            ],
                        ),
                        self._full_data[self._full_data["id"] == 2],
                    ]

            else:
                raise ValueError

            return True

        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Request error occurred: {req_err}")
        except ValueError:
            logging.error("Failed to decode JSON from response")
        except KeyError as key_err:
            logging.error(f"Key missing in JSON response: {key_err}")
        return False

    def get_last_turtle_data(self) -> list:
        """

        :return:
        """
        return self._last_downloaded_turtle

    def test(self):
        return self._full_data
