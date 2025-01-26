from langchain_google_genai import GoogleGenerativeAI
from typing import Any

def call_llm(prompt:str | list[str | dict[Any, Any]]) -> str:
    """this function calls the Google Generative AI model to generate a response based on the prompt"""
    from core.config import gemini_api_key
    
    llm = GoogleGenerativeAI(model="gemini-1.5-flash", api_key=gemini_api_key)
    result = llm.invoke(prompt)
    return result