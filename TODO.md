# ✅ Project TODO & Architectural Principles

This file outlines the architectural decisions, development principles, and pending tasks for building and maintaining this full-stack application.

---

## 🧭 Architectural Principles

### 1. **Backend as Modular Flask API**
- Use **Flask App Factory Pattern** via `app/__init__.py`.
- Split all routes into `routes/api/` (JSON) and `routes/web/` (admin HTML).
- Admin tools use **Jinja templates** (e.g., CSV upload), but all user-facing frontend is handled by Vue.

### 2. **Frontend as Decoupled Vue 3 SPA**
- Fully managed in `frontend/`, built with Vite.
- Communicates with backend via REST API (`VITE_API_URL`).
- Built and deployed independently from the backend.

### 3. **Local Development via Docker**
- Docker used **only for local development** (`docker-compose.yml`).
- Scripts in `scripts/` folder automate dev tasks like start/stop/test/setup.

### 4. **Production Deployment to Render (No Docker)**
- Backend is deployed to Render as a Python Web Service.
- Frontend is deployed as a Static Site.
- Database hosted via Render Postgres (managed).

### 5. **Maintainability & Scalability**
- Use **services/** to isolate business logic.
- Use **schemas/** for input validation and serialization.
- Follow API versioning convention in `routes/api/v1/`.

---

## 📦 Folder Purpose Quick Recap

- `backend/app/routes/` – API and admin routes
- `backend/app/models/` – SQLAlchemy DB models
- `backend/app/schemas/` – Data validation rules (Marshmallow/Pydantic)
- `backend/app/services/` – Core logic: DB operations, business rules
- `backend/app/templates/` – Jinja HTML (admin tools only)
- `backend/migrations/` – Alembic migration history
- `backend/tests/` – Unit/integration tests using `pytest`
- `frontend/` – Vue 3 SPA frontend
- `scripts/` – Bash/Python scripts to automate dev/ops tasks
- `docs/` – Internal documentation, API specs, onboarding

---

## 📌 TODO List (Phase 1 – MVP Setup)

### 🔧 Environment & Tooling
- [ ] Set up `.env` files for backend and frontend
- [ ] Configure Dockerfile and `docker-compose.yml` for local dev
- [ ] Create and test `scripts/start.sh`, `scripts/stop.sh`, `scripts/test.sh`

### 🧱 Backend Essentials
- [ ] Implement Flask app factory (`app/__init__.py`)
- [ ] Initialize Flask extensions (`app/extensions.py`)
- [ ] Set up base user model (`models/user.py`)
- [ ] Define user schema (`schemas/user_schema.py`)
- [ ] Add basic user service (`services/user_service.py`)
- [ ] Create `/api/v1/users` GET/POST routes (`routes/api/v1/user_routes.py`)
- [ ] Implement CSV upload route in admin (`routes/web/admin_routes.py`)

### 🧪 Testing & Quality
- [ ] Configure `pytest` and create test fixtures (`tests/conftest.py`)
- [ ] Add test coverage for user endpoints (`tests/test_users.py`)
- [ ] Test CSV upload flow (`tests/test_admin_routes.py`)

### 🎨 Frontend Basics
- [ ] Scaffold Vue 3 project using Vite
- [ ] Set up base routes and views
- [ ] Add API integration layer (e.g., Axios service)
- [ ] Test connection to backend using `VITE_API_URL`

### 📄 Documentation
- [x] **API Routes Documentation** (`backend/app/routes/api/v1/API_ROUTES.md`) - ✅ **COMPLETED**
- [ ] Fill in `docs/onboarding.md` with setup instructions
- [ ] Document API routes in `docs/api_spec.md`
- [ ] Outline project structure in `docs/architecture.md`

---

## 🧠 Nice-to-Have (Later)
- [ ] Add Swagger/OpenAPI UI for internal API testing
- [ ] Add admin authentication
- [ ] Create reusable Postman collection
- [ ] Add frontend CI pipeline (GitHub Actions)
- [ ] Add staging environment support

---

## 📋 Recent Updates

### ✅ Club Management System (COMPLETED)
- **Models**: Clean Club model with Flask-SQLAlchemy
- **Services**: Full ClubService with CRUD operations, search, and business logic
- **Routes**: Thin club routes with proper authentication decorators
- **Schemas**: Marshmallow validation for club data
- **Authentication**: JWT-based auth with `@token_required` and `@admin_required` decorators
- **Documentation**: Comprehensive API routes documentation

### 🔄 Current Focus
- **Authentication**: All routes except login/register require authentication
- **API Structure**: Clean `/api/v1/` versioning with proper URL prefixes
- **Documentation**: Live API documentation in `backend/app/routes/api/v1/API_ROUTES.md`

---
Project structure:

project-root/
│
├── backend/                           # ⚙️ Flask backend app (API + admin tools)
│   ├── app/                           # 📦 Main Flask application package
│   │   ├── __init__.py                # App factory function: creates and configures app
│   │   ├── config.py                  # Environment-specific configuration classes
│   │   ├── extensions.py              # Initialize extensions: SQLAlchemy, Marshmallow, LoginManager, etc.
│   │
│   │   ├── routes/                    # 🌐 HTTP routes (API and Web)
│   │   │   ├── api/                   # 🧩 JSON-based REST API
│   │   │   │   └── v1/                # API versioning
│   │   │   │       ├── user_routes.py        # Example: /api/v1/users endpoints
│   │   │   │       └── item_routes.py        # Example: /api/v1/items endpoints
│   │   │   └── web/                   # 🛠 Admin-only HTML views (Jinja templates)
│   │   │       └── admin_routes.py           # e.g., CSV uploader for data imports
│   │
│   │   ├── models/                    # 🧬 SQLAlchemy models (ORM representations of DB tables)
│   │   │   ├── __init__.py
│   │   │   ├── user.py                       # Standard user model
│   │   │   └── admin_user.py                 # Admin-only or privileged users
│   │
│   │   ├── schemas/                   # 📤📥 Data validation & serialization (Marshmallow or Pydantic)
│   │   │   ├── user_schema.py                # Defines fields exposed for user objects
│   │   │   └── admin_user_schema.py          # Admin-specific serialization rules
│   │
│   │   ├── services/                  # 🧠 Business logic (decoupled from HTTP layer)
│   │   │   ├── user_service.py               # User creation, update, queries
│   │   │   └── admin_service.py              # Admin-only operations, e.g., batch imports
│   │
│   │   └── templates/                # 🖼 Jinja2 templates (used only for admin views)
│   │       └── admin/
│   │           └── upload.html              # Example form: upload CSV for import
│
│   ├── migrations/                   # 🧱 Alembic/Flask-Migrate: DB schema version control
│   │   └── versions/                        # Auto-generated migration scripts
│
│   ├── tests/                        # 🧪 Unit/integration tests (pytest-based)
│   │   ├── __init__.py
│   │   ├── conftest.py                      # Fixtures: app, client, DB setup
│   │   ├── test_users.py                   # Tests for user API routes
│   │   └── test_admin_routes.py            # Tests for admin web tools
│
│   ├── run.py                        # 🚀 App entry point (used by flask or gunicorn)
│   ├── requirements.txt              # 📦 Python dependencies
│   ├── .env                          # 🔐 ENV vars (DB_URL, SECRET_KEY, etc.)
│   └── Dockerfile                    # 🐳 For local development with Docker (not used in production on Render)
│
├── frontend/                         # 🎨 Vue 3 frontend SPA (optional Docker)
│   ├── public/                       # 📁 Static files (index.html, favicon)
│   ├── src/                          # 💡 Source code
│   │   ├── assets/                   # 🎨 Images, styles, fonts
│   │   ├── components/               # 🧩 Reusable Vue components
│   │   ├── views/                    # 📄 Page-level views
│   │   ├── router/                   # 🔀 Vue Router configuration
│   │   ├── store/                    # 📦 State management (Pinia or Vuex)
│   │   ├── App.vue                   # 🧱 Root component
│   │   └── main.js                   # 🚪 Entry point
│   ├── package.json                  # 📦 Node dependencies
│   ├── vite.config.js                # ⚙️ Vite dev/build config
│   ├── .env                          # 🌍 Frontend-specific ENV (e.g., `VITE_API_URL`)
│   └── Dockerfile                    # 🐳 Optional for containerized dev (not used in Render deployment)
│
├── scripts/                          # 🛠 Utility scripts for dev & ops automation
│   ├── start.sh                      # 🔄 Start all services (Docker Compose)
│   ├── stop.sh                       # ⛔ Stop services
│   ├── init_db.sh                    # 🧱 Run migrations, create tables
│   ├── check_health.sh               # ✅ Ping endpoints (e.g., /health) to verify services are up
│   ├── dev_setup.sh                  # 📦 First-time install: set up ENV, install deps
│   ├── test.sh                       # 🧪 Run all backend tests
│   └── import_data.py                # 📂 Manual CSV import or one-off DB operations
│
├── docs/                             # 📚 Developer and API documentation
│   ├── architecture.md               # System design and decisions
│   ├── api_spec.md                   # API contract / OpenAPI (if used)
│   └── onboarding.md                 # Quickstart guide for new devs
│
├── docker-compose.yml                # 🐳 Local orchestration: backend, frontend, postgres
├── .gitignore                        # 🙈 Ignore secrets, compiled files, etc.
└── README.md                         # 📘 Project overview, setup instructions, usage