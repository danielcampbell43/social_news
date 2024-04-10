"""Tests for API."""

# pylint: skip-file
import json
import os
import sys
from unittest.mock import patch

import pytest

from api import app

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


@pytest.fixture(scope='module')
def test_client():
    with app.test_client() as testing_client:
        yield testing_client


class TestStoriesRoute:
    def test_index(self, test_client):
        response = test_client.get('/')
        assert response.status_code == 200

    @patch("api.conn", 1)
    @patch("api.get_stories_data")
    def test_get_stories(self, mock, test_client):
        mock.return_value = [{"created_at": 1,
                             "id": 1,
                              "score": 1,
                              "title": "1",
                              "updated_at": 1,
                              "url": "1"}]
        response = test_client.get(
            "/stories?sort=title&order=ascending&search=aukus")
        assert response.status_code == 200
        for i in ["created_at", "id", "score", "title", "updated_at", "url"]:
            assert i in response.json[0]
        assert mock.called

    @patch("api.get_stories_data")
    def test_get_stories_error(self, mock, test_client):
        mock.return_value = {"error": True,
                             "message": "No stories were found"}
        response = test_client.get(
            "/stories?sort=title&order=ascending&search=aukus")
        assert "error" in response.json

    @patch("api.insert_story")
    def test_post_stories(self, mock, test_client):
        data = {"url": "foo", "title": "bar"}
        mock.return_value = {"message": "Insert story successful."}
        response = test_client.post("/stories", data=json.dumps(data),
                                    headers={"Content-Type": "application/json"})

        assert mock.called
        assert response.status_code == 200

    def test_post_error(self, test_client):
        data = {"title": "bar"}
        response = test_client.post("/stories", data=json.dumps(data),
                                    headers={"Content-Type": "application/json"})
        assert "error" in response.json


class TestVotingRoute:

    @patch("api.update_score")
    def test_update_votes_up(self, mock, test_client):
        mock.return_value = {"message": "Update score successful."}
        data = {"direction": "up"}
        response = test_client.post(f"/stories/1/votes", data=json.dumps(data),
                                    headers={"Content-Type": "application/json"})

        assert mock.called
        assert response.status_code == 200

    @patch("api.update_score")
    def test_update_votes_down(self, mock, test_client):
        mock.return_value = {"message": "Update score successful."}
        data = {"direction": "down"}
        response = test_client.post(f"/stories/1/votes", data=json.dumps(data),
                                    headers={"Content-Type": "application/json"})

        assert mock.called
        assert response.status_code == 200

    @patch("api.update_score")
    def test_update_votes_down_at_0(self, mock, test_client):
        mock.return_value = {"error": True,
                             "message": "Cannot downvote a story on 0 score."}

        data = {"direction": "down"}
        res = test_client.post(f"/stories/1/votes", data=json.dumps(data),
                               headers={"Content-Type": "application/json"})

        assert mock.called
        assert res.json["message"] == "Cannot downvote a story on 0 score."

    def test_update_votes_no_direction(self, test_client):
        data = {}
        res = test_client.post(f"/stories/1/votes", data=json.dumps(data),
                               headers={"Content-Type": "application/json"})

        assert b"error" in res.data

    @patch("api.update_score")
    def test_incorrect_id_fails(self, mock, test_client):
        mock.return_value = {"error": True, "message": "Incorrect ID."}
        data = {"direction": "down"}
        res = test_client.post(f"/stories/2147483648/votes", data=json.dumps(data),
                               headers={"Content-Type": "application/json"})

        assert res.status_code == 404
        assert res.json["message"] == "Incorrect ID."
        assert mock.called


class TestModifyStoriesRoute:

    @patch("api.patch_story")
    def test_stories_id_patch(self, mock, test_client):
        mock.return_value = "Success"
        data = {"url": "foo", "title": "bar"}
        res = test_client.patch("/stories/1", data=json.dumps(data),
                                headers={"Content-Type": "application/json"})
        assert mock.called
        assert res.status_code == 200

    @patch("api.patch_story")
    def test_incorrect_id_fails(self, mock, test_client):
        mock.return_value = {"error": True, "message": "Update story failed."}
        res = test_client.patch(f"/stories/asd/", data=json.dumps([]),
                                headers={"Content-Type": "application/json"})
        assert res.status_code == 404

    def test_incorrect_bad_data_fails(self, test_client):
        res = test_client.patch(f"/stories/1/", data=json.dumps([]),
                                headers={"Content-Type": "application/json"})
        assert res.status_code == 404

    @patch("api.delete_story")
    def test_stories_id_delete(self, mock, test_client):
        mock.return_value = "Success"
        res = test_client.delete(f"/stories/1")
        assert mock.called
        assert res.status_code == 200


class TestScrape:
    @patch("api.parse_stories_bs")
    def test_scrape_patch(self, mock, test_client):
        mock.return_value = []
        res = test_client.post(f"/scrape", data=json.dumps({"url": "https://www.bbc.co.uk/news"}),
                               headers={"Content-Type": "application/json"})
        assert mock.called
        assert res.status_code == 200

    def test_scrape_bad_post(self, test_client):
        res = test_client.post(f"/scrape", data=json.dumps({}),
                               headers={"Content-Type": "application/json"})
        assert "error" in res.json
        assert res.status_code == 400

    def test_scrape_bad_url(self, test_client):
        res = test_client.post(f"/scrape", data=json.dumps({"url": "https://www.bcc.co.uk/news"}),
                               headers={"Content-Type": "application/json"})
        assert "error" in res.json
        assert res.status_code == 400

    @patch("api.check_internet_connection")
    def test_scrape_no_internet(self, mock, test_client):
        mock.return_value = False
        res = test_client.post(f"/scrape", data=json.dumps({"url": "https://www.bbc.co.uk/news"}),
                               headers={"Content-Type": "application/json"})
        assert res.json["message"] == "API not connected to internet."
        assert res.status_code == 400


class TestAPI:
    def test_api_bad_endpoint(self, test_client):
        response = test_client.get('/alskdjhfalksdj')
        assert response.status_code == 404
