# 🚀 ToolNest

**ToolNest** is a secure, modular, and fully private personal dashboard built with **Next.js** and **Django REST Framework**.

Track your entire life in one place:

* ✅ Todos & goals
* 💸 Daily expenses
* 📈 Stock market earnings
* 📅 Schedules & life routines
* 🔐 PIN-secured access (no external login)

> ToolNest is crafted for devs who want total privacy, zero noise, and full control over their productivity — across devices, with real-time sync.

---

## 🛠️ Tech Stack

| Layer    | Technology                              |
| -------- | --------------------------------------- |
| Frontend | **Next.js** (React, TypeScript)         |
| Backend  | **Django REST Framework**               |
| Database | **PlanetScale** (MySQL) or SQLite (dev) |
| Auth     | Custom PIN-based auth (session/token)   |
| DevOps   | GitHub Codespaces, Railway (optional)   |
| API Docs | DRF + Swagger (`drf-yasg`)              |

---

## 📆 Key Features

* Modular micro-apps (Todos, Earnings, Schedule, etc.)
* Secure PIN-only authentication
* Auto-generated Swagger & ReDoc API docs
* Lightweight, scalable backend
* Subdomain-ready (e.g. `todos.toolnest.com`)
* Local dev & full production-ready setup

---

## 🌐 Deployment Goals

* ✅ Fully free hosting (custom domain ready)
* 🔧 Frontend: Vercel, Netlify, or static build
* 🐍 Backend: Render, Railway, or Codespace tunnel
* 🦰 DB: PlanetScale (prod), SQLite (dev/test)
* 🔒 No external login or OAuth

---

## ⚙️ Structure (Planned)

```
ToolNest/
├── frontend/            # Next.js app
├── backend/             # Django project
│   ├── main/            # DRF main app
│   ├── users/           # (Optional) future auth module
│   └── toolnest_backend/
├── .env                 # Centralized config
├── README.md
└── requirements.txt
```

---

## 🕵️‍♂️ Security Philosophy

* PIN-secured local sessions
* No third-party login
* Ideal for personal dashboards, planners, or dev tools
* Subdomain-ready for micro-tools:
  e.g. `earnings.toolnest.com`, `todos.toolnest.com`

---

## 📚 API Documentation

Once running, access:

* Swagger: `{BASE URL}/v1/docs/`
* Redoc: `{BASE URL}/v1/redoc/`

---

---

> Built by [@jatin7425](https://github.com/jatin7425) with vision, clarity, and zero distractions.
