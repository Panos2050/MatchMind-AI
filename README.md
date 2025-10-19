# 🤖 MatchMind-AI

An intelligent football match summarizer that fetches live match data, analyzes it, and generates natural-language summaries using **HuggingFace Transformers**.

This project includes a full **CI/CD pipeline** with:
- 🧪 Automated testing using **pytest**
- ⚙️ Continuous Integration using **Jenkins**
- 🐳 Containerization via **Docker & Docker Compose**
- 📊 Monitoring & analytics with **Prometheus** and **Grafana**
- ☁️ Webhook automation via **GitHub → Jenkins (Ngrok tunnel)**

---

## 🚀 Features
- Summarizes football match data using NLP
- MongoDB integration for match storage
- Automated builds and testing via Jenkins
- Real-time pipeline monitoring (Prometheus + Grafana)
- Easy-to-deploy with Docker Compose

---

## 🧰 Prerequisites
Before you start, make sure you have:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Git](https://git-scm.com/)
- [Ngrok](https://ngrok.com/) (optional, for exposing Jenkins externally)

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/Panos2050/MatchMind-AI.git
cd MatchMind-AI
