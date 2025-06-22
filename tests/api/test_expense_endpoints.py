import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, ANY

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app import app as flask_app

class MockObjectId(str):
    def __new__(cls, value=None):
        return str.__new__(cls, value or '507f1f77bcf86cd799439011')

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_add_expense(client):
    test_id = '507f1f77bcf86cd799439011'
    expense_data = {
        'amount': 100.50,
        'category': 'Food',
        'description': 'Lunch',
        'date': '2023-01-01'
    }
    mock_insert = MagicMock()
    mock_insert.inserted_id = test_id
    with patch('app.expenses_collection') as mock_collection, \
         patch('app.ObjectId', MockObjectId):
        mock_collection.insert_one.return_value = mock_insert
        response = client.post('/expenses', json=expense_data)
        assert response.status_code == 201
        data = response.get_json()
        assert data['id'] == test_id
        mock_collection.insert_one.assert_called_once_with(expense_data)

def test_get_expenses(client):
    test_expenses = [
        {'_id': '507f1f77bcf86cd799439011', 'description': 'Lunch', 'amount': 100.50, 'category': 'Food', 'date': '2023-01-01'},
        {'_id': '507f1f77bcf86cd799439012', 'description': 'Dinner', 'amount': 200.00, 'category': 'Food', 'date': '2023-01-02'}
    ]
    mock_cursor = MagicMock()
    mock_cursor.__iter__.return_value = test_expenses
    with patch('app.expenses_collection') as mock_collection:
        mock_collection.find.return_value = mock_cursor
        response = client.get('/expenses')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]['_id'] == test_expenses[0]['_id']
        assert data[1]['_id'] == test_expenses[1]['_id']
        mock_collection.find.assert_called_once_with({})

def test_get_single_expense(client):
    test_id = '507f1f77bcf86cd799439011'
    test_expense = {
        '_id': test_id,
        'description': 'Lunch',
        'amount': 100.50,
        'category': 'Food',
        'date': '2023-01-01'
    }
    with patch('app.expenses_collection') as mock_collection, \
         patch('app.ObjectId', MockObjectId):
        mock_collection.find_one.return_value = test_expense
        response = client.get(f'/expenses/{test_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['_id'] == test_id
        assert data['description'] == 'Lunch'
        mock_collection.find_one.assert_called_once_with({'_id': test_id})

def test_update_expense(client):
    test_id = '507f1f77bcf86cd799439011'
    update_data = {'amount': 150.75, 'description': 'Dinner'}
    mock_update_result = MagicMock()
    mock_update_result.matched_count = 1
    mock_update_result.modified_count = 1
    with patch('app.expenses_collection') as mock_collection, \
         patch('app.ObjectId', MockObjectId):
        mock_collection.update_one.return_value = mock_update_result
        response = client.put(f'/expenses/{test_id}', json=update_data)
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Expense updated successfully'
        mock_collection.update_one.assert_called_once_with({'_id': test_id}, {'$set': update_data})

def test_delete_expense(client):
    test_id = '507f1f77bcf86cd799439011'
    mock_delete_result = MagicMock()
    mock_delete_result.deleted_count = 1
    with patch('app.expenses_collection') as mock_collection, \
         patch('app.ObjectId', MockObjectId):
        mock_collection.delete_one.return_value = mock_delete_result
        response = client.delete(f'/expenses/{test_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Expense deleted successfully'
        mock_collection.delete_one.assert_called_once_with({'_id': test_id})

def test_invalid_expense_id(client):
    invalid_id = 'invalid_id'
    with patch('app.expenses_collection') as mock_collection, \
         patch('app.ObjectId', side_effect=Exception('Invalid ObjectId')):
        response = client.get(f'/expenses/{invalid_id}')
        assert response.status_code in (400, 404, 422, 500)
        data = response.get_json()
        assert 'error' in data
        mock_collection.find_one.assert_not_called()

def test_nonexistent_expense(client):
    test_id = '507f1f77bcf86cd799439011'
    with patch('app.expenses_collection') as mock_collection, \
         patch('app.ObjectId', MockObjectId):
        mock_collection.find_one.return_value = None
        response = client.get(f'/expenses/{test_id}')
        assert response.status_code in (404, 400, 422)
        data = response.get_json()
        assert 'error' in data
        mock_collection.find_one.assert_called_once_with({'_id': test_id})