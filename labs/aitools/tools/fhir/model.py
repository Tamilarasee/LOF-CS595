from pydantic import BaseModel, Field as PydanticField
from typing import Optional, List, Dict, Any


class FHIRCondition(BaseModel):
    """
    TODO:
    Pydantic model representing a FHIR Condition resource.
    Contains information about a patient's diagnosed condition or problem.

    Fields:
    - id: Unique identifier for the condition
    - code: Dictionary containing the condition code and coding system info
    - subject: Dictionary containing reference to the patient this condition belongs to
    - clinicalStatus: Optional dictionary with status codes (active, resolved, etc)
    - verificationStatus: Optional dictionary with verification state (confirmed, provisional, etc) 
    - onsetDateTime: Optional string containing when the condition began
    """



class FHIRMedication(BaseModel):
    """
    TODO:
    Pydantic model representing a FHIR Medication resource.
    Contains information about a medication, including its code and status.

    Fields:
    - id: Unique identifier for the medication
    - code: Dictionary containing the medication code and coding system info
    - status: String indicating if medication is active, inactive, etc
    """



class FHIRMedicationRequest(BaseModel):
    """
    TODO:
    Pydantic model representing a FHIR MedicationRequest resource.
    Contains information about a medication prescription, including dosage instructions.

    Fields:
    - id: Unique identifier for the medication request
    - status: String indicating request status (active, completed, etc)
    - intent: String specifying type of request (order, plan, etc)
    - subject: Dictionary containing reference to the patient
    - medicationCodeableConcept: Optional dictionary with medication coding info
    - medicationReference: Optional dictionary with reference to medication resource
    - authoredOn: Optional string containing when request was created
    - dosageInstruction: Optional list of dictionaries with dosing details
    """



class FHIRPatient(BaseModel):
    """
    TODO:
    Pydantic model representing a FHIR Patient resource.
    Contains demographic and contact information about a patient.

    Fields:
    - id: Unique identifier for the patient
    - name: List of dictionaries containing patient name components
    - gender: Optional string with patient's gender
    - birthDate: Optional string with patient's date of birth
    - address: Optional list of dictionaries with address details
    - telecom: Optional list of dictionaries with contact info (phone, email)
    - maritalStatus: Optional dictionary with marital status codes
    """

