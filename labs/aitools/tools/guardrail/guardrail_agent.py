from agents import OpenAIChatCompletionsModel, Agent, RunContextWrapper, GuardrailFunctionOutput, Runner
from openai import AsyncOpenAI

from labs.aitools.constants import openai_api_key
from labs.aitools.tools.guardrail.model import MedicalQueryOutput


def create_guardrail_agent(use_openai=False):
    """
    Create a guardrail agent that checks if a query is medical-related.
    The agent returns a JSON with the following structure:
      {
         "is_medical_query": <true/false>,
         "reasoning": "<explanation text>"
      }
    For example, for a query about symptoms or treatments, the agent should return:
      {"is_medical_query": true, "reasoning": "The query mentions symptoms or treatments."}
    Otherwise, it returns:
      {"is_medical_query": false, "reasoning": "The query is non-medical."}
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
                api_key="dummy-key"  # Ollama doesn't check API keys, but the client requires one
            )
        )

    instructions = (
        "Check if the user's query is related to medical information or healthcare data. "
        "Return a JSON object with exactly two keys: 'is_medical_query' (a boolean) and 'reasoning' (a string). "
        "For example, if the query mentions symptoms or treatments, return "
        "{\"is_medical_query\": true, \"reasoning\": \"The query mentions symptoms or treatments.\"}. "
        "If the query is non-medical, return "
        "{\"is_medical_query\": false, \"reasoning\": \"The query is non-medical.\"}."
    )

    return Agent(
        name="Medical Query Checker",
        instructions=instructions,
        output_type=MedicalQueryOutput,
        model=model
    )


async def medical_query_guardrail(ctx: RunContextWrapper, agent: Agent, input_data: str) -> GuardrailFunctionOutput:
    """
    Guardrail function to determine if a query is medical-related.

    Args:
        ctx: The run context wrapper
        agent: The agent instance
        input_data: The user's input query

    Returns:
        GuardrailFunctionOutput with evaluation results and whether the tripwire was triggered
    """
    guardrail_agent = create_guardrail_agent(use_openai=True)
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(MedicalQueryOutput)
    is_medical = final_output.is_medical_query if isinstance(final_output.is_medical_query, bool) else False

    print(f"Guardrail evaluation: {final_output}, interpreted is_medical: {is_medical}")

    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not is_medical,
    )
