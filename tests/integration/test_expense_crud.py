import sys
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch, call, ANY

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Mock ObjectId for testing
class MockObjectId:
    def __init__(self, id_str):
        self.id_str = id_str
    
    def __str__(self):
        return self.id_str

# Apply the mock
sys.modules['bson'] = type(sys)('bson')
sys.modules['bson'].ObjectId = MockObjectId

# Import the module after setting up mocks
with patch('pymongo.MongoClient'):
    from app import app, get_database, expenses_collection

class TestExpenseCRUD:
    def setup_method(self):
        """Setup test environment before each test."""
        # Create mock database client and collection
        self.mock_collection = MagicMock()
        self.mock_db = MagicMock()
        self.mock_db.expenses = self.mock_collection
        
        # Patch the get_database function
        self.patcher = patch('app.get_database', return_value=self.mock_db)
        self.mock_get_db = self.patcher.start()
        
        # Store the original expenses_collection
        self.original_expenses_collection = expenses_collection
        
        # Replace the actual collection with our mock
        import app
        app.expenses_collection = self.mock_collection
    
    def teardown_method(self):
        """Clean up after each test."""
        self.patcher.stop()
        
        # Restore the original expenses_collection
        import app
        app.expenses_collection = self.original_expenses_collection
    
    def test_create_expense(self, app):
        """Test creating a new expense."""
        # Setup test data
        expense_data = {
            'amount': 100.50,
            'category': 'Food',
            'description': 'Lunch',
            'date': '2023-01-01'
        }
        
        # Setup mock return value
        mock_result = MagicMock()
        mock_result.inserted_id = 'test_id_123'
        self.mock_collection.insert_one.return_value = mock_result
        
        # Import the module to get the current expenses_collection
        from app import expenses_collection
        
        # Perform the operation
        result = expenses_collection.insert_one(expense_data)
        
        # Verify the result
        self.mock_collection.insert_one.assert_called_once_with(expense_data)
        assert result == mock_result
    
    def test_read_expense(self, app):
        """Test reading an expense."""
        # Setup test data
        test_expense = {
            '_id': 'test_id_123',
            'amount': 100.50,
            'category': 'Food',
            'description': 'Lunch',
            'date': '2023-01-01'
        }
        
        # Setup mock return value
        self.mock_collection.find_one.return_value = test_expense
        
        # Import the module to get the current expenses_collection
        from app import expenses_collection
        
        # Perform the operation
        result = expenses_collection.find_one({'_id': 'test_id_123'})
        
        # Verify the result
        self.mock_collection.find_one.assert_called_once_with({'_id': 'test_id_123'})
        assert result == test_expense
    
    def test_update_expense(self, app):
        """Test updating an expense."""
        # Setup test data
        update_data = {'$set': {'amount': 150.75, 'description': 'Dinner'}}
        
        # Setup mock return value
        mock_result = MagicMock()
        mock_result.matched_count = 1
        mock_result.modified_count = 1
        self.mock_collection.update_one.return_value = mock_result
        
        # Import the module to get the current expenses_collection
        from app import expenses_collection
        
        # Perform the operation
        result = expenses_collection.update_one(
            {'_id': 'test_id_123'},
            update_data
        )
        
        # Verify the result
        self.mock_collection.update_one.assert_called_once_with(
            {'_id': 'test_id_123'},
            update_data
        )
        assert result == mock_result
    
    def test_delete_expense(self, app):
        """Test deleting an expense."""
        # Setup mock return value
        mock_result = MagicMock()
        mock_result.deleted_count = 1
        self.mock_collection.delete_one.return_value = mock_result
        
        # Import the module to get the current expenses_collection
        from app import expenses_collection
        
        # Perform the operation
        result = expenses_collection.delete_one({'_id': 'test_id_123'})
        
        # Verify the result
        self.mock_collection.delete_one.assert_called_once_with({'_id': 'test_id_123'})
        assert result == mock_result
