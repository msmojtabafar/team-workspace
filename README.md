# 🚀 Team Workspace - Real-time Project Management System

![Django](https://img.shields.io/badge/Django-4.2.7-green)
![Channels](https://img.shields.io/badge/Channels-4.0.0-blue)
![WebSocket](https://img.shields.io/badge/WebSocket-Real--time-orange)
![Python](https://img.shields.io/badge/Python-3.11%2B-yellow)

A powerful **real-time team collaboration platform** built with **Django** and **Django Channels**, featuring project management, task tracking, and live chat capabilities.

---

## ✨ Features

### 🎯 Core Functionality
- 📂 **Project Management** – Create and organize projects
- ✅ **Task Tracking** – Assign and monitor tasks with priorities and statuses
- 💬 **Real-time Chat** – Instant messaging powered by WebSockets
- 👥 **Team Collaboration** – Multi-user environments for productivity

### ⚡ Real-time Capabilities
- Live task status updates
- Instant messaging between members
- Real-time notifications
- Seamless WebSocket connections

### 📱 PWA (Progressive Web App)
- Installable on desktop & mobile devices
- Works offline using service workers
- Dynamic caching for performance
- Background push notifications

### 🔔 Push Notifications
- Receive live alerts for new tasks, messages, and updates
- Configurable via browser notifications
- Built with **pywebpush** and **service workers**

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-------------|
| **Backend** | Django 4.2.7 + Django Channels |
| **Frontend** | HTML5, Tailwind CSS, JavaScript |
| **Real-time** | WebSocket, ASGI |
| **Database** | SQLite (PostgreSQL-ready) |
| **Authentication** | Django Auth System |
| **PWA & Notifications** | Service Worker, pywebpush |

---

## 📸 Screenshots

**Administration Page:**  
![Admin](https://github.com/user-attachments/assets/b2800d99-34a3-4c06-84e3-717a9fc9eb24)

**Dark Mode:**  
![Dark Mode](https://github.com/user-attachments/assets/c25173bf-2810-4185-b251-1f368f0c3701)

**Add Project / Task / Chat Pages:**  
![Project](https://github.com/user-attachments/assets/5f173f7e-a719-482e-8769-a6d53636a8a0)
![Task](https://github.com/user-attachments/assets/01c46c2e-3017-4584-a2fa-373dc1e4daa0)

---

## 🚀 Quick Start

### 🧩 Prerequisites
- Python 3.11+
- Redis (for production)

### ⚙️ Installation

```bash
git clone https://github.com/yourusername/team-workspace.git
cd team-workspace
```

#### Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate    # Windows
```

#### Install dependencies
```bash
pip install -r requirements.txt
```

#### Setup database
```bash
python manage.py migrate
python manage.py createsuperuser
```

#### Run development server
```bash
python manage.py runserver
```

Access the app:
- Main: http://127.0.0.1:8000  
- Admin: http://127.0.0.1:8000/admin

---

## 🏗️ Project Structure

```
team_workspace/
├── workspace/          # Django settings
├── projects/           # Project management app
├── tasks/              # Task tracking app
├── chat/               # Real-time chat app
├── templates/          # HTML templates
└── static/             # Static files & service workers
```

---

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:
```
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database Setup (Production)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'team_workspace',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 🌐 Real-time Features
- WebSocket Consumers for async communication
- Channel Layers for multiple connections
- Async task & message updates
- Group-based chat rooms

---

## 🎯 API Endpoints

| Method | Endpoint | Description |
|--------|-----------|-------------|
| GET | `/projects/` | List user projects |
| GET | `/projects/{id}/` | Project details |
| POST | `/projects/{id}/` | Create new task |
| WS | `/ws/projects/{id}/` | Real-time project updates |
| WS | `/ws/chat/{id}/` | Real-time chat |

---

## 👥 User Management
- User registration & authentication
- Team-based permissions
- Role-based access *(planned)*
- Profile management

---

## 📦 Deployment

### Using Docker (Recommended)
```bash
docker-compose up --build
```

### Manual Deployment
```bash
python manage.py collectstatic
python manage.py migrate
gunicorn workspace.asgi:application -k uvicorn.workers.UvicornWorker
```

---

## 🤝 Contributing
We welcome contributions!  
Follow these steps:
```bash
git checkout -b feature/AmazingFeature
git commit -m 'Add some AmazingFeature'
git push origin feature/AmazingFeature
```
Then open a Pull Request.

---

## 🙏 Acknowledgments
- Django & Django Channels team
- Tailwind CSS for styling
- WebSocket technology for real-time updates
- pywebpush for push notifications

---

## ⭐ Support
If you find this project helpful, please **star** it on GitHub!  
For issues or questions, open an **Issue** in the repository.
