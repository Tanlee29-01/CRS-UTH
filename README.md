# Course Registration System — UTH Portal

Hệ thống Đăng ký Học phần dành cho sinh viên UTH, gồm **Backend** (FastAPI + PostgreSQL) và **Frontend** (React + Vite).

## Live Demo

| Service | URL |
|---------|-----|
| Frontend | `https://crs-uth.vercel.app` |
| Backend API | `https://crs-backend-xxxx.onrender.com` |
| API Docs | `https://crs-backend-xxxx.onrender.com/docs` |

> Thay `xxxx` bằng tên project thực tế trên Render sau khi deploy.

## Tính năng

| Role | Chức năng |
|------|-----------|
| **Student** | Đăng ký / hủy học phần, waitlist tự động, giỏ đăng ký + validate, xem thời khóa biểu, ước tính học phí, dashboard thông tin sinh viên, tiến độ tín chỉ |
| **Instructor** | Xem danh sách lớp (roster), xuất CSV |
| **Admin** | CRUD khoa/môn/HK/lớp/quy tắc, báo cáo, nhập CSV, quản lý sinh viên |

## Tài khoản test

| Email | Mật khẩu | Role |
|-------|-----------|------|
| `admin@example.com` | `AdminPass123!` | admin |
| `student@example.com` | `StudentPass123!` | student |

---

## 🚀 Deploy lên web miễn phí

### Bước 1: Push code lên GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/CRS.git
git push -u origin main
```

### Bước 2: Deploy Backend lên Render.com (Free)

1. Vào [render.com](https://render.com) → Đăng ký (dùng GitHub)
2. **Tạo PostgreSQL Database:**
   - Dashboard → **New** → **PostgreSQL**
   - Name: `crs-db`
   - Plan: **Free**
   - → **Create Database**
   - Chờ tạo xong → Copy **External Database URL** (dạng `postgres://user:pass@host/dbname`)

3. **Tạo Web Service:**
   - Dashboard → **New** → **Web Service**
   - Kết nối GitHub repo `CRS`
   - Cấu hình:

   | Field | Value |
   |-------|-------|
   | Name | `crs-backend` |
   | Region | Singapore (hoặc gần nhất) |
   | Runtime | **Python 3** |
   | Root Directory | `backend` |
   | Build Command | `pip install -r requirements.txt` |
   | Start Command | `alembic upgrade head && python -m app.seed && uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
   | Plan | **Free** |

4. **Thêm Environment Variables** (tab Environment):

   | Key | Value |
   |-----|-------|
   | `DATABASE_URL` | *(paste External Database URL từ bước 2)* |
   | `SECRET_KEY` | *(tạo chuỗi ngẫu nhiên, VD: `my-super-secret-key-abc123`)* |
   | `FRONTEND_ORIGIN` | `https://crs-uth.vercel.app` |
   | `PYTHONPATH` | `/opt/render/project/src/backend` |
   | `APP_ENV` | `production` |
   | `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` |
   | `MAX_CREDITS_PER_TERM` | `18` |
   | `CREDIT_RATE` | `300` |
   | `RATE_LIMIT_PER_MINUTE` | `120` |

5. → **Create Web Service** → Chờ build xong
6. Kiểm tra: `https://crs-backend-xxxx.onrender.com/health` → `{"status":"ok"}`

### Bước 3: Deploy Frontend lên Vercel (Free)

1. Vào [vercel.com](https://vercel.com) → Đăng ký (dùng GitHub)
2. **Import Project** → Chọn repo `CRS`
3. Cấu hình:

   | Field | Value |
   |-------|-------|
   | Framework Preset | **Vite** |
   | Root Directory | `frontend` |
   | Build Command | `npm run build` |
   | Output Directory | `dist` |

4. **Environment Variables:**

   | Key | Value |
   |-----|-------|
   | `VITE_API_BASE_URL` | `https://crs-backend-xxxx.onrender.com` |

   > Thay URL bằng URL thực tế của backend trên Render.

5. → **Deploy** → Chờ build xong
6. Truy cập: `https://crs-uth.vercel.app` (hoặc URL Vercel cấp)

### Bước 4: Cập nhật CORS (nếu cần)

Sau khi có URL frontend thực tế từ Vercel, quay lại Render → Environment Variables → cập nhật `FRONTEND_ORIGIN` thành URL chính xác.

---

## Cấu trúc dự án

```
CRS/
├── backend/
│   ├── app/
│   │   ├── api/routes/     # auth, admin, catalog, enrollment, instructor, notifications, health
│   │   ├── core/           # config, security (JWT + bcrypt)
│   │   ├── db/             # SQLAlchemy engine & session
│   │   ├── models/         # 17 ORM models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # CSV import
│   │   └── seed.py         # Dữ liệu mẫu
│   ├── alembic/            # Database migrations
│   ├── tests/              # pytest
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/     # Header, LoginPage, Dashboard, CatalogPanel, AdminPanel, ...
│   │   ├── api/client.js   # API client (fetch + JWT)
│   │   ├── App.jsx         # Main SPA
│   │   └── styles.css      # UTH teal theme
│   ├── vercel.json
│   └── package.json
├── render.yaml             # Render Blueprint (optional)
├── Dockerfile.backend
├── docker-compose.yml
└── SPEC.md
```

## API Endpoints

| Method | Path | Mô tả |
|--------|------|-------|
| `POST` | `/auth/register` | Đăng ký |
| `POST` | `/auth/login` | Đăng nhập → JWT |
| `GET` | `/auth/me` | User hiện tại |
| `GET` | `/auth/me/profile` | Profile + student info |
| `GET` | `/departments` | Danh sách khoa |
| `GET` | `/courses` | Danh sách môn |
| `GET` | `/terms` | Danh sách học kỳ |
| `GET` | `/sections` | Lớp học phần |
| `POST` | `/sections/{id}/enroll` | Đăng ký lớp |
| `POST` | `/sections/{id}/drop` | Hủy đăng ký |
| `GET` | `/me/enrollments` | Lớp đã đăng ký |
| `POST` | `/cart/validate` | Validate giỏ |
| `POST` | `/billing/estimate` | Ước tính phí |
| `GET` | `/notifications` | Thông báo |
| `POST` | `/admin/*` | Quản trị |
| `GET` | `/health` | Health check |

## Chạy local (tùy chọn)

```bash
# Backend
cd backend
pip install -r requirements.txt
alembic upgrade head
python -m app.seed
uvicorn app.main:app --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

## Tech Stack

- **Backend**: Python 3.12, FastAPI, SQLAlchemy 2, Alembic, PostgreSQL, JWT
- **Frontend**: React 18, Vite, vanilla CSS (UTH teal theme)
- **Deploy**: Render (backend + DB) + Vercel (frontend)
