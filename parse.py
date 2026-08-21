# Import the standard os module to access operating system environment variables
import os

# Import ChatPromptTemplate from LangChain to define parameterized model prompts
from langchain_core.prompts import ChatPromptTemplate

# Import ChatGroq class from langchain-groq to interface with the Groq API
from langchain_groq import ChatGroq

# Import Streamlit library to retrieve secrets configured in cloud deployment
import streamlit as st

# Define system instruction template for strict, non-conversational extraction
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. \n\n"
    "1. **Extract Information:** Only extract the information that directly matches: {parse_description}.\n"
    "2. **No Extra Content:** Do not include any additional text or commentary.\n"
    "3. **Empty Response:** If nothing matches, return an empty string ('').\n"
    "4. **Direct Data Only:** Provide only the explicitly requested data."
)

# Ordered list of supported model endpoints for automatic fallback handling
CANDIDATE_MODELS = [
    "llama-3.3-70b-versatile",
    "openai/gpt-oss-120b",
    "qwen/qwen3.6-27b",
    "openai/gpt-oss-20b",
]


# Main parsing handler function accepting text chunks and user query
def parse_with_ollama(dom_chunks, parse_description):
    # Attempt to read GROQ_API_KEY from Streamlit secrets dashboard or OS environment
    api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

    # Guard clause to notify user if the authentication key is absent
    if not api_key:
        return "Error: GROQ_API_KEY is missing. Please add it to your Streamlit secrets."

    # Initialize reusable prompt template from string definition
    prompt = ChatPromptTemplate.from_template(template)

    # Sequentially test candidate models to mitigate endpoint deprecation / 404 errors
    for model_name in CANDIDATE_MODELS:
        # Wrap API calls in exception handler to permit model failover
        try:
            # Instantiate Groq model client with zero temperature for deterministic outputs
            model = ChatGroq(
                model_name=model_name,
                groq_api_key=api_key,
                temperature=0,
            )

            # Build runnable LangChain pipeline using LCEL syntax
            chain = prompt | model

            # Array accumulator for individual chunk outputs
            parsed_results = []

            # Iterate through sliced text chunks
            for i, chunk in enumerate(dom_chunks, start=1):
                # Execute inference pipeline on current text chunk
                response = chain.invoke(
                    {
                        "dom_content": chunk,
                        "parse_description": parse_description,
                    }
                )

                # Append string content to result list
                parsed_results.append(response.content)

            # Return all aggregated chunk responses joined by a newline
            return "\n".join(parsed_results)

        # Catch exceptions thrown by unreachable or invalid model names
        except Exception as e:
            # Check if exception represents an endpoint lookup error
            if "NotFoundError" in str(e) or "404" in str(e):
                # Print debug message to console logs
                print(
                    f"Model {model_name} unavailable, attempting next candidate..."
                )

                # Skip to next model candidate in list
                continue

            # Re-raise any unrelated runtime or validation exceptions
            raise e

    # Fallback return value if all candidate models fail
    return "Error: None of the configured Groq models were reachable. Check your Groq console for available model IDs."