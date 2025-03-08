import streamlit as st
import requests
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Constants
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './../..')))
# It ensures that Python can find and import modules that are located two directories up (./../..) 
# from the current script's directory.
from labs.tokenization.constants import TOKEN_PROMPT
from lof.services import IMONLPService

MAX_CHARS = 10000
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
#Update your openrouter key
OPENROUTER_API_KEY = "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"

#Python's @dataclass decorator is used to create a class that mainly stores data, without writing boilerplate code manually.
#Automatically generates a constructor (__init__) so you don’t have to write:
# def __init__(self, text, semantic_type, codes, source, assertion):
#     self.text = text
#     self.semantic_type = semantic_type
#     self.codes = codes
#     self.source = source
#     self.assertion = assertion

@dataclass
class TokenizationResult:
    text: str
    semantic_type: str
    codes: Dict[str, str]
    source: str
    assertion: str

def format_codes_with_assertion(result_type, result_data):
    if result_type not in result_data:
        return ""
    
    codes = ", ".join(f"{k}: {v}" for k, v in result_data[result_type].codes.items())
    assertion = result_data[result_type].assertion
    
    return f"Assertion: {assertion}, {codes}" if codes else ""

def process_entity_codes(entity: Dict, source: str) -> TokenizationResult:
    """
    TODO: Implement process_entity_codes
    Process entity codes from medical text tokenization
    Steps:
    1. Initialize empty codes dictionary
    2. Check if entity contains codemaps
    3. For each coding system in codemaps:
        a. If system is IMO and source is IMO, use lexical_code
        b. Otherwise, if codes array exists and not empty:
            - Use rxnorm_code if available (Drug domain)
            - Otherwise use generic code field (Other domains)
    4. Return TokenizationResult with:
        - Original text
        - Semantic type
        - Processed codes
        - Source system
        - Clinical assertion
    """
    codes = {}

    
    # Your implementation here

    # Check if the entity has codemaps
    if 'codemaps' in entity and entity['codemaps']:
        for system, code_data in entity['codemaps'].items():
            # Check if the coding system is IMO and the source is IMO
            if system == 'imo' and source == 'IMO':
                if 'lexical_code' in code_data:
                    codes[system] = code_data['lexical_code']  # Use lexical_code if available
            else:
                # Proceed only if the codes array exists and is not empty
                if 'codes' in code_data and code_data['codes']:
                    # Use rxnorm_code if available (Drug domain)
                    if entity['semantic'] == "drug":
                        codes[system] = code_data['codes'][0].get('rxnorm_code', None)
                    else:
                        # Use the generic code field for other domains
                        codes[system] = code_data['codes'][0].get('code', None)



    return TokenizationResult(
        text=entity['text'],
        semantic_type=entity['semantic'],
        codes=codes,
        source=source,
        assertion=entity['assertion']
    )


#In Python, an abstract class is a blueprint for other classes. It cannot be instantiated directly 
# and ensures that derived classes must implement certain methods. Inherits from ABC() Abstract Base Class)
#@abstractmethod forces subclasses to implement the tokenize method.
#This guarantees that all tokenizers return a list of TokenizationResult objects.
class BaseTokenizer(ABC):
    @abstractmethod
    def tokenize(self, text: str) -> List[TokenizationResult]:
        pass


class OpenRouterTokenizer(BaseTokenizer):
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    def tokenize(self, text: str) -> List[TokenizationResult]:
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8501",
                "X-Title": "Medical Note Tokenizer"
            }
            payload = {
                "messages": [
                    {"role": "system", "content": TOKEN_PROMPT},
                    {"role": "user", "content": text}
                ],
                "model": self.model,
                "response_format": {"type": "json_object"}
            }
            response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            content = response.json()['choices'][0]['message']['content']
            data = json.loads(content)

            results = []
            for entity in data['entities']:
                results.append(process_entity_codes(entity, 'OpenRouter'))

            return results
        except Exception as e:
            st.error(f"OpenRouter API Error: {str(e)}")
            raise e


class IMOTokenizer(BaseTokenizer):
    def tokenize(self, text: str) -> List[TokenizationResult]:
        try:
            data = IMONLPService().tokenize_text(text=text)
            entities_to_consider = ['problem', 'drug','treatment', 'imo_procedure', 'test']
            results = []
            for entity in data['entities']:
                if entity['semantic'] not in entities_to_consider:
                    continue
                #print(entity)
                results.append(process_entity_codes(entity, 'IMO'))
            return results
        except Exception as e:
            st.error(f"IMO API Error: {str(e)}")
            raise e


def check_file_size(content: str) -> bool:
    """Check if file content is within character limit."""
    return len(content) <= MAX_CHARS


def display_comparison(openrouter_results: List[TokenizationResult], imo_results: List[TokenizationResult]):
    """
    TODO: Display comparison of OpenRouter and IMO tokenization results by:
    1. Creating dictionary to store results by text (upper case for case-insensitive matching)
    2. Adding OpenRouter results with codes to dictionary, skipping empty codes
    3. Adding IMO results with codes and semantic type to dictionary, skipping empty codes 
    4. Creating combined table with:
        - Text from original input
        - Semantic type from IMO results
        - OpenRouter codes with assertions
            Use format_codes_with_assertion to format codes with assertions
        - IMO codes with assertions
            Use format_codes_with_assertion to format codes with assertions
    5. Displaying combined table using Streamlit dataframe
    """
    st.subheader("Token(Unique) Details")

    # Create dictionary to store results by text
    results_by_text = {}
    
    # Add OpenRouter results
    for result in openrouter_results:
            if result.codes:
                results_by_text[result.text.upper()] = {
                    'OpenRouter': result
                }
        

    # Add IMO results and semantic type
    for result in imo_results:
        if result.codes and result.semantic_type:
            text_key = result.text.upper()
            if text_key in results_by_text:
                results_by_text[text_key]['IMO'] = result
            else:
                results_by_text[text_key] = {
                    'IMO': result                        
                }
        

    # Create combined table
    combined_table = []
    for text, entry in results_by_text.items():
        #print(entry)
        combined_entry = {
            'Text': text,
            'Semantic Type': entry['IMO'].semantic_type if 'IMO' in entry else None,
            'OpenRouter Codes': format_codes_with_assertion('OpenRouter', entry),
            'IMO Codes': format_codes_with_assertion('IMO', entry)
        }
        
        # Append to combined table
        combined_table.append(combined_entry)
    st.dataframe(combined_table, use_container_width=True)


def main():
    st.title("Medical Note Tokenizer")

    # Navigation panel
    with st.sidebar:
        st.header("Navigation")

        # Model selection
        model_choice = st.selectbox(
            "Select OpenRouter Model",
            ["google/gemini-2.0-flash-lite-preview-02-05:free"]
        )

        st.write("Upload a text file to tokenize its content.")
        # File upload
        uploaded_file = st.file_uploader("Choose a text file", type=["txt"])

    if uploaded_file:
        content = uploaded_file.read().decode()

        if not check_file_size(content):
            st.error(f"File exceeds maximum limit of {MAX_CHARS} characters.")
            return

        st.subheader("File Content")
        st.text_area("Original Text", value=content, height=200, disabled=True)

        if st.button("Tokenize"):
            with st.spinner("Processing..."):
                openrouter_tokenizer = OpenRouterTokenizer(OPENROUTER_API_KEY, model_choice)
                imo_tokenizer = IMOTokenizer()

                openrouter_results = openrouter_tokenizer.tokenize(content)
                imo_results = imo_tokenizer.tokenize(content)

                display_comparison(openrouter_results, imo_results)


if __name__ == "__main__":
    main()
