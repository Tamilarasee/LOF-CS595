from agents import OpenAIChatCompletionsModel, Agent
from openai import AsyncOpenAI

from labs.aitools.constants import openai_api_key
from labs.aitools.tools.enhancer.functions.utils import normalize_medication_with_imo, normalize_problem_with_imo
from labs.aitools.tools.search.functions.utils import search_duckduckgo


def create_result_enhancer_agent(use_openai=False):
    """
    Create the result enhancer agent that improves responses from the primary agent.
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
    # Instructions for the enhancer agent that processes FHIR Healthcare Assistant responses
    # This prompt guides the agent to:
    # - Normalize medical terms using IMO services
    # - Add standardized medical codes and explanations 
    # - Format responses clearly with proper structure
    # - Only use factual information from available tools
    #
    # Detailed Guidelines:
    # 1. Response Enhancement:
    #    - Maintain original response integrity
    #    - Improve readability and organization
    #    - Add relevant medical context
    #
    # 2. Medical Term Processing:
    #    - Use IMO normalization for standardization
    #    - Include all available coding systems
    #    - Present codes in organized tables
    #
    # 3. Information Sources:
    #    - IMO services for medical terminology
    #    - DuckDuckGo for supplementary info
    #    - Original response content preservation
    #
    # 4. Quality Control:
    #    - No fabricated information
    #    - Verify all added content
    #    - Clear section organization
    """
    enhancer_instructions = """
        """
    
    """
    TODO:
    # Step 1: Create the Result Enhancer agent with a descriptive name
    # Step 2: Pass the detailed instructions defined above
    # Step 3: Add required tools:
    #   - DuckDuckGo search for additional medical information (search_duckduckgo)
    #   - IMO medication normalizer for standardizing drug names (normalize_medication_with_imo)
    #   - IMO problem normalizer for standardizing medical conditions (normalize_problem_with_imo)
    # Step 4: Set output type to string for text responses
    # Step 5: Use the specified language model for processing
    """
    enhancer = None
    return enhancer
