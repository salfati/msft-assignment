#Community Insights Chatbot

This is an AI-powered conversational chatbot built using **Python**, **Flask**, and **OpenAI GPT-4** that:
- Ingests developer questions from Stack Overflow
- Extracts actionable insights using AI
- Enables chat-based exploration of pain points and solutions

---

## Features

- Fetches recent questions tagged with `microsoft-teams` from Stack Overflow
- Uses OpenAI GPT-4 to extract and summarize developer pain points
- Allows users to interact with extracted insights in a chatbot-style interface
- Supports follow-up questions for deeper exploration

---

## Setup Instructions

### 1. Clone the repository or extract the files

```bash
git clone <repo-url>
cd community_insights_tool
```

### 2. Install dependencies

Make sure you have Python 3.8+ installed. Then run:

```bash
pip install flask openai requests
```

### 3. Set your OpenAI API key

Export your API key as an environment variable:

```bash
export OPENAI_API_KEY='your-openai-key'
```

Or set it inline in `extract_feedback.py` and `bot.py` if needed (not recommended).

---

## Run the Application

```bash
python bot.py
```

Navigate to: [http://localhost:5000](http://localhost:5000)

---

## Project Structure

```bash
community_insights_tool/
├── bot.py                  # Flask chatbot app
├── fetch_data.py           # Pulls Stack Overflow questions
├── extract_feedback.py     # Uses OpenAI API to extract insights
├── templates/              # Contains Adaptive Card template (if extended)
├── static/                 # (Optional for future UI assets)
└── README.md               # This file
```

---

## Demo Suggestions

Create a 5–7 minute video showing:
1. Starting the app
2. Exploring Stack Overflow insights
3. Chatting with the AI for follow-up recommendations

---

## Notes

- This is a local prototype and not integrated with Microsoft Teams or deployed externally.
- Extend it with real-time Teams integration or database persistence for production use.

---

## Created With

- Flask
- OpenAI GPT-4
- Stack Overflow API
