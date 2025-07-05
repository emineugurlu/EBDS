# 🔬 EBDS Basic Science Assistant

This project is an AI-powered science assistant developed to provide quick and accurate answers to users in the field of basic sciences. In addition to its internal knowledge base, it has the ability to fetch and summarize up-to-date information from the internet. It features an interactive and user-friendly web interface built with the Streamlit framework.

## 🚀 Project Vision

This assistant is developed with the vision of being "a big project for humanity". Our goal is to facilitate access to fundamental scientific knowledge and enhance scientific literacy.

## ✨ Features

* **Intelligent Answering:** Utilizes NLP (Natural Language Processing) techniques to understand user queries and provide relevant answers.
* **Knowledge Base Integration:** Offers fast and accurate responses to topics within its predefined knowledge base.
* **Web Scraping:** For questions not found in its knowledge base, it finds relevant web pages via DuckDuckGo and extracts their content.
* **Intelligent Summarization:** Summarizes lengthy texts fetched from the web using the `sumy` library's LexRank algorithm, presenting them in an understandable format.
* **Interactive Chat Interface:** Provides a modern and intuitive chat-based user interface with Streamlit. It maintains a chat history, and messages are displayed in bubbles.
* **User Feedback Mechanism:** Includes simple like/dislike buttons to evaluate the helpfulness of the assistant's responses.
* **Comprehensive Error Handling:** Notifies the user clearly about errors that may occur during web scraping or other operations.

## 🛠️ Technologies

* **Python:** The primary development language for the project.
* **Streamlit:** Web framework used for developing the user interface (GUI).
* **Sentence Transformers:** NLP library used for converting texts into embeddings.
* **scikit-learn:** For similarity calculations (`cosine_similarity`).
* **BeautifulSoup4 & Requests:** For web scraping operations.
* **Sumy:** For summarizing texts fetched from the web (using the `LexRank` algorithm).
* **NLTK:** For text processing and sentence tokenization (specifically the `punkt` tokenizer).

## 🚀 Setup and Running

Follow these steps to set up and run the project on your local machine:

### 1. Clone the Repository

```bash
git clone [https://github.com/YourGitHubUsername/EBDS.git](https://github.com/YourGitHubUsername/EBDS.git) # Replace with your GitHub username
cd EBDS
2. Create and Activate Virtual Environment
It is highly recommended to create a virtual environment to isolate project dependencies.

Bash

python -m venv venv
On Windows:

Bash

.\venv\Scripts\activate
On macOS/Linux:

Bash

source venv/bin/activate
3. Install Dependencies
Install all required Python libraries:

Bash

pip install -r requirements.txt
4. Download NLTK Resources
For Sumy and other NLP operations to function correctly, you may need to download NLTK's punkt tokenizer. Run this command once:

Bash

python -c "import nltk; nltk.download('punkt')"
5. Start the Application
Start the Streamlit application with the following command:

Bash

streamlit run app.py
or (If the streamlit command is not directly recognized):

Bash

.\venv\Scripts\streamlit run app.py
The application will automatically open in your web browser (usually at http://localhost:8501).

