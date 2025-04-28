from pydantic import BaseModel


class MedicalQueryOutput(BaseModel):
    """
    Pydantic model for the output of the medical query guardrail.

    Determines whether a user query is medical-related and provides reasoning.
    """
    is_medical_query: bool
    reasoning: str
