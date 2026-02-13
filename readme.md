This is my first project 
I have learned about streamlit and integrating LLM and how to work with different types of scraping tools in Python.
I have used;
Selenium for using webdriver,
Beautiful soup for extracting, cleaning the body content and spliting DOM content.
I have used ollama - phi4-mini model 




🤖 AI Web Scraper & Intelligence Engine
A powerful, modular web scraping tool that leverages LLMs (Ollama/Phi-4-mini) to extract and parse specific data from any website. By combining Selenium for browser automation and LangChain for intelligent orchestration, this tool turns messy HTML into clean, structured information.

🚀 Features
Automated Web Navigation: Uses Selenium to launch a headless browser, ensuring JavaScript-heavy sites are fully loaded before extraction.

Intelligent DOM Cleaning: Automatically strips scripts and styles using BeautifulSoup4, reducing noise and optimizing token usage for the LLM.

Context-Aware Parsing: Utilizes LangChain and Phi-4-mini (via Ollama) to extract only the information you describe, ignoring irrelevant data.

Chunking Algorithm: Implements a custom DOM splitting logic to handle large pages without exceeding LLM context limits.

Interactive UI: A clean, user-friendly interface built with Streamlit for real-time scraping and parsing.

🛠️ Tech Stack
Frontend: Streamlit

Orchestration: LangChain

LLM: Ollama (Phi-4-mini)

Automation: Selenium WebDriver

Parsing: BeautifulSoup4

Language: Python 3.x