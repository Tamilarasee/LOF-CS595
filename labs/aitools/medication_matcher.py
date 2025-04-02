import logging
from typing import Optional, List, Dict, Any
import dotenv
import streamlit as st
from agents import Runner
import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from labs.aitools.constants import patient_data
from labs.aitools.tools.enhancer.enhancer_agent import create_result_enhancer_agent
from labs.aitools.tools.fhir.fhir_agent import create_fhir_agent
from labs.aitools.tools.guardrail.guardrail_agent import create_guardrail_agent
from labs.aitools.tools.medication.matcher_agent import create_medication_matcher_agent

dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO)

st.set_page_config(page_title="FHIR Healthcare Assistant", layout="wide")


def analyze_medication_condition_relationships(conditions: List[str], medications: List[str],
                                               patient_id: str = "1") -> str:
    """
    Analyze which medications are treating which conditions using the Medication Condition Matcher agent.

    Args:
        conditions: List of patient conditions
        medications: List of patient medications
        patient_id: The ID of the patient

    Returns:
        Analysis of which medications are treating which conditions
    """
    try:

        medication_matcher = create_medication_matcher_agent(use_openai=True)

        # TODO:
        # Construct a prompt for the medication matcher agent to analyze:
        # - Patient ID
        # - List of conditions
        # - List of medications
        # The agent will identify medication-condition relationships, uses, and interactions

        matcher_input = f"""
        """

        result = Runner.run_sync(medication_matcher, matcher_input)
        return result.final_output
    except Exception as e:
        return f"Error analyzing medication-condition relationships: {str(e)}"


def main():
    """
    Main function to run the Streamlit application with the FHIR Healthcare Assistant.
    """
    st.title("FHIR Healthcare Assistant")

    st.sidebar.title("Model Settings")
    use_openai = st.sidebar.checkbox("Use OpenAI (gpt-4o-mini)", value=False,
                                     help="Check to use OpenAI's gpt-4o-mini model. Uncheck to use local Ollama with llama3.2")

    st.markdown("Ask me about patient data or healthcare information.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    primary_agent = create_fhir_agent(use_openai)
    enhancer_agent = create_result_enhancer_agent(use_openai)
    guardrail_agent = create_guardrail_agent(use_openai)

    if not primary_agent or not enhancer_agent or not guardrail_agent:
        return

    model_name = "OpenAI (gpt-4o-mini)" if use_openai else "Ollama (llama3.2)"
    st.sidebar.info(f"Currently using: {model_name}")

    if prompt := st.chat_input("Ask about patient data or healthcare information"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()

            try:

                with st.spinner(f"Thinking using {model_name}..."):
                    import asyncio
                    import json
                    import re

                    # TODO:
                    #streamlit run medication_matcher.py
                    # Step-by-step process:
                    # 1. Set up asyncio event loop for async operations
                    # 2. Get primary response from the agent using the user's prompt
                    # 3. Extract conditions and medications from patient data
                    # 4. If no conditions/medications found in patient data:
                    #    - Parse conditions and medications from the primary output using regex
                    # 5. Prepare input string for the enhancer agent with:
                    #    - Original response
                    #    - User query
                    #    - Extracted conditions and medications
                    # 6. Get enhanced response from enhancer agent
                    # 7. If both conditions and medications exist:
                    #    - Analyze medication-condition relationships
                    #    - Add analysis to final output
                    # 8. Display final output and update session state


            except Exception as e:
                error_message = f"Error: {str(e)}"
                message_placeholder.markdown(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})


if __name__ == "__main__":
    main()
