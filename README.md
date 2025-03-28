# Academic-GUARD

## Academic & Performance Management System
A Django-based web application designed to streamline academic management for senior high school students preparing for national examinations. This system addresses challenges such as managing transcripts, correcting errors in academic records, and providing AI-driven performance predictions. It features three distinct user panels: Admin, Teacher, and Student, with role-based authentication and PDF transcript handling.

## Features
### General
- Role-Based Authentication: Separate access for Admin, Teachers, and Students.
- Responsive Design: Built with Bootstrap for a professional, mobile-friendly interface.
- Static Assets: Custom CSS and JS served from the assets/ directory.
- File Uploads: Supports PDF uploads for transcripts and report cards.
### Admin Panel
- Add, update, and delete students and teachers.
- Upload PDF transcripts and national exam results.
- View AI-driven performance predictions and statistics (e.g., total students, average marks).
- Dashboard with Chart.js visualizations (e.g., bar charts for predictions).
### Student Panel
- View personal transcripts and extracted marks from PDFs.
- Submit claims for mark corrections.
- Download or view uploaded PDF transcripts.
### Teacher Panel
- Correct marks based on student claims or errors in transcripts.
- View a history of mark corrections.
- Access performance dashboards for classes taught.
### AI Features
- Predict student performance (1, 3, 5 years) using Linear Regression.
- Identify at-risk students based on historical data.
- Visualize predictions with Chart.js.
### Tech Stack
- Backend: Django 4.x with PostgreSQL
- Frontend: Django Templates, Bootstrap 4, Chart.js
- AI/ML: Scikit-learn, Pandas, NumPy
- PDF Processing: pdfplumber for extracting marks from PDF transcripts
- Static Assets: Custom CSS/JS in assets/
- Forms: Django Crispy Forms (Bootstrap 4)
### Project Structure
---
```
school_management/
├── school_management/      # Main project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── admin_app/             # Admin-specific logic
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── student_app/           # Student-specific logic
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── teacher_app/           # Teacher-specific logic
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── templates/             # HTML templates
│   ├── base.html
│   ├── admin/
│   ├── student/
│   └── teacher/
├── assets/                # Static files (CSS, JS)
│   ├── css/
│   ├── js/
│   └── images/
├── media/                 # Uploaded files (PDFs, images)
└── manage.py
```
---
Installation
Clone the Repository (if applicable):
bash

Collapse

Wrap

```
git clone <repository-url>
cd school_management
```
Create a Virtual Environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
Install Dependencies:
pip install 
```
pip install django psycopg2-binary scikit-learn pandas numpy django-crispy-forms pdfplumber
```

## Frontend Part
![image](https://github.com/user-attachments/assets/99e82428-4b2a-4cf0-8cb5-4d7dfd023462)
![image](https://github.com/user-attachments/assets/c49f5806-30f9-42c8-82a8-938fa8cf1e25)



