
# Student Management System

## About the Project
A web-based Student Management System developed using Python, FastAPI, SQLite, HTML and CSS.

The application allows users to manage student records through a simple web interface.

## Features
- Add new student records
- View all students
- Edit student details
- View individual student information
- Store student data using SQLite

## Technologies Used
- Python
- FastAPI
- SQLite
- HTML
- CSS
- Jinja2

## Project Structure
```text
student_management/
│
├── main.py
├── templates/
│   ├── home.html
│   ├── add-std.html
│   ├── edit-std.html
│   └── single-std.html
│
└── .gitignore
```

## Installation and Execution

1. Clone the repository:

```bash
git clone https://github.com/divyak1234/Student-Management-System.git
```

2. Navigate to the project folder:

```bash
cd student_management
```

3. Install dependencies:

```bash
pip install fastapi uvicorn jinja2 python-multipart
```

4. Run the application:

```bash
uvicorn main:app --reload
```

5. Open your browser:

```text
http://127.0.0.1:8000
```

## Author
Divya
