# CareerTracker — Job Application & Recruiter Follow-up Platform

CareerTracker is a web application built with **FastAPI and Python** to help users organize their job search. It provides API endpoints for managing job-search data and a web interface for viewing information through a dashboard.

The project combines backend API development, database integration, authentication, and frontend development using HTML, CSS, and Jinja2 templates.

## Features

- **User Authentication:** User login with password verification and session management for the web interface.
- **Dashboard:** View job application information and application status summaries.
- **Company Management:** Organize company information.
- **Job Management:** Manage job listings and related details.
- **Application Tracking:** Track job applications and their statuses.
- **Interview Management:** Organize interview information.
- **Contact Management:** Store recruiter and professional contact information.
- **Protected Frontend Pages:** Require login to access the frontend.
- **Logout:** Clear the user's session and redirect to the login page.
- **REST API:** Backend endpoints built with FastAPI.
- **Database Integration:** Store and retrieve information using PostgreSQL and SQLAlchemy.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API development |
| SQLAlchemy | Database ORM |
| PostgreSQL | Relational database |
| Pydantic | Data validation and API schemas |
| HTML | Web page structure |
| CSS | Styling and responsive layout |
| Jinja2 | Server-rendered HTML templates |
| JavaScript | Frontend interactions |
| Uvicorn | ASGI server |
| Postman | API testing |
| Git and GitHub | Version control and project hosting |

## Project Structure

```text
CareerTracker/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── dependencies.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── companies.py
│   │   ├── jobs.py
│   │   ├── applications.py
│   │   ├── interviews.py
│   │   └── contacts.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── navbar.html
│   │   ├── login.html
│   │   └── dashboard.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── main.js
├── .gitignore
└── README.md
```

*Note: The structure above represents the main files and folders; your local project may contain additional files.*

## Getting Started

### Prerequisites

Install or prepare the following:

- Python 3.13 or a compatible Python version
- PostgreSQL
- PyCharm or another Python editor
- Git (optional, for version control)

### 1. Clone the repository

```bash
git clone https://github.com/Aditir17/CareerTracker.git
cd CareerTracker
```

Alternatively, open your existing project folder in PyCharm.

### 2. Create and activate a virtual environment

Create the environment:

```bash
python -m venv .venv
```

On Windows PowerShell, activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Install the packages required by your project. If you have a `requirements.txt` file, run:

```bash
pip install -r requirements.txt
```

If you do not have this file yet, install the dependencies listed in your project's imports and configuration.

### 4. Configure PostgreSQL

Create a PostgreSQL database and configure your database connection in the project's database configuration.

Keep database credentials and secret keys out of public source code. Use environment variables or a local environment file excluded from Git.

### 5. Start the application

Run the following command from the project root directory:

```bash
uvicorn app.main:app --reload
```

The application should start on your local machine.

## Access the Application

Once the server is running, open:

| Page | URL |
|---|---|
| Frontend login | http://127.0.0.1:8000/frontend/login |
| Dashboard | http://127.0.0.1:8000/frontend |
| API documentation | http://127.0.0.1:8000/docs |
| Alternative API documentation | http://127.0.0.1:8000/redoc |

Log in with an existing registered account to access protected frontend pages.

## API Testing

The API can be explored and tested using:

- **Swagger UI:** Interactive API documentation available at `/docs`.
- **Postman:** Send HTTP requests and verify responses, status codes, and authentication behavior.

The project includes API routers for authentication, companies, jobs, applications, interviews, and contacts.

## Learning Outcomes

This project provides practical experience with:

- Building REST APIs using FastAPI.
- Working with PostgreSQL and SQLAlchemy.
- Defining database models and validation schemas.
- Implementing password verification and authentication.
- Managing browser sessions and protected pages.
- Rendering dynamic HTML using Jinja2.
- Styling web pages using CSS.
- Testing APIs using Postman.
- Managing code using Git and GitHub.

## Future Improvements

Potential enhancements include:

- More complete frontend create, read, update, and delete workflows.
- Improved filtering and search for job applications.
- Automated recruiter follow-up reminders.
- Unit and integration tests using Pytest.
- Deployment and containerization with Docker.

## Author

**Aditi Lohokare**

GitHub: [Aditir17](https://github.com/Aditir17)

LinkedIn: [Aditi Lohokare](https://www.linkedin.com/in/aditi-lohokare-5a7806135/)

---

*CareerTracker is a learning and portfolio project focused on Python backend development and full-stack web application fundamentals.*
