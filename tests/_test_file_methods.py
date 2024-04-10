"""tests for file_methods module"""

# pylint: skip-file

import json
import os
import sys
from unittest.mock import patch, mock_open

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from file_methods import (get_stories_data,
                 get_stories_from_json,
                 write_to_json)

SINGLE_STORY_DATA = '''[{
"created_at": "Fri, 24 Jun 2022 17:25:16 GMT",
"id": 2,
"score": 24,
"title": "eBird: A crowdsourced bird sighting database",
"updated_at": "Fri, 24 Jun 2022 17:25:16 GMT",
"url": "https://ebird.org/home"
}]'''

TWO_STORY_DATA = '''[{
"created_at": "Fri, 24 Jun 2022 17:25:16 GMT",
"id": 2,
"score": 24,
"title": "eBird: A crowdsourced bird sighting database",
"updated_at": "Fri, 24 Jun 2022 17:25:16 GMT",
"url": "https://ebird.org/home"
},
{
"created_at": "Fri, 24 Jun 2022 17:25:16 GMT",
"id": 3,
"score": 471,
"title": "Karen Gillan teams up with Lena Headey and Michelle Yeoh in assassin thriller Gunpowder Milkshake",
"updated_at": "Fri, 24 Jun 2022 17:25:16 GMT",
"url": "https://www.empireonline.com/movies/news/gunpowder-milk-shake-lena-headey-karen-gillan-exclusive/"
}
]'''

NO_STORY_DATA = "[]"

class TestGetStoriesData:
    @patch("builtins.open", new_callable=mock_open, read_data=SINGLE_STORY_DATA)
    def test_get_stories_data_name(self, mock_data):
        output = get_stories_data("eBird: A crowdsourced bird sighting database", "", False)
        assert "eBird: A crowdsourced bird sighting database" in output[0]["title"]
        assert mock_data.called

    def test_get_stories_data_order(self):
        output = get_stories_data("", "", False)
        assert output[0]["created_at"] <= output[1]["created_at"]

    def test_get_stories_data_sort_title(self):
        output = get_stories_data("", "title", False)
        assert output[0]["title"] <= output[1]["title"]

    @patch("builtins.open", new_callable=mock_open, read_data=NO_STORY_DATA)
    def test_get_stories_data_errors(self, mock_data):
        assert "error" in get_stories_data("", "", False)
        assert mock_data.called
    
class TestGetStories:
    @patch("builtins.open", new_callable=mock_open, read_data=SINGLE_STORY_DATA)
    def test_get_stories(self, mock_data):
        output = get_stories_from_json("r")[0]
        for i in ["created_at", "id", "score", "title", "updated_at", "url"]:
            assert i in output
            assert mock_data.called

    def test_get_stories_bad_mode(self):
        with pytest.raises(ValueError):
            get_stories_from_json("z")[0]

class TestWriteToJSON:
    @patch("builtins.open", new_callable=mock_open)
    def test_write_to_json(self, mock_file):
        write_to_json([{"id": 1}])
        mock_file.assert_called_once_with("stories.json", 'w', encoding='utf-8')
        mock_file().write.assert_called_once_with('[\n    {\n        "id": 1\n    }\n]')