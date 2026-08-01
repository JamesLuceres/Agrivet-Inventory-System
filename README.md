# Nichole Agrivet - POS & Inventory Management System

A Point-of-Sale (POS) and inventory management system designed for **Nichole Agrivet**, featuring bulk/retail item unit tracking, fast checkout, customer credit (utang) ledger tracking, profit margin calculations, and monthly sales reports.

---

## 🛠️ Project Structure
- `frontend/` - Vue 3 + Quasar SPA Frontend (Vite)
- `backend/` - Django REST Framework API Backend

---

## 🚀 Local Setup & Development

### 1. Backend (Django REST API)
```bash
cd backend
python -m venv .venv
# Activate environment (Windows)
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
Backend API will run at `http://127.0.0.1:8000/api/`

### 2. Frontend (Vue 3 + Quasar)
```bash
cd frontend
npm install
npm run dev
```
Frontend Web App will run at `http://localhost:9000/`

---

## 🌐 Online Deployment (Vercel & Render)

### 1. Backend (Render / Railway)
- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements.txt && python manage.py migrate`
- **Start Command**: `gunicorn core.wsgi:application`

### 2. Frontend (Vercel)
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `dist/spa`
- **Environment Variable**: `VITE_API_URL` = `https://<your-backend-domain>/api/`
