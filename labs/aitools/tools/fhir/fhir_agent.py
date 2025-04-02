from agents import OpenAIChatCompletionsModel, Agent, InputGuardrail
from openai import AsyncOpenAI

from labs.aitools.constants import openai_api_key
from labs.aitools.tools.fhir.functions.utils import get_patient_biography, get_patient_conditions, \
    get_patient_medications
from labs.aitools.tools.guardrail.guardrail_agent import medical_query_guardrail


def create_fhir_agent(use_openai=False):
    """
    Create the primary FHIR healthcare assistant agent.

    Args:
        use_openai: Boolean flag to use OpenAI instead of Ollama

    Returns:
        Agent instance configured with FHIR tools
    """
    if use_openai:
        model = OpenAIChatCompletionsModel(
            model="gpt-4o-mini",
            openai_client=AsyncOpenAI(
                base_url="https://api.openai.com/v1",
                api_key=openai_api_key
            )
        )
    else:
        model = OpenAIChatCompletionsModel(
            model="llama3.2",
            openai_client=AsyncOpenAI(
                base_url="http://localhost:11434/v1",
                api_key="dummy-key"  # Ollama doesn't check API keys, but OpenAI client requires one
            )
        )

    """
    #TODO:
    # Instructions for creating FHIR Agent Instructions:
    # 1. Define the agent's role as a healthcare assistant
    # 2. Specify the data retrieval capabilities:
    #    - Biographical details (name, gender, DOB, etc)
    #    - Medical conditions and diagnoses
    #    - Medication information
    # 3. Set behavior guidelines:
    #    - Always request patient ID if missing
    #    - Present information clearly
    #    - No medical advice
    #    - Use tools only for patient data
    # 4. Define tool usage rules:
    #    - get_patient_biography for personal info (get_patient_biography)
    #    - get_patient_conditions for diagnoses (get_patient_conditions)
    #    - get_patient_medications for prescriptions (get_patient_medications)
    """
    fhir_agent_instructions = """
        """

    """
    TODO:
    Instructions for creating FHIR Agent:
    1. Set agent name as "FHIR Healthcare Assistant"
    2. Pass the detailed instructions defined above
    3. Configure required tools:
       - get_patient_biography: Retrieves patient demographic info (get_patient_biography)
       - get_patient_conditions: Retrieves patient diagnoses (get_patient_conditions)
       - get_patient_medications: Retrieves patient prescriptions (get_patient_medications)
    4. Add input guardrails for medical query validation
    5. Use the specified language model
    """
    fhir_agent = None

    return fhir_agent
