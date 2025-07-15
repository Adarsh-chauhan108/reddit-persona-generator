# 🧠 Reddit Persona Generator

A Python-based tool that scrapes a Reddit user's public activity (posts + comments), analyzes it using OpenAI's GPT models, and generates a detailed, evidence-based user persona — complete with citations.

---

## 📌 Features

- 🔍 Scrapes posts and comments from any public Reddit user
- 🤖 Generates structured persona insights using GPT-4 (via OpenAI API)
- 📂 Outputs persona to a Markdown `.txt` file
- 📎 Cites sources from Reddit (with permalinks and scores)
- 🧠 Covers traits like:
  - Location
  - Profession
  - Hobbies
  - Personality & Communication style
  - Tech savviness
  - Values & Beliefs
  - Reddit usage patterns

---

## 🛠️ Setup Instructions

### 1. **Clone the Repository**

```bash
git clone https://github.com/your-username/reddit-persona-generator.git
cd reddit-persona-generator
```

### 2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 3. **Add Your API Keys**

Create a `.env` file using the provided `.env.example`:

```
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_secret_here
REDDIT_USER_AGENT=reddit-persona-script
OPENAI_API_KEY=your_openai_key_here
OPENAI_MODEL=gpt-4  # or gpt-3.5-turbo if preferred
```

> 💡 To get Reddit API credentials, visit: https://www.reddit.com/prefs/apps  
> Choose "script" type and set redirect URI to `http://localhost:8080`

---

## 🚀 How to Run

```bash
python main.py kojied --limit 50 --verbose
```

### Optional flags:
| Flag | Description |
|------|-------------|
| `--limit` | Max number of posts/comments (default: 100) |
| `--output-dir` | Directory to save the output file (default: `output/`) |
| `--verbose` or `-v` | Enable detailed logging |

---

## 📄 Output

Each analysis is saved as a `.txt` file like:

```
output/
├── kojied_persona.txt
├── Rainbolt_persona.txt
```

Each persona includes:
- Structured insights (Location, Hobbies, etc.)
- Direct citations with permalinks
- Confidence ratings (High / Medium / Low)

---

## 📦 Folder Structure

```
reddit-persona-generator/
├── main.py
├── reddit_scraper.py
├── persona_generator.py
├── utils.py
├── requirements.txt
├── .env.example
├── README.md
└── output/
```

---

## ⚠️ Disclaimer

This tool is for **educational and research** purposes only. The generated personas are based on **public Reddit data** and **LLM inference**, and may not reflect the full personality or beliefs of the user.

---

## 👨‍💻 Author

Adarsh Singh Chauhan — Built with ❤️ 
Feel free to explore or fork for learning!