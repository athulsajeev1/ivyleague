# IvyLeague Connect | AI Intel 2.0 🎓✨

IvyLeague Connect is a powerful, AI-driven networking and opportunity matching platform designed for elite students and researchers. It automates the discovery of Ivy League fellowships, research roles, and internships while providing a high-stakes social environment for achievement sharing.

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.9+
- [Optional] VS Code with Python extension

### 2. Setup
```powershell
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize & Seed Database
python seed_db.py
```

### 3. Run the Application
```powershell
uvicorn app.main:app --reload
```
Open **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser.

---

## 🛠️ Performance Modules

### 🔍 Ivy Intelligence (AI Matching)
Uses a **TF-IDF (Term Frequency-Inverse Document Frequency)** Machine Learning model combined with **Cosine Similarity** to match your profile/resume against real-world opportunities. It doesn't just look for words; it understands the semantic domain (e.g., distinguishing between "Legal Research" and "AI Research").

### 📄 PDF Resume Parsing
Upload your CV in PDF format. The system uses `PyPDF2` to read the document and extract:
- Technical and soft skills
- Research interests
- Email addresses for auto-filling applications

### 📡 Real-World Scrapers
The system includes robust scrapers for **Yale** and **Harvard** event portals. When you click **Sync Intel**, the backend performs real-time HTTP requests to these universities to fetch the latest academic openings.

### 🤝 Social Achievement Feed
A live-updating feed where "Ivy Scholars" share their achievements. Features include:
- Persistence (Database-backed)
- Verified achievement badges
- Real-time UI notifications

---

## ❓ FAQ

### Q: How does the CV upload help me?
When you upload your CV, the AI extracts your **Skills**. These skills are then cross-referenced with the descriptions of every fellowship and internship in the database. Your **Match Score** increases if your CV skills align with the requirements of the opportunity.

### Q: Why is my Match Score 0%?
Try clicking **Sync Intel** or ensure your Profile corresponds to the domains (AI, Law, Biomedical, etc.) covered by the opportunities.

### Q: Where is the data stored?
All data (Users, Posts, Opportunities) is stored in a local `sql_app.db` (SQLite) file for easy portability.
