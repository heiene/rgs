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
