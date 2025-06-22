from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from bson import ObjectId

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='templates')
CORS(app, resources={r"/*": {"origins": "*"}})

def get_database():
    """Get database connection, with test environment support."""
    if os.getenv('TESTING') == 'True':
        # Use a mock database for testing
        from unittest.mock import MagicMock
        mock_db = MagicMock()
        mock_db.expenses = MagicMock()
        return mock_db
        
    # Use real MongoDB in non-test environments
    try:
        print("Connecting to MongoDB...")
        client = MongoClient(os.getenv("MONGO_URI"), serverSelectionTimeoutMS=5000)  # 5 second timeout
        # Test the connection
        client.server_info()  # Will raise an exception if connection fails
        print("Successfully connected to MongoDB")
        
        db = client['expense_tracker']
        expenses_collection = db['expenses']
        
        # Create indexes if they don't exist
        try:
            expenses_collection.create_index([("date", -1)])  # Index for sorting by date
            expenses_collection.create_index([("category", 1)])  # Index for filtering by category
        except Exception as e:
            print(f"Warning: Could not create indexes: {e}")
            print("This is normal when running tests")
            
        return db
        
    except Exception as e:
        print(f"Error connecting to MongoDB: {str(e)}")
        print(f"Using connection string: {os.getenv('MONGO_URI', 'Not set').split('@')[-1]}")
        raise

# Initialize database connection
expenses_collection = get_database().expenses

def serialize_expense(expense):
    """Convert ObjectId to string for JSON serialization"""
    if expense:
        expense['_id'] = str(expense['_id'])
    return expense

@app.route('/expenses', methods=['POST'])
def add_expense():
    """Add a new expense"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        required_fields = ['amount', 'category', 'description', 'date']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        result = expenses_collection.insert_one(data)
        return jsonify({
            'message': 'Expense added successfully',
            'id': str(result.inserted_id)
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/expenses', methods=['GET'])
def get_expenses():
    """Get all expenses"""
    try:
        expenses = list(expenses_collection.find({}))
        return jsonify([serialize_expense(exp) for exp in expenses])
    except Exception as e:
        print(f"Error fetching expenses: {str(e)}")
        return jsonify({'error': 'Failed to fetch expenses'}), 500

@app.route('/expenses/<id>', methods=['GET'])
def get_expense(id):
    """Get a single expense by ID"""
    try:
        expense = expenses_collection.find_one({'_id': ObjectId(id)})
        if not expense:
            return jsonify({'error': 'Expense not found'}), 404
        return jsonify(serialize_expense(expense))
    except Exception as e:
        print(f"Error fetching expense: {str(e)}")
        return jsonify({'error': 'Failed to fetch expense'}), 500

@app.route('/expenses/<id>', methods=['PUT'])
def update_expense(id):
    """Update an existing expense"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        result = expenses_collection.update_one(
            {'_id': ObjectId(id)},
            {'$set': data}
        )
        
        if result.matched_count == 0:
            return jsonify({'error': 'Expense not found'}), 404
            
        return jsonify({'message': 'Expense updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/expenses/<id>', methods=['DELETE'])
def delete_expense(id):
    """Delete an expense"""
    try:
        result = expenses_collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count == 0:
            return jsonify({'error': 'Expense not found'}), 404
        return jsonify({'message': 'Expense deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Serve the main page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test-db')
def test_db():
    """Test MongoDB connection"""
    try:
        # Try to fetch server info
        server_info = client.server_info()
        # Try a simple database operation
        db.list_collection_names()
        return jsonify({
            'status': 'success',
            'mongo_server': server_info.get('version'),
            'database': db.name,
            'collections': db.list_collection_names()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'connection_string': os.getenv('MONGO_URI').split('@')[-1]  # Don't expose full connection string
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
