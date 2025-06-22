import os
import sys
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Set testing environment variable
os.environ['TESTING'] = 'True'

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the app after setting up the environment
from app import app as flask_app, get_database

@pytest.fixture(autouse=True)
def mock_database(monkeypatch):
    """Mock the database for all tests."""
    # Create a mock database
    mock_db = MagicMock()
    mock_db.expenses = MagicMock()
    
    # Mock the get_database function to return our mock database
    def mock_get_db():
        return mock_db
    
    # Apply the mock
    monkeypatch.setattr('app.get_database', mock_get_db)
    return mock_db

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Configure Flask app for testing
    flask_app.config.update({
        'TESTING': True,
    })
    
    # Reset the database mock for each test
    flask_app.db = get_database()
    flask_app.expenses_collection = flask_app.db.expenses
    
    yield flask_app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def sample_expense():
    """Provide sample expense data for testing."""
    return {
        'amount': 100.50,
        'category': 'Food',
        'description': 'Lunch',
        'date': '2023-01-01'
    }
