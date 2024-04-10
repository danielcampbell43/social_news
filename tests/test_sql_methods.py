"""tests for file_methods module"""

# pylint: skip-file

import datetime
import os
import sys
from unittest.mock import MagicMock

from sql_methods import (delete_story,
                         get_stories_data,
                         insert_story,
                         patch_story,
                         update_score)

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class TestGetStoriesData:
    def test_get_stories_data_name(self):
        conn = MagicMock()
        mock_fetch = conn.cursor().fetchall
        mock_fetch.return_value = [('id', 2),
                                   ('title', 'eBird: A crowdsourced bird sighting database'),
                                   ('url', 'https://ebird.org/home'),
                                   ('created_at', datetime.datetime(
                                       2024, 2, 20, 15, 16, 23, 205084)),
                                   ('updated_at', datetime.datetime(
                                       2024, 2, 20, 15, 16, 23, 205084)),
                                   ('score', 0)]
        output = get_stories_data(conn,
                                  "eBird", "", False)
        assert "eBird: A crowdsourced bird sighting database" in output[1][1]
        assert mock_fetch.called

    def test_get_stories_data_order(self):
        conn = MagicMock()
        mock_fetch = conn.cursor().fetchall
        mock_fetch.return_value = [[('id', 8),
                                    ('title', 'Aukus deal: Summit was projection of power and collaborative intent'),
                                    ('url', 'https://www.bbc.co.uk/news/uk-politics-64948535'),
                                    ('created_at', datetime.datetime(
                                        2024, 2, 20, 15, 16, 23, 205084)),
                                    ('updated_at', datetime.datetime(
                                        2024, 2, 20, 15, 16, 23, 205084)),
                                    ('score', 1)
                                    ], [('id', 7),
                                        ('title', 'SVB and Signature Bank: How bad is US banking crisis and what does it mean?'),
                                        ('url', 'https://www.bbc.co.uk/news/business-64951630'),
                                        ('created_at', datetime.datetime(
                                            2024, 2, 20, 15, 16, 23, 205084)),
                                        ('updated_at', datetime.datetime(
                                            2024, 2, 20, 15, 16, 23, 205084)),
                                        ('score', 0)]]
        output = get_stories_data(conn, "", "", False)
        assert output[0][3][1] <= output[1][3][1]
        assert mock_fetch.called

    def test_get_stories_data_sort_title(self):
        conn = MagicMock()
        mock_fetch = conn.cursor().fetchall
        mock_fetch.return_value = [[('id', 8),
                                    ('title', 'Aukus deal: Summit was projection of power and collaborative intent'),
                                    ('url', 'https://www.bbc.co.uk/news/uk-politics-64948535'),
                                    ('created_at', datetime.datetime(
                                        2024, 2, 20, 15, 16, 23, 205084)),
                                    ('updated_at', datetime.datetime(
                                        2024, 2, 20, 15, 16, 23, 205084)),
                                    ('score', 1)
                                    ], [('id', 5),
                                        ('title', 'Budget: Pensions to get boost as tax-free limit to rise'),
                                        ('url', 'https://www.bbc.co.uk/news/business-64949083'),
                                        ('created_at', datetime.datetime(
                                            2024, 2, 20, 15, 16, 23, 205084)),
                                        ('updated_at', datetime.datetime(
                                            2024, 2, 20, 15, 16, 23, 205084)),
                                        ('score', 0)]]
        output = get_stories_data(conn, "", "title", False)
        assert output[0][1][1] <= output[1][1][0]
        assert mock_fetch.called

    def test_get_stories_data_errors(self):
        conn = MagicMock()
        mock_fetch = conn.cursor().fetchall
        mock_fetch.return_value = []
        res = get_stories_data(conn, "zzzzzzzzzzz", "", False)
        assert res["error"]
        assert res["message"] == "No stories were found"
        assert mock_fetch.called

    def test_get_stories_bad_args(self):
        conn = MagicMock()
        res = get_stories_data(conn, 1, 1, "foo")
        assert res["error"]
        assert res["message"] == "Invalid argument type(s)"


class TestInsertStory:
    def test_insert_story(self):
        conn = MagicMock()
        mock_fetch = conn.cursor().fetchall
        mock_fetch.return_value = [1]

        res = insert_story(conn, "foo", "bar")
        res["message"] == "Update score successful."
        assert mock_fetch.called

    def test_insert_story_fail(self):
        conn = MagicMock()
        mock_fetch = conn.cursor().fetchall
        mock_fetch.return_value = []

        res = insert_story(conn, "foo", "bar")
        assert res["error"]
        assert res["message"] == "Update score failed."
        assert mock_fetch.called

    def test_insert_story_bad_args(self):
        conn = MagicMock()
        res = insert_story(conn, 1, 1)
        assert res["error"]
        assert res["message"] == "Invalid argument type(s)"


class TestUpdateScore:
    def test_update_score(self):
        conn = MagicMock()
        mock_fetch = conn.cursor().fetchall
        mock_fetch.return_value = [1]

        res = update_score(conn, 1, "u")
        res["message"] == "Update score successful."
        assert mock_fetch.called

    def test_update_score_fail_first_query(self):
        conn = MagicMock()
        mock_fetch = conn.cursor().fetchall
        mock_fetch.side_effect = [[], [1]]

        res = update_score(conn, -1, "u")
        assert res["error"]
        assert res["message"] == "Incorrect ID."

    def test_update_score_fail_second_query(self):
        conn = MagicMock()
        mock_fetch = conn.cursor().fetchall
        mock_fetch.side_effect = [[1], []]

        res = update_score(conn, -1, "u")
        assert res["error"]
        assert res["message"] == "Update score failed."
        assert mock_fetch.called

    def test_update_score_bad_args(self):
        conn = MagicMock()
        res = update_score(conn, "a", "a")
        assert res["error"]
        assert res["message"] == "Invalid argument type(s)"


class TestPatchStory:
    def test_patch_story(self):
        conn = MagicMock()
        mock_fetch = conn.cursor().fetchall
        mock_fetch.return_value = 1

        res = patch_story(conn, 1, "foo", "bar")
        res['message'] == 'Update story successful.'
        assert mock_fetch.called

    def test_patch_story_fail(self):
        conn = MagicMock()
        mock_fetch = conn.cursor().fetchall
        mock_fetch.return_value = []

        res = patch_story(conn, -1, "foo", "bar")
        assert res["message"] == "Update story failed."
        assert res["error"]
        assert mock_fetch.called

    def test_patch_story_bad_args(self):
        conn = MagicMock()
        res = patch_story(conn, "a", 1, 1)
        assert res["error"]
        assert res["message"] == "Invalid argument type(s)"


class TestDeleteStory:
    def test_delete_story(self):
        conn = MagicMock()
        mock_fetch = conn.cursor().fetchall
        mock_fetch.return_value = 1

        res = delete_story(conn, 1)
        assert res["message"] == "Delete story successful."
        assert mock_fetch.called

    def test_delete_story_fail(self):
        conn = MagicMock()
        mock_fetch = conn.cursor().fetchall
        mock_fetch.return_value = []

        res = delete_story(conn, -1)
        assert res["message"] == "Update story failed."
        assert res["error"]
        assert mock_fetch.called

    def test_delete_story_bad_args(self):
        conn = MagicMock()
        res = delete_story(conn, "a")
        assert res["error"]
        assert res["message"] == "Invalid argument type(s)"
