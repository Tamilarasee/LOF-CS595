from pydantic import BaseModel, Field as PydanticField
from typing import Optional, List, Dict, Any


class MedicationMatcherInput(BaseModel):
    """
    TODO:
    Input model for the medication matcher agent.
    
    Fields:
    - conditions: List of patient's diagnosed medical conditions and problems
                 Used to analyze potential medication interactions and contraindications
                 Example: ["Type 2 Diabetes", "Hypertension"]
    
    - medications: List of patient's current and past medications
                  Used to track medication history and evaluate drug combinations
                  Example: ["Metformin 500mg", "Lisinopril 10mg"]
    
    - patient_id: Unique identifier for the patient in the FHIR system
                 Used to retrieve additional patient details if needed
                 Example: "patient-123456"
    """
