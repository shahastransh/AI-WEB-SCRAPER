```markdown
# 🤖 AI Web Scraper & Intelligence Engine

A modular, cloud-ready web scraping application that extracts dynamic web content and intelligently parses it using Large Language Models. Built with **Streamlit**, **Selenium**, and **LangChain (Groq / Ollama)**, this tool converts raw, unstructured HTML into targeted, structured insights based on natural language instructions.

---

## 🚀 Features

* **Dynamic JavaScript Scraping:** Utilizes headless Selenium WebDriver to reliably render dynamic, JavaScript-heavy single-page applications.
* **Intelligent DOM Sanitization:** Strips boilerplate script, style, and formatting tags using BeautifulSoup4 to isolate core content and minimize token overhead.
* **Context-Aware LLM Extraction:** Leverages LangChain and high-throughput LLMs (via Groq API / local Ollama) to extract strictly what you specify with zero conversational filler.
* **Smart Content Chunking:** Implements customizable character-based windowing to process extensive web pages without exceeding model context window boundaries.
* **Cross-Platform & Cloud Ready:** Pre-configured with dual driver detection for local machines (Windows/macOS) and Debian-based Linux containers (Streamlit Community Cloud).
* **Interactive UI:** Built with Streamlit for seamless URL input, real-time scraping, DOM inspection, and structured output rendering.

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Automation & Scraping:** Selenium WebDriver, BeautifulSoup4
* **LLM Orchestration:** LangChain, LangChain-Groq
* **Inference Engine:** Groq API (`llama-3.3-70b-versatile` / `llama-3.1-8b-instant`) & Local Ollama support
* **Language & Runtime:** Python 3.10+

---

## 📁 Project Structure

```text
├── main.py              # Streamlit frontend and UI execution flow
├── scrape.py            # Headless browser configuration, scraping, and DOM cleaning
├── parse.py             # LangChain prompt templates, Groq client, and chunk parsing
├── requirements.txt     # Python package dependencies
├── packages.txt         # Linux OS dependencies for cloud deployment (Chromium)
├── .gitignore           # Ignores sensitive keys (.env), drivers, and cache
└── README.md            # Project documentation

```

---

## ⚙️ Local Installation & Setup

**1. Clone the repository**

```bash
git clone [https://github.com/your-username/AI-web-Scraper.git](https://github.com/your-username/AI-web-Scraper.git)
cd AI-web-Scraper

```

**2. Create and activate a virtual environment**

```bash
# Windows
python -m venv ai
.\ai\Scripts\activate

# macOS / Linux
python3 -m venv ai
source ai/bin/activate

```

**3. Install dependencies**

```bash
pip install -r requirements.txt

```

**4. Configure environment variables**
Create a `.env` file in the project root:

```ini
GROQ_API_KEY=your_groq_api_key_here

```

**5. Run the Streamlit application**

```bash
streamlit run main.py

```

---

## 🌐 Cloud Deployment (Streamlit Community Cloud)

1. Push this repository to GitHub.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) and create a new application pointing to `main.py`.
3. In **App Settings > Secrets**, provide your API credentials:
```toml
GROQ_API_KEY = "gsk_your_actual_groq_api_key_here"

```


4. Deploy the app. The included `packages.txt` will automatically install the headless Chromium binaries required for scraping in the cloud container.

---

## 💡 How It Works

```
[Target URL] 
     │
     ▼
[Selenium Headless Browser]  ──►  Renders dynamic JS & extracts raw HTML
     │
     ▼
[BeautifulSoup Pipeline]    ──►  Strips <script>/<style> tags & cleans DOM
     │
     ▼
[Text Chunking Engine]       ──►  Splits text into token-friendly segments
     │
     ▼
[LangChain + Groq LLM]       ──►  Extracts user-requested data based on custom prompts
     │
     ▼
[Streamlit Interface]        ──►  Presents clean, structured results

```

```

```