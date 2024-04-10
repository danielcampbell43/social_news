"""
Server file for the Social News Site.
Uses Flask to define endpoints to GET and POST stories as well as up/downvote
"""
# pylint: disable=unused-variable, import-error
import sys
from os import environ
from urllib.error import URLError
from urllib.request import urlopen

from dotenv import load_dotenv
from flask import current_app, Flask, jsonify, request, render_template_string
from psycopg2 import connect, OperationalError
from psycopg2.extensions import connection

from news_scraper import (get_html,
                          parse_stories_bs)
from sql_methods import (delete_story,
                         get_stories_data,
                         insert_story,
                         patch_story,
                         update_score)

VALID_URL = "https://www.bbc.co.uk/news"
UPVOTE_DIRECTION = "up"
UPVOTE_CHAR = 'u'
DOWNVOTE_CHAR = 'd'
ERROR_MSG = "error"
HOST = "0.0.0.0"
PORT = 5000

app = Flask(__name__)


def check_internet_connection():
    """Checks if API server is connected to internet and able to perform scraping."""
    try:
        with urlopen('https://www.google.com/', timeout=10):
            return True
    except URLError:
        return False


load_dotenv()


def get_db_connection() -> connection:
    """Initalises a DB connection to Pokemon db."""
    try:
        return connect(
            user=environ["DATABASE_USERNAME"],
            password=environ["DATABASE_PASSWORD"],
            host=environ["DATABASE_IP"],
            port=environ["DATABASE_PORT"],
            database=environ["DATABASE_NAME"]
        )
    except OperationalError as err:
        print(err)
        print("Could not connect to DB.")
        return None


# This has to stay here for testing.
conn = get_db_connection()
if not conn:
    sys.exit()


@app.route("/", methods=["GET"])
def index():
    """Gets root of server."""
    return current_app.send_static_file("index.html")


@app.route("/add", methods=["GET"])
def addstory():
    """Gets add story page."""
    return current_app.send_static_file("./addstory/index.html")


@app.route("/scrape", methods=["GET"])
def scrape():
    """Sends a scrape page to website."""
    return current_app.send_static_file("./scrape/index.html")


@app.route("/scrape", methods=["POST"])
def scrape_post() -> tuple[dict, int]:
    """Scrapes stories from BBC news website and adds to stories."""
    data = request.json
    if not "url" in data:
        return jsonify({"error": True, "message": "Request must contain URL"}), 400

    url = data["url"]
    if VALID_URL not in url:
        return jsonify({"error": True, "message": f"URL must start with {VALID_URL}"}), 400

    if not check_internet_connection():
        return jsonify({"error": True, "message": "API not connected to internet."}), 400
    html = get_html(url)
    scraped_data = parse_stories_bs(url, html)

    for story in scraped_data:
        insert_story(conn, story[0], story[1])

    return jsonify({"message": "successful"}), 200


@app.route("/stories", methods=["GET"])
def get_stories() -> tuple[dict, int]:
    """Returns all stories stored on the server."""

    args = request.args.to_dict()
    search = args.get("search", "")
    sort = args.get("sort").lower()
    order = args.get("order").lower() == "descending"
    sort = "created_at" if sort == "created" else "updated_at" if sort == "modified" else sort

    res = get_stories_data(conn, search, sort, order)
    if ERROR_MSG in res:
        return jsonify(res), 404
    return jsonify(res), 200


@app.route("/stories", methods=["POST"])
def post_stories() -> tuple[dict, int]:
    """Posts a story to the database."""
    data = request.json

    if not ("url" in data and "title" in data) or not data["url"] or not data["title"]:
        return jsonify({"error": True, "message": "Request must contain URL & title"}), 500

    res = insert_story(conn, data["url"], data["title"])
    if ERROR_MSG in res:
        return jsonify({"message": "Request not successful"}), 500
    return jsonify({"message": "Success"}), 200


@app.route("/stories/<int:id_num>/votes", methods=["POST"])
def update_stories_votes(id_num: int) -> tuple[dict, int]:
    """Increases/decreases the score of a story."""
    data = request.json
    if "direction" not in data:
        return jsonify({"error": True, "message": "Request must contain if it is up or down"}, 500)

    direction_char = UPVOTE_CHAR if data["direction"] == UPVOTE_DIRECTION else DOWNVOTE_CHAR
    res = update_score(conn, id_num, direction_char)
    if ERROR_MSG in res:
        return jsonify({"message": res["message"]}), 404

    return jsonify({"message": "successful"}), 200


@app.route("/stories/<int:num_id>", methods=["PATCH"])
def patch_story_data(num_id: int) -> tuple[dict, int]:
    """Patches the values stored at the title/url key for a specific story."""

    data = request.json
    if not data["url"] and not data["title"]:
        return {"error": True, "message": "Request must contain URL and/or title."}, 500

    res = patch_story(conn, num_id, data["url"], data["title"])
    if ERROR_MSG in res:
        return jsonify({"message": "Not successful"}), 404
    return jsonify({"message": "Successful"}), 200


@app.route("/stories/<int:num_id>", methods=["DELETE"])
def delete_story_data(num_id: int) -> tuple[dict, int]:
    """Deletes a story from the API."""

    res = delete_story(conn, num_id)
    if ERROR_MSG in res:
        return jsonify({"message": "Not successful"}), 404
    return jsonify({"message": "successful"}), 200


@app.errorhandler(404)
def page_not_found(error):
    with open("./static/page_not_found.html", "r", encoding="utf-8") as f:
        return render_template_string(f.read().format(error)), 404


if __name__ == "__main__":
    app.run(debug=True, host=HOST, port=PORT)
