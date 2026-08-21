# Import python-dotenv to load environment variables from a local .env file
from dotenv import load_dotenv

# Load key-value pairs from .env into os.environ for local execution
load_dotenv()

# Import streamlit to construct the web application user interface
import streamlit as st

# Import the DOM scraping and text processing helper functions from scrape.py
from scrape import (
    scrape_website,
    split_dom_content,
    clean_body_content,
    extract_body_content,
)

# Import the Groq LLM parsing pipeline function from parse.py
from parse import parse_with_ollama

# Render the application header title in the browser
st.title("AI WEB SCRAPER")

# Render a single-line text input field where users enter a target URL
url = st.text_input("Enter a URL : ")

# Trigger the scraping workflow when the user clicks the "Scrape Site" button
if st.button("Scrape Site"):
    # Display a status update notification to the user
    st.write("Scrapping the website")

    # Fetch the complete raw HTML DOM from the website via Selenium
    result = scrape_website(url)

    # Filter out header/metadata tags to isolate the <body> section
    body_content = extract_body_content(result)

    # Strip script/style tags and clean redundant whitespace
    cleaned_content = clean_body_content(body_content)

    # Store the cleaned text inside Streamlit session_state for persistence
    st.session_state.dom_content = cleaned_content

    # Create an expandable UI dropdown container to inspect the raw extracted text
    with st.expander("View DOM content"):
        # Display the full extracted text within a scrollable text area component
        st.text_area("DOM Content", cleaned_content, height=300)


# Check if cleaned DOM text exists in state before displaying parse controls
if "dom_content" in st.session_state:
    # Render a multiline text area for the user's natural language parsing request
    parse_description = st.text_area("Describe what you want to parse?")

    # Trigger LLM extraction when the user clicks the "Parse Content" button
    if st.button("Parse Content"):
        # Verify that the instruction string is not empty
        if parse_description:
            # Display a processing status message to the UI
            st.write("Parsing the content")

            # Slice the DOM string into manageable character chunks for LLM context limits
            dom_chunks = split_dom_content(st.session_state.dom_content)

            # Send prompt and chunks sequentially to the Groq LLM API
            result = parse_with_ollama(dom_chunks, parse_description)

            # Render the final AI-extracted response onto the screen
            st.write(result)