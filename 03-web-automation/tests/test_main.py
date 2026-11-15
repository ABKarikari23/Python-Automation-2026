import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import requests

import main


class FetchPostsTests(unittest.TestCase):
    @patch("main.requests.get")
    def test_fetch_posts_returns_api_records(self, get: Mock) -> None:
        response = Mock()
        response.json.return_value = [
            {"id": 1, "userId": 2, "title": "Title", "body": "Body"}
        ]
        get.return_value = response

        posts = main.fetch_posts()

        self.assertEqual(posts[0]["title"], "Title")
        get.assert_called_once_with(main.API_URL, timeout=15)
        response.raise_for_status.assert_called_once_with()

    @patch("main.requests.get")
    def test_fetch_posts_rejects_unexpected_response_shape(
        self, get: Mock
    ) -> None:
        response = Mock()
        response.json.return_value = {"id": 1}
        get.return_value = response

        with self.assertRaisesRegex(ValueError, "expected a list"):
            main.fetch_posts()

    @patch("main.requests.get")
    def test_fetch_posts_rejects_invalid_json(self, get: Mock) -> None:
        response = Mock()
        response.json.side_effect = ValueError("invalid JSON")
        get.return_value = response

        with self.assertRaisesRegex(ValueError, "invalid JSON"):
            main.fetch_posts()

    @patch("main.requests.get")
    def test_fetch_posts_propagates_http_errors(self, get: Mock) -> None:
        response = Mock()
        response.raise_for_status.side_effect = requests.HTTPError("Not found")
        get.return_value = response

        with self.assertRaises(requests.HTTPError):
            main.fetch_posts()

    @patch("main.fetch_posts", side_effect=requests.ConnectionError("offline"))
    def test_main_exits_when_request_fails(self, fetch_posts: Mock) -> None:
        with self.assertRaisesRegex(SystemExit, "Data collection failed"):
            main.main()


class SavePostsTests(unittest.TestCase):
    def test_save_posts_writes_csv_and_creates_parent_directory(self) -> None:
        posts = [
            {
                "id": 1,
                "userId": 2,
                "title": "A, quoted title",
                "body": "First line\nSecond line",
            }
        ]

        with tempfile.TemporaryDirectory() as temporary_directory:
            output_file = Path(temporary_directory) / "output" / "posts.csv"

            main.save_posts(posts, output_file)

            with output_file.open(newline="", encoding="utf-8") as csv_file:
                rows = list(csv.DictReader(csv_file))

        self.assertEqual(
            rows,
            [
                {
                    "id": "1",
                    "userId": "2",
                    "title": "A, quoted title",
                    "body": "First line\nSecond line",
                }
            ],
        )


if __name__ == "__main__":
    unittest.main()
