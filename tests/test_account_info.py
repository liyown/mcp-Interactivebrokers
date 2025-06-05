import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from main import fast_app

client = TestClient(fast_app)


@pytest.fixture
def mock_ib():
    with patch("core.ib") as mock:
        yield mock


def test_connect_endpoint(mock_ib):
    mock_ib.isConnected.return_value = False
    response = client.get("/ib_api/account_info/connect")
    assert response.status_code == 200
    mock_ib.connect.assert_called_once()


def test_portfolio_endpoint_not_connected(mock_ib):
    mock_ib.isConnected.return_value = False
    response = client.get("/ib_api/account_info/portfolio")
    assert response.status_code == 200
    assert "error" in response.json()


def test_portfolio_endpoint_connected(mock_ib):
    mock_ib.isConnected.return_value = True
    mock_position = Mock()
    mock_position.contract.symbol = "AAPL"
    mock_position.position = 100
    mock_position.marketPrice = 150.0
    mock_position.marketValue = 15000.0
    mock_position.averageCost = 140.0
    mock_position.unrealizedPNL = 1000.0
    mock_position.realizedPNL = 500.0
    mock_ib.portfolio.return_value = [mock_position]

    response = client.get("/ib_api/account_info/portfolio")
    assert response.status_code == 200
    data = response.json()
    assert "AAPL" in str(data)
