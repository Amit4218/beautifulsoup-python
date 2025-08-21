import os
import pandas as pd
import pytest
import mongomock
from unittest.mock import patch
from bs4 import BeautifulSoup

# Import your scraper functions
from main import (
    dataToCsv,
    database,
    main,
)


# --------------------------
# Tests for dataToCsv
# --------------------------
def test_dataToCsv_creates_file(tmp_path):
    titles = ["Book A", "Book B"]
    images = ["http://img1", "http://img2"]
    ratings = ["Five", "Three"]
    instocks = ["In stock", "Out of stock"]
    prices = ["£10.99", "£20.50"]

    test_file = tmp_path / "books_data.csv"

    # Change cwd so file is written in tmp_path
    old_cwd = os.getcwd()
    os.chdir(tmp_path)

    your_module.dataToCsv(titles, images, ratings, instocks, prices)

    assert os.path.exists("books_data.csv")

    df = pd.read_csv("books_data.csv")
    assert list(df.columns) == [
        "Book Names",
        "Book Prices",
        "Image Links",
        "Availability",
        "Book Rating",
    ]
    assert len(df) == 2
    assert df["Book Names"][0] == "Book A"

    os.chdir(old_cwd)


def test_dataToCsv_with_empty_lists(tmp_path):
    old_cwd = os.getcwd()
    os.chdir(tmp_path)

    your_module.dataToCsv([], [], [], [], [])
    df = pd.read_csv("books_data.csv")
    assert df.empty

    os.chdir(old_cwd)


# --------------------------
# Tests for database
# --------------------------
@patch("your_module.MongoClient", new=mongomock.MongoClient)
def test_database_inserts_data():
    titles = ["Book A"]
    images = ["http://img1"]
    ratings = ["Five"]
    instocks = ["In stock"]
    prices = ["£10.99"]

    post_id = your_module.database(titles, images, ratings, instocks, prices)

    client = mongomock.MongoClient()
    db = client.beautiful_soup_test
    posts = list(db.posts.find({}))

    assert len(posts) == 1
    assert posts[0]["Book name"] == "Book A"
    assert "date" in posts[0]
    assert post_id is not None


@patch("your_module.MongoClient", new=mongomock.MongoClient)
def test_database_with_empty_lists():
    post_id = your_module.database([], [], [], [], [])
    # Should not insert anything
    assert post_id is None or isinstance(post_id, str)


# --------------------------
# Tests for scraping logic
# --------------------------
def test_scraping_parses_sample_html(monkeypatch, tmp_path):
    fake_html = """
    <html>
        <article class="product_pod">
            <h3><a title="Fake Book"></a></h3>
            <div class="image_container"><img src="../../../media/cache/fake.jpg"/></div>
            <div class="product_price"><p>£15.00</p></div>
            <p class="instock availability">In stock</p>
            <p class="star-rating Three"></p>
        </article>
    </html>
    """

    def fake_requests_get(url):
        class FakeResponse:
            text = fake_html

        return FakeResponse()

    monkeypatch.setattr(your_module.requests, "get", fake_requests_get)

    # Run scraper (creates books_data.csv)
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    your_module.main()

    df = pd.read_csv("books_data.csv")
    assert "Fake Book" in df["Book Names"].values
    assert "£15.00" in df["Book Prices"].values
    assert "Three" in df["Book Rating"].values

    os.chdir(old_cwd)
