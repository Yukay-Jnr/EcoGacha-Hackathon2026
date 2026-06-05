<div align="center">

# 🌱 EcoGacha

### AI-Powered Waste Classification & Campus Reward System

_Scan your waste. Earn EcoTokens._

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML](https://img.shields.io/badge/HTML%20%2F%20CSS%20%2F%20JS-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)

**Built for the Topfaith 72-Hour Eco Hackathon · Topfaith University, Mkpatak**

[Features](#-features) · [How it works](#-how-it-works) · [Tech stack](#-tech-stack) · [Getting started](#-getting-started) · [API](#-api-endpoints) · [Team](#-team)

---

</div>

## 🌍 About

**EcoGacha** is a gamified waste classification system that uses AI to identify waste items and reward students for proper disposal habits.

Students upload a photo of their waste item, the AI classifies it, and they earn EcoTokens through a weighted gacha-style reward — rarer and more hazardous waste earns bigger rewards. Tokens accumulate in a personal wallet and can be redeemed on campus.

> ♻️ This is the v1 smart-bin demo, built to run on a local machine for the hackathon. The web dashboard, leaderboard, and token system are fully functional. Future phases will add the physical hardware for the bin, a marketplace, EcoDex education module, upcycling group directory, and campus issue reporting.

**Hackathon theme:** *"Climate Change, Marine Pollution and the Quest for Sustainable Blue Economy in Nigeria."*

---

## ✨ Features

- 🤖 **AI waste classification** — PyTorch + Keras (ResNet18) identifies waste from uploaded photos
- 🎰 **Gacha reward system** — weighted random token amounts; rarer waste earns more
- 🌿 **Eco tip on every scan** — one quick fact shown after each classification
- 👤 **Student accounts** — matric number + email, personal token wallet
- 📊 **Dashboard** — token balance, scan history, and quick redeem
- 🏆 **Leaderboard** — top campus eco contributors ranked by tokens
- 💰 **Token redemption** — cash out via the web app or at the campus token stall


---

## ⚙️ How it works

```
Student registers / logs in with matric number
        │
        ▼
Uploads a photo of their waste item
        │
        ▼
PyTorch model classifies the waste
(cardboard · glass · metal · organic · paper · plastic · e-waste)
        │
        ▼
Backend assigns a base token value by category
        │
        ▼
Weighted gacha roll → Common | Rare | Epic
        │
        ▼
Final EcoTokens credited to student wallet
+ Eco tip displayed
        │
        ▼
Dashboard and leaderboard updated
        │
        ▼
Student redeems tokens via web or campus stall
```

---

## 🎰 Reward system

Waste with higher environmental danger, higher recycling difficulty, or stronger marine pollution risk gets a higher base token value. The gacha roll then adds randomness on top.

| Waste Type | Token Range | Gacha Tier Weights |
|---|---|---|
| 🥫 Metal | 4–6 base | same weights |
| 🍶 Glass | 3–5 base | same weights |
| 🧴 Plastic | 2–4 base | same weights |
| 📄 Paper / Cardboard | 1–3 base | same weights |


**Epic rolls multiply base tokens by 3–5×. Rare rolls multiply by 1.5–2.5×.**

---

## 🛠️ Tech stack

| Layer | Technology | Why |
|---|---|---|
| **AI model** | Pytorch + ResNet18 | Pretrained base, easy to fine-tune on waste images |
| **Backend** | Python + Flask | Simple REST API, beginner-friendly |
| **Database** | SQLite | Zero setup, single file, fully offline |
| **Frontend** | HTML + JavaScript | No framework needed |
| **Styling** | CSS | Clean dark UI with minimal effort |
| **Backend hosting** | Render (free tier) | Deploy from GitHub in minutes |
| **Frontend hosting** | Vercel | Instant static deploy, free |


---

## 📁 Project structure

```
ecogacha/
│
├── 📂 backend/
│   ├── app.py                  # Flask entry point, registers blueprints
│   ├── database.py             # SQLite setup — creates DB and tables on first run
│   ├── requirements.txt        # Python dependencies
│   │
│   ├── routes/
│   │   ├── auth.py             # /api/auth/register · /api/auth/login
│   │   ├── scan.py             # /api/scan/classify
│   │   ├── rewards.py          # /api/rewards/redeem
│   │   └── users.py            # /api/users/balance · history · leaderboard
│   │
│   └── services/
│       ├── ai_service.py       # Loads TF model, runs image prediction (demo mode if no model)
│       └── token_service.py    # Gacha logic, token calculation, eco tips
│
├── 📂 ai_model/
│   ├── rise_ai_model.pth                # Trained Keras model (add after training — see notes)
│   ├── labels.txt              # One category per line
│   └── training_notes.md       # How to train and export the model
│
├── 📂 frontend/
│   ├── index.html              # Login + register
│   ├── dashboard.html          # Token balance, history, redeem
│   ├── scan.html               # Scan/Upload image → classify → see result
│   ├── leaderboard.html        # Campus rankings
│   │
│   ├── css/
│   │   └── style.css           # Full dark-theme and light-theme stylesheet
│   │
│   └── js/
│       └── app.js              # Shared API helper, auth, utilities
│
├── vercel.json                 # Vercel deploy config for frontend
├── .gitignore
└── README.md
```

---

## 🚀 Getting started

### Prerequisites

- Python 3.10+
- `pip`
- Git
- Any modern browser

---

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ecogacha.git
cd ecogacha
```

---

### 2. Install backend dependencies

```bash
cd backend
pip install -r requirements.txt
```

---

### 3. Start the backend

```bash
python app.py
```

The database file (`ecogacha.db`) is created automatically on first run.

API runs at:
```
http://localhost:5000
```

---

### 4. Open the frontend

Open `frontend/index.html` in your browser. Keep the backend running in the background.

> For local testing, `API_BASE` in `frontend/js/app.js` is already set to `http://localhost:5000`.

---


## 🗺️ Roadmap

- [x] AI waste classification (PyTorch + ResNet18)
- [x] Flask REST API with student accounts
- [x] Gacha reward system with weighted tiers
- [x] Token wallet, dashboard, and leaderboard
- [x] Token redemption
- [x] Eco tip on every scan
- [ ] EcoDex — full waste education module
- [ ] Marketplace — trade and swap upcyclable materials
- [ ] Upcycling group directory (Uyo-based)
- [ ] Campus issue reporting (drainage, waste, odour alerts)
- [ ] Mobile-friendly QR scan integration

---

## 👥 Team — G-Unit

| Name | Role |
|---|---|
| Uduak Umobit-Jnr | Frontend, and UI design |
| Godswill James | AI model, testing & backend |
| Uniokid Uwak |Frontend, UI design & documentation |

---

<div align="center">

Built with sustainability in mind 🌱 · Topfaith University, Mkpatak · G-Unit

</div>
