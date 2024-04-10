"""Defines the methods used within the API that do not relate to the endpoints."""
# pylint: disable=unused-variable

from datetime import datetime
import json


def get_stories_from_json(mode: str) -> list[dict]:
    """Gets all stories from json file in a specified file mode."""
    modes = ["r", "x", "a", "t", "b"]
    if not ((len(mode) == 1 and mode.lower() in modes)
            or (len(mode) == 2 and mode[0].lower() in modes and mode[1] == "+")):
        raise ValueError("Mode must be valid file opening mode.")
    with open("stories.json", mode.lower(), encoding="utf-8") as file:
        return json.load(file)


def write_to_json(contents) -> None:
    """Overwrites json.file to contain data passed as argument."""
    with open("stories.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(contents, indent=4))


def get_stories_data(search, sort, order) -> list[dict]:
    """Gets the data to be returned when someone makes a GET request to stories."""
    return_data = get_stories_from_json("r")
    if len(return_data) == 0:
        return {"error": True, "message": "No stories were found"}
    if search:
        return_data = [s for s in return_data if search.lower()
                       in s["title"].lower()]

    if sort == "title":
        return sorted(return_data, key=lambda x: x[sort].lower(), reverse=order)

    if sort:
        return sorted(return_data, key=lambda x: x[sort], reverse=order)
    return sorted(return_data, key=lambda x: x["created_at"], reverse=order)


def get_max_id() -> int:
    """Gets the max id stored in json file."""
    return get_stories_from_json("r")[-1]["id"]


def create_story_dict(id_num, title, url) -> dict:
    """Creates a dictionary using arguments, to be added to stories json."""
    return {"created_at": datetime.now().strftime("%a, %d %b %Y %H:%M:%S") + " GMT",
            "id": id_num,
            "score": 0,
            "title": title,
            "updated_at": datetime.now().strftime("%a, %d %b %Y %H:%M:%S") + " GMT",
            "url": url
            }
