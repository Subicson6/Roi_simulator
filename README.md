Invoicing ROI Simulator
This is a full-stack web application that helps users visualize the cost savings and Return on Investment (ROI) when switching from manual to automated invoicing. The frontend is built with React, and the backend is a REST API built with Python and Flask.

📂 Project Structure
The project is organized into two main parts: a backend API and a frontend client.

.
├── 📂 backend/
│   ├── app.py
│   ├── logic.py
│   ├── models.py
│   └── ...
└── 📂 frontend/
    ├── src/
    │   ├── App.jsx
    │   └── ...
    └── index.html
    
💻 Technologies Used
Frontend: React (with Vite), JavaScript, Axios

Backend: Python, Flask, Flask-SQLAlchemy

Database: MySQL

🚀 Getting Started
Follow these instructions to get the project running on your local machine.

Prerequisites
Make sure you have the following installed:

Node.js (which includes npm)

Python

A running [suspicious link removed]

1. Backend Setup
First, get the Python server running.

Navigate to the backend folder:

Bash

cd backend
Create a virtual environment:

Bash

# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
Install dependencies:

Bash

pip install -r requirements.txt
Set up the database:

Log in to MySQL and create a new database.

SQL

CREATE DATABASE roi_calculator;
Create a .env file in the backend folder and add your database connection URL (remember to URL-encode any special characters in your password, like @ becoming %40).

DATABASE_URL="mysql+mysqlconnector://your_user:your_password@localhost/roi_calculator"
Run the server:

Bash

python app.py
The backend will now be running at http://127.0.0.1:5000. Keep this terminal open.

2. Frontend Setup
Now, get the React user interface running in a new terminal.

Open a new terminal window.

Navigate to the frontend folder:

Bash

cd frontend
Install dependencies:

Bash

npm install
Run the development server:

Bash

npm run dev
The frontend will now be running at http://localhost:5173. Open this URL in your web browser to use the application.

⚙️ API Endpoints
The backend provides the following endpoints:

Method	Endpoint	Description
POST	/simulate	Runs a simulation calculation.
POST	/scenarios	Saves a new scenario.
GET	/scenarios	Retrieves all saved scenarios.
GET	/scenarios/<id>	Retrieves a single scenario.
PUT	/scenarios/<id>	Updates an existing scenario.
DELETE	/scenarios/<id>	Deletes a scenario.
POST	/report/generate	Generates a downloadable PDF report.


✨ Features
Interactive Calculator: A dynamic form to calculate ROI in real-time.

Favorable Logic: Internal constants ensure calculations always favor automation.

Full CRUD for Scenarios: Users can create, read, update, and delete named scenarios, which are persisted in a MySQL database.

Gated Report Generation: A downloadable PDF report is available after providing an email address for lead capture.
