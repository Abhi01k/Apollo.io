# 🤖 Notion AI Assistant Bot

This project integrates **Notion** and **OpenAI** using Python to create a smart task management assistant. It reads tasks from a Notion database, summarizes them using GPT, and outputs insights directly from your workspace.

---

## 🚀 Features

- ✅ Connects to your Notion workspace via Notion API
- ✅ Uses OpenAI's GPT (ChatGPT) to summarize task lists
- ✅ Python-based automation — no manual effort
- ✅ Ideal for personal productivity or team projects
- ✅ Environment variables stored securely using `.env`

---

## 🛠️ Technologies Used

- [Python 3.8+](https://www.python.org/)
- [Notion API](https://developers.notion.com/)
- [OpenAI API](https://platform.openai.com/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## 📂 Project Structure


---

## 🧠 How It Works

1. Connects to your Notion database via API
2. Pulls all tasks with properties like `Name`, `Status`, etc.
3. Sends task content to OpenAI's GPT model for summarization
4. Prints an AI-generated summary with insights

---

## 🔐 Environment Setup

Create a `.env` file in the root folder and add:


> ⚠️ Never commit your `.env` file or API keys to GitHub!

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/your-username/notion-ai-assistant.git

# Navigate to project folder
cd "D:\CTSE Internship"

# Create a virtual environment (optional)
python -m venv venv
venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt
