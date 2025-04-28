from agents import OpenAIChatCompletionsModel, Agent
from openai import AsyncOpenAI

from labs.aitools.constants import openai_api_key
from labs.aitools.tools.medication.functions.utils import get_medication_info_from_fdb
from labs.aitools.tools.search.functions.utils import search_duckduckgo


def create_medication_matcher_agent(use_openai=False):
    """
    Create an agent that matches medications to conditions.

    Args:
        use_openai: Boolean flag to use OpenAI instead of Ollama

    Returns:
        Agent instance configured to match medications to conditions
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
    TODO:
    Instructions for creating matcher_agent_instructions:
    1. Define the agent's role as a specialized healthcare assistant for medication matching
    2. Specify the data retrieval and analysis workflow:
       - Use FDB database for medication information
       - Use search for supplementary condition information
       - Analyze medication-condition relationships
    3. Set analysis requirements:
       - Match medications to conditions
       - Identify use cases
       - Check for interactions
    4. Define output format:
       - Present findings in tables
       - Include reasoning
       - Note uncertainties
       - Cite FDB sources
    """
    matcher_agent_instructions = """
        """

    """
    TODO:
    Instructions for creating Medication Matcher Agent:
    1. Set agent name as "Medication Condition Matcher"
    2. Use the detailed instructions defined above
    3. Configure required tools:
       - get_medication_info_from_fdb: Retrieves medication data
       - search_duckduckgo: Provides condition information
    4. Set output type to string for formatted results
    5. Use the specified language model
    """
    matcher = None
    return matcher
