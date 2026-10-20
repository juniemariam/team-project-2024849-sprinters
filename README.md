[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Fu_pncF5)

# Team Name - Sprinters

### 👥 Team
- [Ananya Praveen Shetty](https://github.com/ananya101001)
- [Apoorva Shastry](https://github.com/ApoorvaShastry10)
- [Junie Mariam Varghese](https://github.com/juniemariam)
- [Rinku Tekchandani](https://github.com/rinkutek)

### Contributions
Apoorva & Ananya collaborated on the Customer module, working across both the frontend and backend to build user-facing features like browsing restaurants, making reservations, integrating google maps API, SMTP integrating,and submitting reviews.

Junie was responsible for the Restaurant Manager module, implementing both frontend and backend logic for managing restaurant profiles, updating availability, and viewing reservations.

Rinku handled the Admin module end-to-end, developing backend analytics, approval workflows, and the admin dashboard UI with rich visual insights and data visualization.

### XP Values
1.	Communication
The team maintained open and consistent communication by holding daily stand-up meetings, using collaborative tools and engaging in pair programming sessions. This helped ensure that everyone was aligned on progress, blockers, and changes in requirements. Regular code reviews and design discussions promoted shared understanding and reduced miscommunication.

2.	Respect
The team created a culture of mutual respect, valuing each member's contributions regardless of role or experience level. Constructive feedback was given in a supportive manner, and decisions were made collaboratively. Respect for each other’s time and work led to better morale and productivity.


# 🍽️ BookTable — Restaurant Reservation Platform

BookTable is a full-stack web application for discovering, reserving, reviewing, and managing restaurants. It supports user reservations and admin approvals, with a clean dashboard to monitor analytics.

---

## 🌟 Features

### 👥 Users
- Sign up / Log in
- Browse and search restaurants
- Make, view, modify, and cancel reservations
- Submit and read reviews

### Restaurant Managers
- Managing restaurant profiles
- Updating restaurant availability
- Viewing reservations 
  

### 🛠️ Admins
- Admin login interface
- `/admin/dashboard` with analytics:
   - Reservation trends (30-day history)
   - Top-performing restaurants
   - Top booked restaurants
  - Daily breakdown
- `/admin/restaurants` management:
  - View details of each restaurant in a modal
  - Approve / delete new submissions
---

## 🏗️ Architecture

### Frontend
- React (with Redux & React Router)
- CSS modules for styling

### Backend
- Flask (Python)
- SQLAlchemy ORM
- Flask-Login
- PostgreSQL as the database

---

## 📦 Folder Structure
backend/ # Flask app
└── models/
└── api/
└── seeds/
└── init.py
---
front-end/ # React app
└── src/
└── components/
└── store/
└── App.js
---

## 🗂️ Design Decisions

- **MVC Pattern**: Flask acts as controller, SQLAlchemy as model, React as view
- **Factory Pattern**: `create_app()` is used for environment flexibility
- **Decorator Pattern**: Used extensively via Flask route decorators
- **Observer & State Patterns**: Used via Redux and React hooks
- **Command Pattern**: Used for CLI seeding (`flask seed all`)
---

## 📐 Diagrams

### 🧱 Deployment Diagram
- **Deployment Diagram**: [View Here](./architecture/DeploymentDiagram.png)

### 🧩 Component Diagram
- **Component Diagram**: [View Here](./architecture/ComponentDiagram.png)


### 🔧 Backend
```bash
cd backend
pip install -r requirements.txt
flask db upgrade
flask seed all
flask run
```
### 💻 Frontend

``` bash
cd front-end
npm install
npm start
```
### Cloud Deployment -GCP
[View Here](output/Outputs.pdf)
