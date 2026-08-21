import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=NetworkService")
    options.add_argument("--window-size=1920x1080")

    # Use Linux system Chromium on Streamlit Cloud if present
    if os.path.exists("/usr/bin/chromium") or os.path.exists(
        "/usr/bin/chromium-browser"
    ):
        options.binary_location = (
            "/usr/bin/chromium"
            if os.path.exists("/usr/bin/chromium")
            else "/usr/bin/chromium-browser"
        )
        service = (
            Service("/usr/bin/chromedriver")
            if os.path.exists("/usr/bin/chromedriver")
            else Service()
        )
        return webdriver.Chrome(service=service, options=options)

    # Local fallback
    return webdriver.Chrome(options=options)


def scrape_website(website):
    # Ensure URL has scheme
    if not website.startswith(("http://", "https://")):
        website = f"https://{website}"

    print(f"Scraping: {website}")
    driver = get_driver()

    try:
        driver.get(website)
        time.sleep(3)
        html = driver.page_source
        return html
    finally:
        driver.quit()


def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    return str(body_content) if body_content else ""


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length]
        for i in range(0, len(dom_content), max_length)
    ]