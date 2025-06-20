# Personal Expense Tracker

A modern web application to track personal expenses with a clean, responsive interface and full CRUD functionality.

## Features

- Add, view, edit, and delete expenses
- Categorize expenses
- Search and filter expenses
- Responsive design that works on all devices
- Real-time updates
- Modern dark theme

## Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla), Bootstrap 5, Bootstrap Icons
- **Backend**: Python (Flask)
- **Database**: MongoDB Atlas
- **Deployment**: Local development setup

---

## API Documentation

### Base URL

http://localhost:5001

pgsql
Copy
Edit

### Endpoints

#### 1️⃣ Get All Expenses

- **URL**: `/expenses`
- **Method**: `GET`
- **Response**:

```json
[
  {
    "_id": "60d5ec9e1c9d440000f2c1a1",
    "description": "Grocery shopping",
    "amount": 1500.50,
    "category": "food",
    "date": "2023-06-20",
    "notes": "Weekly groceries"
  }
]
2️⃣ Add New Expense
URL: /expenses

Method: POST

Request Body:

json
Copy
Edit
{
  "description": "Dinner",
  "amount": 1200,
  "category": "food",
  "date": "2023-06-20",
  "notes": "Dinner with friends"
}
Response:

json
Copy
Edit
{
  "status": "success",
  "expense_id": "60d5ec9e1c9d440000f2c1a1"
}
3️⃣ Update Expense
URL: /expenses/<expense_id>

Method: PUT

Request Body: (Same as POST)

Response:

json
Copy
Edit
{
  "status": "success",
  "message": "Expense updated successfully"
}
4️⃣ Delete Expense
URL: /expenses/<expense_id>

Method: DELETE

Response:

json
Copy
Edit
{
  "status": "success",
  "message": "Expense deleted successfully"
}
Prerequisites
Python 3.8+

MongoDB Atlas account (or local MongoDB instance)

pip (Python package manager)

Setup Instructions
1️⃣ Clone the repository

bash
Copy
Edit
git clone https://github.com/yourusername/personal-expense-tracker.git
cd personal-expense-tracker
2️⃣ Set up a virtual environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3️⃣ Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
4️⃣ Configure environment variables

Create a .env file in the root directory with your MongoDB connection string:

ini
Copy
Edit
MONGO_URI=your_mongodb_connection_string
5️⃣ Run the Flask server

bash
Copy
Edit
python app.py
6️⃣ Open the application

Open templates/index.html in your web browser (or use a local server).

Testing the API
Using cURL
Get all expenses:

bash
Copy
Edit
curl http://localhost:5001/expenses
Add a new expense:

bash
Copy
Edit
curl -X POST http://localhost:5001/expenses \
-H "Content-Type: application/json" \
-d '{
  "description": "Test Expense",
  "amount": 1000,
  "category": "test",
  "date": "2023-06-20",
  "notes": "Sample Note"
}'
Update an expense (replace :id with actual ID):

bash
Copy
Edit
curl -X PUT http://localhost:5001/expenses/:id \
-H "Content-Type: application/json" \
-d '{
  "description": "Updated Expense",
  "amount": 1500,
  "category": "test",
  "date": "2023-06-20",
  "notes": "Updated Note"
}'
Delete an expense (replace :id with actual ID):

bash
Copy
Edit
curl -X DELETE http://localhost:5001/expenses/:id
Screenshots
(Add screenshots of your frontend UI here for better presentation)

Contributing
Contributions are welcome! Feel free to submit a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.

yaml
Copy
Edit

---

✅ **DONE!**

---

If you want, I can also give you:

- **`.gitignore` file content**  
- **`requirements.txt` file content** (if you haven’t created one)  
- **Sample screenshot list you can take**

👉 If you say **“Yes, give me complete final submission package”**, I will give you everything ready-to-go.

Shall I? 🚀