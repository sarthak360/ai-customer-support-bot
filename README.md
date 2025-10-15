# 🤖 AI Customer Support Bot

![Chatbot Demo GIF](demo.gif)

*A fully local, AI-powered chatbot designed to handle customer support queries with contextual memory and smart escalation capabilities. This project runs 100% on your local machine, ensuring data privacy and no API costs.*

---

## ✨ Features

* 🧠 **Conversational Memory:** Remembers the last few messages in a conversation for natural, context-aware follow-up questions.
* 📚 **Knowledge Base Integration (RAG):** Answers user questions by retrieving relevant information from a local `faqs.json` file, ensuring grounded and accurate responses.
* 🚀 **Smart Escalation:**
    * Automatically detects when a user's query cannot be answered from the knowledge base and suggests speaking to a human agent.
    * Handles direct user requests to speak with a human.
* ✍️ **Conversation Summarization:** Upon escalation, it generates a concise summary of the conversation to seamlessly hand over to a human agent.
* 💻 **Fully Local & Private:** Powered by Ollama and a local language model (Llama 3), meaning no data ever leaves your machine.
* 🌐 **Web Interface:** A clean and simple chat interface built with HTML, CSS, and JavaScript.
* 🗄️ **Session Tracking:** Uses an SQLite database to manage and log individual chat sessions.

---

## 🛠️ Tech Stack

| Component            | Technology                                                                                                   |
| -------------------- | ------------------------------------------------------------------------------------------------------------ |
| **Backend** | ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) |
| **LLM Engine** | ![Ollama](https://img.shields.io/badge/Ollama-222222?style=for-the-badge&logo=ollama&logoColor=white) (using Llama 3 8B) |
| **Database** | ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)      |
| **Frontend** | ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) |

---

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

* **Python 3.8+** installed on your system.
* **Ollama:** You must have Ollama installed and running. Download it from [ollama.com](https://ollama.com).

### Installation & Setup

1.  **Clone the Repository**
    ```sh
    git clone [https://github.com/sarthak360/ai-customer-support-bot.git](https://github.com/sarthak360/ai-customer-support-bot.git)
    cd ai-customer-support-bot
    ```

2.  **Download the LLM Model via Ollama**
    *Make sure Ollama is running.* Open a terminal and pull the Llama 3 8B model.
    ```sh
    ollama pull llama3:8b
    ```

3.  **Create and Activate a Python Virtual Environment**
    ```sh
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

4.  **Install Dependencies**
    Install all the required Python packages from the `requirements.txt` file.
    ```sh
    pip install -r requirements.txt
    ```

---

## ⚡ Running the Application

With the setup complete, you can now run the chatbot.

1.  **Ensure Ollama is running** in the background.
2.  **Start the Flask Backend Server:**
    ```sh
    flask --app app.api run
    ```
3.  **Open the Chat Interface:**
    Open your favorite web browser and navigate to:
    **http://127.0.0.1:5000**

You can now start chatting with your AI support bot!

---

