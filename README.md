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

To set up and run the project on your local machine, follow these steps:

1.  **Clone the Repository:** If you haven't already, clone the project repository to your local machine.
    ```bash
    git clone [https://github.com/YourGitHubUsername/EBDS.git](https://github.com/YourGitHubUsername/EBDS.git) # Replace with your GitHub username
    cd EBDS
    ```
2.  **Create and Activate Virtual Environment:** It is highly recommended to create a virtual environment to isolate project dependencies. Then, activate it.
    ```bash
    python -m venv venv
    # On Windows (PowerShell):
    .\venv\Scripts\activate
    # On macOS/Linux (Bash/Zsh):
    # source venv/bin/activate
    ```
3.  **Install Dependencies:** Install all required Python libraries listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```
4.  **Download NLTK Resources:** For Sumy and other NLP operations to function correctly, you may need to download NLTK's `punkt` tokenizer. Run this command **once**.
    ```bash
    python -c "import nltk; nltk.download('punkt')"
    ```
5.  **Start the Application:** Launch the Streamlit application. It should automatically open in your web browser (typically at `http://localhost:8501`).
    ```bash
    streamlit run app.py
    # Alternatively (If 'streamlit' command is not directly recognized, especially on Windows/PowerShell):
    # .\venv\Scripts\streamlit run app.py
    ```

## ⚙️ Git Commands (For Version Control)

These commands are essential for managing your project's version control and pushing changes to your GitHub repository.

1.  **Add Changes to Staging Area:** Prepare all your modified (new, changed, deleted) files for the next commit.
    ```bash
    git add .
    ```
2.  **Commit Changes:** Save the staged changes to your local repository. Use the `-m` flag to add a concise commit message describing your changes.
    ```bash
    git commit -m "Your descriptive commit message here"
    ```
3.  **Push Changes to GitHub:** Send your local commits to your remote GitHub repository. The `master:main` part sends changes from your local `master` branch to the `main` branch on GitHub (which is the modern default).
    ```bash
    git push origin master:main
    # If your remote repository's main branch is still named 'master', you might need to use:
    # git push origin master
    ```
4.  **Check/Update Git Configuration (Email):** Verify which email address Git is using for your commits. This email must match a verified email address associated with your GitHub account for contributions to appear on your profile. If it's incorrect, update it.
    ```bash
    git config --global user.email
    # To update:
    # git config --global user.email "emineugurlu957@gmail.com"
    ```

## 📝 Usage

Once the application opens, type a question related to basic sciences into the "Type your question here..." box and press Enter. The assistant will provide information from its knowledge base or by fetching it from the web.

## 🤝 Contributing

If you wish to contribute to the project, please feel free to create a Pull Request or report an Issue.

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
