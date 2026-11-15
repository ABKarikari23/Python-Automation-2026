from __future__ import annotations

import csv
from pathlib import Path

import requests

API_URL = "https://jsonplaceholder.typicode.com/posts"
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_FILE = OUTPUT_DIR / "posts_report.csv"
FIELDNAMES = ("id", "userId", "title", "body")


def fetch_posts() -> list[dict[str, object]]:
    """Retrieve posts from the JSONPlaceholder test API."""
    response = requests.get(API_URL, timeout=15)
    response.raise_for_status()

    try:
        data = response.json()
    except ValueError as error:
        raise ValueError("The API returned invalid JSON.") from error

    if not isinstance(data, list):
        raise ValueError("Unexpected API response: expected a list of posts.")

    posts: list[dict[str, object]] = []
    for index, record in enumerate(data):
        if not isinstance(record, dict):
            raise ValueError(
                f"Unexpected API response: post {index} is not an object."
            )
        posts.append({str(key): value for key, value in record.items()})

    return posts


def save_posts(
    posts: list[dict[str, object]], output_file: Path = OUTPUT_FILE
) -> None:
    """Save selected post fields to a CSV report."""
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        writer.writeheader()
        for post in posts:
            writer.writerow(
                {field: post.get(field, "") for field in FIELDNAMES}
            )

    print(f"Successfully saved {len(posts)} records.")
    print(f"Report location: {output_file}")


def main() -> None:
    print("Starting Python Web Data Collector...")

    try:
        posts = fetch_posts()
        save_posts(posts)
    except requests.RequestException as error:
        raise SystemExit(f"Data collection failed: {error}") from error
    except (OSError, ValueError) as error:
        raise SystemExit(f"Data processing failed: {error}") from error


if __name__ == "__main__":
    main()
