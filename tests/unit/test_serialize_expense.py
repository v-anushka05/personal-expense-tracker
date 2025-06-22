import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Mock ObjectId before importing from app
class MockObjectId:
    def __init__(self, id_str):
        self.id_str = id_str
    
    def __str__(self):
        return self.id_str

# Apply the mock
sys.modules['bson'] = type(sys)('bson')
sys.modules['bson'].ObjectId = MockObjectId

from app import serialize_expense

def test_serialize_expense():
    """Test serialization of expense object."""
    # Test with None input
    assert serialize_expense(None) is None
    
    # Test with empty dict
    assert serialize_expense({}) == {}
    
    # Test with ObjectId
    obj_id = MockObjectId("507f1f77bcf86cd799439011")
    expense = {
        '_id': obj_id,
        'amount': 100.50,
        'category': 'Food'
    }
    result = serialize_expense(expense)
    assert result['_id'] == "507f1f77bcf86cd799439011"
    assert isinstance(result['_id'], str)
    assert result['amount'] == 100.50
    assert result['category'] == 'Food'
