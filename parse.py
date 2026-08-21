import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import streamlit as st

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. \n\n"
    "1. **Extract Information:** Only extract the information that directly matches: {parse_description}.\n"
    "2. **No Extra Content:** Do not include any additional text or commentary.\n"
    "3. **Empty Response:** If nothing matches, return an empty string ('').\n"
    "4. **Direct Data Only:** Provide only the explicitly requested data."
)

CANDIDATE_MODELS = [
    "llama-3.3-70b-versatile",
    "openai/gpt-oss-120b",
    "qwen/qwen3.6-27b",
    "openai/gpt-oss-20b",
]


def parse_with_ollama(dom_chunks, parse_description):
    api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

    if not api_key:
        return "Error: GROQ_API_KEY is missing. Please add it to your Streamlit secrets."

    prompt = ChatPromptTemplate.from_template(template)

    # Try each available model until one succeeds
    for model_name in CANDIDATE_MODELS:
        try:
            model = ChatGroq(
                model_name=model_name,
                groq_api_key=api_key,
                temperature=0,
            )
            chain = prompt | model

            parsed_results = []
            for i, chunk in enumerate(dom_chunks, start=1):
                response = chain.invoke(
                    {
                        "dom_content": chunk,
                        "parse_description": parse_description,
                    }
                )
                parsed_results.append(response.content)

            return "\n".join(parsed_results)

        except Exception as e:
            if "NotFoundError" in str(e) or "404" in str(e):
                print(
                    f"Model {model_name} unavailable, attempting next candidate..."
                )
                continue
            raise e

    return "Error: None of the configured Groq models were reachable. Check your Groq console for available model IDs."