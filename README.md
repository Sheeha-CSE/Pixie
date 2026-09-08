# 🧚 Pixie — MarketMind AI Marketing Platform

An intelligent, AI-powered marketing and campaign collaboration platform designed for modern businesses, growth teams, and part-time student marketers. Powered by **Groq Ultra-Fast LLMs** and **Flask**.

---

## 🌟 Key Features

* **🧚 Pixie Mascot AI Widget:** Interactive pink mascot assistant providing real-time marketing suggestions, copy generation, and strategy tips.
* **📊 Growth & Analytics Dashboard:** Visual marketing performance metrics, conversion tracking, and ROI analysis.
* **🎯 Campaign Management:** Launch, manage, and assign multi-channel campaigns (Instagram, WhatsApp, TikTok, Google Ads).
* **🎓 Student Marketer Portal:** Connect business owners with creative student marketers for viral campus outreach and content creation.
* **💡 AI Strategy & Content Generation:** Instant campaign strategies, copy variations, and audience segmentation.

---

## 🚀 Quick Start (Local)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and enter your Groq API key:
```bash
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your_secret_key_here
```

### 3. Run the App
Double-click `run.bat` or run:
```bash
python app.py
```
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser.

---

## 🔑 Demo Login Accounts

| Role | Email | Password |
| :--- | :--- | :--- |
| **Business Owner** | `owner@marketmind.ai` | `owner123` |
| **Student Marketer** | `alex@marketmind.ai` | `employee123` |

---

## ☁️ Deployment on Vercel

This repository is pre-configured for seamless deployment on **Vercel**:
* Configured with serverless routing via `vercel.json` and `api/index.py`
* Serverless-friendly dynamic SQLite storage in `/tmp`
* Automatic demo database seeding on cold starts

### Required Environment Variables in Vercel:
* `GROQ_API_KEY`: Your Groq API key (from [console.groq.com](https://console.groq.com))
* `SECRET_KEY`: A secure random secret key (e.g. `marketmind_secret_super_secure_key_2026`)