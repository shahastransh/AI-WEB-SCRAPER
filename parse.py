import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. \n\n"
    "1. **Extract Information:** Only extract the information that directly matches: {parse_description}.\n"
    "2. **No Extra Content:** Do not include any additional text or commentary.\n"
    "3. **Empty Response:** If nothing matches, return an empty string ('').\n"
    "4. **Direct Data Only:** Provide only the explicitly requested data."
)

def parse_with_ollama(dom_chunks, parse_description):
    # Initializes Groq model using the GROQ_API_KEY environment variable
    model = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0)
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []
    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke({"dom_content": chunk, "parse_description": parse_description})
        parsed_results.append(response.content)

    return "\n".join(parsed_results)