# 🛒 Cloud-Store

**Cloud-Store** is a single-vendor e-commerce web application built with **Django** and **MySQL**, designed with production-grade backend architecture, security best practices, and test-driven development.

This project represents a complete **Minimum Viable Product (MVP)** and serves as a real-world Django deployment case study.

---

```
E-Commerce/
├── README.md
├── requirements.txt
└── ecommerce/
    ├── manage.py
    ├── pytest.ini
    │
    ├── ecommerce/
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    │
    ├── users/
    │   ├── admin.py
    │   ├── apps.py
    │   ├── backends.py
    │   ├── models.py
    │   ├── urls.py
    │   ├── views.py
    │   ├── templates/users/
    │   │   ├── login.html
    │   │   └── signup.html
    │   └── tests/
    │       ├── test_login_view.py
    │       ├── test_logout_view.py
    │       └── test_signup_view.py
    │
    ├── products/ 
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── urls.py
    │   ├── views.py
    │   ├── templates/products/
    │   │   ├── home.html
    │   │   └── product.html
    │   └── tests/
    │       ├── test_home_view.py
    │       ├── test_models.py
    │       └── test_product_view.py
    │
    ├── cart/
    │   ├── context_processors.py
    │   ├── services.py
    │   ├── urls.py
    │   ├── views.py
    │   ├── templates/cart/cart.html
    │   └── tests/
    │       ├── test_services.py
    │       └── test_views.py
    │
    ├── orders/
    │   ├── models.py
    │   ├── services.py
    │   ├── urls.py
    │   ├── views.py
    │   ├── templates/orders/
    │   │   ├── confirmation.html
    │   │   ├── detail.html
    │   │   └── list.html
    │   └── tests/
    │       ├── test_models.py
    │       ├── test_services.py
    │       └── test_views.py
    │
    ├── templates/
    │   └── base.html
    │
    ├── static/
    └── media/
```

## 🚀 Tech Stack

- **Backend:** Django 6.0  
- **Database:** MySQL  
- **Authentication:** Django Authentication System  
- **Frontend:** Django Templates  
- **Testing:** Pytest + pytest-django  
- **Configuration:** Environment-based settings using `django-environ`  
- **Deployment Target:** Azure App Service  

---

## ▶️ Running Locally

```bash
# Clone the repository
git clone https://github.com/Bharat-Panchal-3578/Cloud-Store.git
cd Cloud-Store

# Create virtual environment
python -m venv env
source env\scripts\activate  # Linux: env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

## ✅ Core Features (MVP)

- Product listing & detail pages  
- Session-based cart system  
- User authentication (login, logout, signup)  
- Order placement & order history  
- Admin management for products and orders  
- Media handling for product images  
- Production-ready security configuration  

---

## 🔐 Security & Production Readiness

- Environment-based secret management
- Secure cookies & CSRF protection
- HTTPS enforcement (production)
- HSTS configuration
- Proxy-aware SSL handling (Azure compatible)

---

## 🧪 Testing & Quality

- Comprehensive unit and integration tests
- Service-layer testing for cart and order logic
- View-level testing with authentication coverage
- All tests passing (`pytest -v`)
- Deployment readiness verified using:
```bash
    python manage.py check --deploy
```

## 📌 Project Status

### 🟢 MVP Complete
### 🚀 Deployment in Progress

### Planned future enhancements:

- Payment gateway integration
- REST APIs
- JWT-based authentication
- Frontend styling & UI improvements
- Performance optimizations (caching, rate limiting)

---

## 📌 Notes

- This project is being developed incrementally with a strong focus on backend design.
- APIs, JWT authentication, and production deployment will be added in later phases.

---

## 📄 License

No license has been applied yet. This project is under active development.