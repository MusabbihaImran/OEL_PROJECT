# Hotel Management System

A Python-based Hotel Management System developed as a university project, featuring both a desktop application and a web interface.

The project combines a **Tkinter desktop application** with a **Flask-based web application**, using SQLite for data storage and Docker for containerized deployment.

## ✨ Features

### 🖥️ Desktop Application

The desktop application is built with Python and Tkinter and includes:

* Hotel booking and room management
* Graphical user interface
* SQLite database integration
* Service and business-logic layer
* Database models
* Input validation and reusable utilities
* Automated database initialization
* Unit tests

### 🌐 Web Application

The project also includes a Flask-based web interface with:

* Web-based hotel management functionality
* HTML templates
* Flask application backend
* Separate web dependencies

### 🐳 Docker

The repository includes Docker configuration for containerized deployment of the project.

## 🛠️ Technologies

* **Python**
* **Tkinter** — desktop GUI
* **Flask** — web application
* **SQLite** — database
* **unittest** — automated testing
* **Docker** — containerization
* **HTML/CSS** — web interface

## 📁 Project Structure

```text
OEL_PROJECT/
│
├── tkinter_app/
│   ├── app/
│   │   ├── models/
│   │   ├── services/
│   │   ├── utils/
│   │   └── views/
│   ├── tests/
│   ├── schema.sql
│   ├── requirements.txt
│   └── README.md
│
├── web/
│   ├── templates/
│   ├── app.py
│   └── requirements_web.txt
│
├── Dockerfile
├── .dockerignore
├── LICENSE
└── README.md
```

## 🚀 Desktop Application Setup

Navigate to the desktop application:

```bash
cd tkinter_app
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python -m app.main
```

The SQLite database is initialized automatically when the application is first run.

## 🧪 Running Tests

From the `tkinter_app` directory:

```bash
python -m unittest discover tests
```

## 🌐 Web Application

Navigate to the web application:

```bash
cd web
```

Install the web dependencies:

```bash
pip install -r requirements_web.txt
```

Then run the Flask application using the project's web configuration.

## 🐳 Docker

The repository includes a `Dockerfile` and `.dockerignore` for containerized deployment.

Build the Docker image with:

```bash
docker build -t hotel-management-system .
```

Run the container according to the application's configured port and deployment settings.

## 🎓 Project Context

This project was developed as part of university coursework to implement a hotel booking and room management system using Python.

The project includes multiple application interfaces and supporting technologies, allowing the same project to be explored through a desktop GUI and a web application while incorporating database management, testing, and containerization.

## 📌 Status

Completed university project maintained as part of my software development portfolio.

