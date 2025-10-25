# 🚀 Team Workspace - Real-time Project Management System

![Django](https://img.shields.io/badge/Django-4.2.7-green)
![Channels](https://img.shields.io/badge/Channels-4.0.0-blue)
![WebSocket](https://img.shields.io/badge/WebSocket-Real--time-orange)
![Python](https://img.shields.io/badge/Python-3.11%2B-yellow)

A powerful real-time team collaboration platform built with **Django** and **Django Channels**, featuring project management, task tracking, and live chat capabilities.

---

## ✨ Features

### 🎯 Core Functionality
- 📂 **Project Management** – Create and organize team projects  
- ✅ **Task Tracking** – Assign tasks with priorities and statuses  
- 💬 **Real-time Chat** – Instant messaging powered by WebSockets  
- 👥 **Team Collaboration** – Multi-user project environments  

### 🔥 Real-time Capabilities
- Live task status updates  
- Instant messaging between team members  
- Real-time notifications  
- Seamless WebSocket connections  

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-------------|
| **Backend** | Django 4.2.7 + Django Channels |
| **Frontend** | HTML5, Tailwind CSS, JavaScript |
| **Real-time** | WebSocket, ASGI |
| **Database** | SQLite (PostgreSQL ready for production) |
| **Authentication** | Django Auth System |

---

## 📸 Screenshots

administration Page:

<img width="1857" height="548" alt="Screenshot From 2025-10-21 14-33-56" src="https://github.com/user-attachments/assets/b2800d99-34a3-4c06-84e3-717a9fc9eb24" />

Dark mode:

<img width="1857" height="548" alt="Screenshot From 2025-10-21 14-34-04" src="https://github.com/user-attachments/assets/c25173bf-2810-4185-b251-1f368f0c3701" />

add group Page:

<img width="1847" height="696" alt="Screenshot From 2025-10-21 14-34-26" src="https://github.com/user-attachments/assets/92ca1ac6-eb56-4c69-9b9b-459dea5c5ccd" />

add user Page:

<img width="1847" height="696" alt="Screenshot From 2025-10-21 14-34-33" src="https://github.com/user-attachments/assets/851559dc-74e7-4911-afa5-dd6c83dba174" />

add chat message Page:

<img width="1847" height="696" alt="Screenshot From 2025-10-21 14-34-38" src="https://github.com/user-attachments/assets/a15d1bc1-ace1-4666-9378-4ed76916e463" />

add project Page:

<img width="1843" height="803" alt="Screenshot From 2025-10-21 14-34-56" src="https://github.com/user-attachments/assets/5f173f7e-a719-482e-8769-a6d53636a8a0" />

add task Page:

<img width="1844" height="901" alt="Screenshot From 2025-10-21 14-35-05" src="https://github.com/user-attachments/assets/01c46c2e-3017-4584-a2fa-373dc1e4daa0" />

---

## 🚀 Quick Start

### 🧩 Prerequisites
- Python 3.11+
- Redis (for production)

### ⚙️ Installation

```bash
# Clone the repository
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

Access the application:  
- Main App → http://127.0.0.1:8000  
- Admin Panel → http://127.0.0.1:8000/admin  

---

## 🏗️ Project Structure

```
team_workspace/
├── workspace/          # Django project settings
├── projects/           # Project management app
├── tasks/              # Task tracking app
├── chat/               # Real-time chat app
├── templates/          # HTML templates
└── static/             # Static files
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
# In settings.py
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

This project demonstrates advanced **Django Channels** implementation:
- WebSocket Consumers for real-time communication  
- Channel Layers for handling multiple connections  
- Async support for high-performance messaging  
- Group Management for project-based chat rooms  

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

- User registration and authentication  
- Project-based team membership  
- Role-based permissions *(planned)*  
- User profile management  

---

## 🚀 Deployment

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

We welcome contributions! Please feel free to submit pull requests, report bugs, or suggest new features.

```bash
# Steps
1. Fork the project
2. Create your feature branch: git checkout -b feature/AmazingFeature
3. Commit your changes: git commit -m 'Add some AmazingFeature'
4. Push to the branch: git push origin feature/AmazingFeature
5. Open a Pull Request
```

---


## 🙏 Acknowledgments

- Django and Django Channels teams  
- Tailwind CSS for amazing styling  
- WebSocket technology for real-time features  

---

## 📞 Support

If you have any questions or need help with setup, please open an **issue** or contact the development team.  
⭐ Don’t forget to **star this repository** if you find it helpful!
