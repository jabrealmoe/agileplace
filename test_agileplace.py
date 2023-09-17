import pytest
import os
from click.testing import CliRunner
from unittest.mock import patch, Mock

from agileplace import cards, users, create_csv


@pytest.fixture
def mock_env_variables():
    with patch.dict(os.environ, {"WEBSITE": "example", "AGILEPLACE": "token"}):
        yield


@pytest.fixture
def mock_requests():
    with patch("agileplace.requests") as mock_requests:
        yield mock_requests


@pytest.fixture
def mock_click_echo():
    with patch("agileplace.click.echo") as mock_echo:
        yield mock_echo


def test_cards(mock_env_variables, mock_requests, mock_click_echo):
    # Mock the requests.get method and response.json() method
    mock_response = Mock()
    mock_response.json.return_value = {"cards": [{"card_id": 1}, {"card_id": 2}]}
    mock_requests.get.return_value = mock_response
    runner = CliRunner()
    result = runner.invoke(cards, ["-o", "test_cards"])
    assert result.exit_code == 0
    assert "Writing file test_cards.csv" in result.output


def test_users(mock_env_variables, mock_requests, mock_click_echo):
    mock_response = Mock()
    mock_response.json.return_value = {"users": [{"user_id": 1}, {"user_id": 2}]}
    mock_requests.get.return_value = mock_response
    runner = CliRunner()
    result = runner.invoke(users, ["-o", "test_users"])
    assert result.exit_code == 0
    assert "Writing file test_users.csv" in result.output


def test_create_csv():
    mock_dataframe = Mock()
    mock_dataframe.to_csv.return_value = None
    with patch("agileplace.pd.DataFrame.from_dict", return_value=mock_dataframe):
        create_csv([{"key": "value"}], "test_create_csv")




if __name__ == "__main__":
    pytest.main()
