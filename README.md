# 🏟️ Sunbelt Snack Station POS

A full-featured Point of Sale system built for concession stands at sporting events. Originally developed as a Python/tkinter desktop application, rebuilt as a Flask web app for browser-based access.

## Features

- **Role-based login** — Employee and Admin accounts
- **Event-driven sessions** — Select sport, gender, level, and away team; unique Game IDs auto-generated
- **Live POS terminal** — Add/remove items by category (Food / Snacks / Drinks), real-time cart updates
- **Inventory tracking** — Stock decrements on every transaction, including multi-ingredient items
- **Admin panel**
  - Menu management (add, remove, transfer items; update prices)
  - Inventory management (view and update stock levels)
  - Analytics dashboard (top sellers, earnings by sport/team, full sales reports)

## Tech Stack

- **Backend**: Python / Flask
- **Database**: SQLite
- **Frontend**: Vanilla HTML/CSS/JS (no framework)
- **Deployment**: Render.com (free tier)

## Local Setup

```bash
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000`

**Default admin setup**: Register an admin account from the main menu to get started.

## Deploy to Render (Free)

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect your GitHub repo
4. Render auto-detects the `render.yaml` config
5. Deploy — your live URL will be `https://sunbelt-snack-station.onrender.com` (or similar)

> **Note**: Render's free tier spins down after inactivity. First load may take ~30 seconds.

## Project Structure

```
sunbelt/
├── app.py               # Flask application + all routes
├── concession_stand.db  # SQLite database (auto-created on first run)
├── requirements.txt
├── Procfile
├── render.yaml
└── templates/
    ├── base.html        # Shared layout + dark POS styling
    ├── index.html       # Main menu / splash screen
    ├── login.html
    ├── register.html
    ├── event.html       # Event/sport selection
    ├── pos.html         # POS terminal (cashier view)
    ├── receipt.html     # Transaction confirmation
    ├── admin.html       # Admin hub
    ├── admin_inventory.html
    ├── admin_menu.html
    └── analytics.html
```

## Original Desktop Version

The original tkinter desktop application is preserved as `Programa_484.py` for reference.

---

*Capstone project — Business Information Systems*
