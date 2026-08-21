# Import os module to verify system paths in containerized environments
import os

# Import time module to inject deterministic delays for client-side rendering
import time

# Import BeautifulSoup parser to navigate and sanitize HTML structure
from bs4 import BeautifulSoup

# Import Selenium webdriver interface to interact with Chrome binary
from selenium import webdriver

# Import Service class to pass executable driver paths to Selenium
from selenium.webdriver.chrome.service import Service


# Helper function to instantiate and return a headless browser instance
def get_driver():
    # Create configuration container for Chrome settings
    options = webdriver.ChromeOptions()

    # Enable modern headless mode to run without a GUI window
    options.add_argument("--headless=new")

    # Disable Linux sandbox security layer required for cloud VM execution
    options.add_argument("--no-sandbox")

    # Prevent out-of-memory crashes by disabling shared memory allocation
    options.add_argument("--disable-dev-shm-usage")

    # Disable GPU hardware acceleration
    options.add_argument("--disable-gpu")

    # Disable out-of-process network service
    options.add_argument("--disable-features=NetworkService")

    # Set virtual viewport dimensions to force full element rendering
    options.add_argument("--window-size=1920x1080")

    # Check for Debian/Ubuntu Chromium binary locations in cloud container
    if os.path.exists("/usr/bin/chromium") or os.path.exists(
        "/usr/bin/chromium-browser"
    ):
        # Assign explicit binary target path
        options.binary_location = (
            "/usr/bin/chromium"
            if os.path.exists("/usr/bin/chromium")
            else "/usr/bin/chromium-browser"
        )

        # Set Linux system ChromeDriver service path
        service = (
            Service("/usr/bin/chromedriver")
            if os.path.exists("/usr/bin/chromedriver")
            else Service()
        )

        # Initialize and return configured cloud Linux Chrome driver
        return webdriver.Chrome(service=service, options=options)

    # Return standard driver for local development environments
    return webdriver.Chrome(options=options)


# Main function to fetch complete DOM HTML from a given URL
def scrape_website(website):
    # Prepend HTTPS protocol if missing from input string
    if not website.startswith(("http://", "https://")):
        website = f"https://{website}"

    # Print target destination to console logs
    print(f"Scraping: {website}")

    # Instantiate Chrome driver instance
    driver = get_driver()

    # Execute request inside a try-finally block to guarantee process cleanup
    try:
        # Navigate browser to the specified URL
        driver.get(website)

        # Pause to allow asynchronous JavaScript scripts to execute
        time.sleep(3)

        # Retrieve rendered HTML source from the current active session
        html = driver.page_source

        # Return full HTML string
        return html
    finally:
        # Terminate browser instance to free system resources
        driver.quit()


# Helper function to extract only the <body> tag content
def extract_body_content(html_content):
    # Parse incoming raw HTML markup with BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Locate body node inside the parsed DOM tree
    body_content = soup.body

    # Return body HTML string if found, otherwise return empty string
    return str(body_content) if body_content else ""


# Helper function to strip script/style tags and normalize spacing
def clean_body_content(body_content):
    # Parse body HTML with BeautifulSoup
    soup = BeautifulSoup(body_content, "html.parser")

    # Iterate and extract all inline JavaScript and CSS tags
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Extract clean text separated by newline characters
    cleaned_content = soup.get_text(separator="\n")

    # Strip outer spacing and remove consecutive empty lines
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    # Return sanitized text payload
    return cleaned_content


# Helper function to chunk long text to adhere to LLM context boundaries
def split_dom_content(dom_content, max_length=6000):
    # Slice text using list comprehension into fixed-character subsets
    return [
        dom_content[i : i + max_length]
        for i in range(0, len(dom_content), max_length)
    ]