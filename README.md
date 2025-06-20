# 🧾 Personal Expense Tracker
A modern web application to track personal expenses with a clean, responsive interface, full CRUD functionality, and REST API integration.

# 🚀 Features
✅ Add, view, edit, and delete expenses

✅ Categorize expenses (Food, Transport, Shopping, Bills, Entertainment, Other)

✅ Search and filter expenses in real-time

✅ Responsive design (works on mobile, tablet, desktop)

✅ Modern dark theme UI

✅ Full API integration with MongoDB backend

# 🛠 Tech Stack
## Frontend: HTML5, CSS3, JavaScript (Vanilla), Bootstrap 5, Bootstrap Icons

## Backend: Python with Flask

## Database: MongoDB Atlas (Cloud MongoDB)

## Deployment: Local development setup (localhost)

## 🌐 API Documentation
### Base URL
```arduino
http://localhost:5001
```
### Endpoints
1️⃣ Get All Expenses
URL: /expenses

### Method: GET

Response Example:
```json
[
  {
    "_id": "60d5ec9e1c9d440000f2c1a1",
    "description": "Grocery shopping",
    "amount": 1500.50,
    "category": "Food",
    "date": "2023-06-20",
    "notes": "Weekly groceries"
  }
]
```
2️⃣ Add New Expense
URL: /expenses

### Method: POST

Request Body Example:
```json
{
  "description": "Dinner",
  "amount": 1200,
  "category": "Food",
  "date": "2023-06-20",
  "notes": "Dinner with friends"
}
```
Response Example:
```json
{
  "status": "success",
  "expense_id": "60d5ec9e1c9d440000f2c1a1"
}
```

### 3️⃣ Update Expense
URL: /expenses/<expense_id>

Method: PUT

Request Body: Same as POST

Response Example:
```json
{
  "status": "success",
  "message": "Expense updated successfully"
}
```
4️⃣ Delete Expense
URL: /expenses/<expense_id>

Method: DELETE

Response Example:

```json
{
  "status": "success",
  "message": "Expense deleted successfully"
}
```
# ⚙️ Prerequisites
Python 3.8+

MongoDB Atlas account (or local MongoDB)

pip (Python package manager)

# 📦 Setup Instructions
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/personal-expense-tracker.git
cd personal-expense-tracker
```
### 2️⃣ Set up Virtual Environment
```bash
python -m venv venv
```
# Activate:
# For Windows:
```
venv\Scripts\activate
```
# For Mac/Linux:
```
source venv/bin/activate
```
### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 4️⃣ Configure Environment Variables
Create a .env file in the root directory:
```ini
MONGO_URI=your_mongodb_connection_string
```
### 5️⃣ Run the Flask Server
```bash
python app.py
```
### 6️⃣ Open Application
Open templates/index.html directly in your browser OR
Use a local server to serve frontend files.

# 🔎 Testing the API (using cURL)
### Get all expenses:
```bash
curl http://localhost:5001/expenses
```
### Add a new expense:
```bash
curl -X POST http://localhost:5001/expenses \
-H "Content-Type: application/json" \
-d '{"description": "Test Expense", "amount": 1000, "category": "Food", "date": "2023-06-20"}'
```
### Update an expense (replace <id> with actual ID):
```bash
curl -X PUT http://localhost:5001/expenses/<id> \
-H "Content-Type: application/json" \
-d '{"description": "Updated Expense", "amount": 1500, "category": "Food", "date": "2023-06-20"}'
```
### Delete an expense:
```bash
curl -X DELETE http://localhost:5001/expenses/<id>
```
# 🖼 Screenshots
(Add screenshots of your working application here for visual reference)

# 🤝 Contributing
Contributions are welcome! Feel free to submit a pull request.

#📄 License
This project is licensed under the MIT License.
