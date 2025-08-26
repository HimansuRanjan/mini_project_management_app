# Mini Project Management System (Django + GraphQL + React)

## Overview
This is a full-stack mini project management system demonstrating:
- Multi-tenancy (organization-based isolation)
- GraphQL API with Django + Graphene
- PostgreSQL database (Dockerized)
- React frontend with TypeScript, Apollo Client, and TailwindCSS

---

## 🚀 Backend Setup (Django + GraphQL)

### Prerequisites
- Python 3.10+
- Docker & Docker Compose
- Node.js (for frontend, later)

### Steps
1. Clone repo
   ```bash
   git clone <repo-url>
   cd project_mgmt

2. Create virtual environment
    ```bash
    python -m venv venv
    source venv/bin/activate     # On Windows: venv\Scripts\activate


3. Install dependencies
    ```bash
    pip install -r requirements.txt


4. Start PostgreSQL with Docker
    ```bash
    docker-compose up -d


5. Apply migrations
    ```bash
    python manage.py makemigrations
    python manage.py migrate


6. Start development server
    ```bash
    python manage.py runserver

🔗 Endpoints

Admin Panel: http://127.0.0.1:8000/admin/

GraphQL Playground: http://127.0.0.1:8000/graphql/