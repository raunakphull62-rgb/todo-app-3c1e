# Todo App Setup Guide
## Introduction
The Todo App is a REST API for managing todo items. This guide will walk you through the steps to set up and run the application.

## Prerequisites
* Python 3.9 or higher
* pip 22.0 or higher
* A Supabase instance
* A JWT secret key

## Step 1: Clone the Repository
Clone the Todo App repository using the following command:
```bash
git clone https://github.com/your-username/todo-app.git
```
## Step 2: Create a .env File
Create a new file named `.env` in the root of the repository. Add the following environment variables:
```makefile
SUPABASE_URL="https://your-supabase-instance.supabase.co"
SUPABASE_KEY="your-supabase-key"
SUPABASE_SECRET="your-supabase-secret"
JWT_SECRET="your-jwt-secret-key"
```
Replace the placeholder values with your actual Supabase instance and JWT secret key.

## Step 3: Install Dependencies
Install the required dependencies using pip:
```bash
pip install -r requirements.txt
```
## Step 4: Run the Application
Run the application using the following command:
```bash
python main.py
```
The application will start on port 8000 by default. You can access the API endpoints by visiting `http://localhost:8000/docs` in your web browser.

## API Endpoints
The Todo App provides the following API endpoints:
* `POST /users`: Create a new user
* `GET /users`: Get a list of all users
* `GET /users/{user_id}`: Get a user by ID
* `POST /todos`: Create a new todo item
* `GET /todos`: Get a list of all todo items
* `GET /todos/{todo_id}`: Get a todo item by ID

## Example Use Cases
* Create a new user: `curl -X POST -H "Content-Type: application/json" -d '{"username": "john", "password": "hello"}' http://localhost:8000/users`
* Get a list of all todo items: `curl -X GET http://localhost:8000/todos`

## Contributing
Contributions to the Todo App are welcome. Please submit a pull request with your changes and a brief description of what you've added or fixed.

## License
The Todo App is licensed under the MIT License. See the LICENSE file for details.