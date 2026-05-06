# 🔬 EBDS: Intelligent Basic Science Assistant & Urban Researcher

> **"A high-performance, AI-driven ecosystem designed to democratize access to fundamental scientific knowledge. Built with Python and Streamlit, EBDS integrates real-time web intelligence with advanced NLP architectures to enhance global scientific literacy."**

![Language](https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Framework](https://img.shields.io/badge/Framework-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![NLP](https://img.shields.io/badge/NLP-Sentence--Transformers-yellow?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

**EBDS Basic Science Assistant** is more than a chat interface; it is a scalable framework for scientific discovery. Developed by **Emine Uğurlu**, this project aims to provide quick, accurate, and summarized scientific data by bridging the gap between static knowledge bases and dynamic web intelligence.

---

## 🚀 Engineering Excellence

This project showcases professional-grade Python development and AI integration standards:

* **Hybrid Intelligence Engine:** Seamlessly switches between an internal vector-based knowledge base and real-time web scraping via **DuckDuckGo** when local data is insufficient.
* **Semantic Search & Embeddings:** Utilizing **Sentence Transformers** and `cosine_similarity` to ensure high-precision matching between user queries and scientific data.
* **Autonomous Summarization:** Implementation of the **LexRank algorithm** via the `sumy` library to distill lengthy research papers and web content into digestible insights.
* **Robust Web Orchestration:** High-performance scraping architecture using **BeautifulSoup4** and **Requests** with comprehensive error handling for network stability.
* **User-Centric Feedback Loop:** Integrated real-time feedback mechanism (like/dislike) to evaluate AI response accuracy and optimize future inference.

## ✨ Core Features

* 🧠 **Intelligent Answering:** Advanced NLP pipeline for deep understanding of complex scientific queries.
* 🌐 **Real-time Web Integration:** Dynamic content extraction from the web to stay updated with the latest scientific breakthroughs.
* 💬 **Interactive UX:** A modern, bubble-based chat interface maintaining session history for seamless scientific dialogue.
* 📊 **Scalable Knowledge Base:** Modular structure allowing for easy expansion of predefined scientific datasets.

## 🛠️ Technologies & Stack

* **Core Logic:** Python 3.10+
* **UI/UX:** Streamlit (Reactive Web Framework)
* **AI/ML:** Sentence Transformers, scikit-learn (Embeddings & Similarity)
* **Text Processing:** NLTK, Sumy (Lexical Analysis & Tokenization)
* **Networking:** Requests, BeautifulSoup4 (Scraping & Extraction)

---
## ⚙️ Installation & Setup

### 1. Prerequisites
* Python 3.10 or higher.
* Virtual Environment (Recommended).

### 2. Getting Started
```bash
git clone [https://github.com/emineugurlu/EBDS.git](https://github.com/emineugurlu/EBDS.git)
cd EBDS
python -m venv venv
source venv/bin/activate  # Or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
````

### 3. Initialize NLP Resources 
````bash 
python -c "import nltk; nltk.download('punkt')"
````

### 4.Launch the Engine
````bash
streamlit run app.py
````

Developed by Emine Uğurlu - Computer Engineer
