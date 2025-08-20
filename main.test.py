import pytest
from unittest.mock import patch, MagicMock
from main.test import dataToCsv, database

def test_dataToCsv_creates_csv(monkeypatch):
    titles = ["Book1", "Book2"]
    images = ["img1.jpg", "img2.jpg"]
    ratings = ["Three", "Five"]
    instocks = ["In stock", "Out of stock"]
    prices = ["£10.00", "£20.00"]

    mock_df = MagicMock()
    monkeypatch.setattr("pandas.DataFrame", lambda x: mock_df)
    mock_df.to_csv = MagicMock()

    dataToCsv(titles, images, ratings, instocks, prices)
    mock_df.to_csv.assert_called_once_with("books_data.csv", index=False)

def test_database_inserts_data(monkeypatch):
    titles = ["Book1"]
    images = ["img1.jpg"]
    ratings = ["Three"]
    instocks = ["In stock"]
    prices = ["£10.00"]

    mock_client = MagicMock()
    mock_db = MagicMock()
    mock_posts = MagicMock()
    mock_insert = MagicMock(return_value=MagicMock(inserted_id="fake_id"))

    mock_client.beautiful_soup_test = mock_db
    mock_db.posts = mock_posts
    mock_posts.insert_one = mock_insert

    monkeypatch.setattr("main.test.MongoClient", lambda x: mock_client)

    post_id = database(titles, images, ratings, instocks, prices)
    mock_insert.assert_called_once()
    assert post_id == "fake_id"import pytest
from main.test import main_function

def test_main_function_normal():
    # Replace with actual input and expected output
    input_data = "normal input"
    expected_output = "expected result"
    assert main_function(input_data) == expected_output

def test_main_function_empty_input():
    input_data = ""
    expected_output = "expected for empty"
    assert main_function(input_data) == expected_output

def test_main_function_invalid_input():
    input_data = None
    with pytest.raises(Exception):
        main_function(input_data)