from typing import Optional, List, Dict, Any
from labs.aitools.tools.fhir.model import FHIRCondition, FHIRMedicationRequest, FHIRMedication, FHIRPatient
import requests


class FHIRClient:
    """
    Client for interacting with a FHIR server.

    Provides methods to retrieve patient data, conditions, medications, and other healthcare information.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_patient_conditions(self, patient_id: str) -> List[FHIRCondition]:
        """
        Get conditions for a specific patient from the FHIR server.

        Args:
            patient_id: The ID of the patient to retrieve conditions for

        Returns:
            List of FHIRCondition objects
        """
        url = f"{self.base_url}/Condition?patient={patient_id}"
        response = requests.get(url, headers={"Accept": "application/fhir+json"})
        response.raise_for_status()

        data = response.json()
        conditions = []
        if "entry" in data:
            for entry in data["entry"]:
                if "resource" in entry:
                    conditions.append(FHIRCondition(**entry["resource"]))

        return conditions

    def get_patient_medications(self, patient_id: str) -> List[FHIRMedicationRequest]:
        """
        Get medication requests for a specific patient from the FHIR server.

        Args:
            patient_id: The ID of the patient to retrieve medications for

        Returns:
            List of FHIRMedicationRequest objects
        """
        url = f"{self.base_url}/MedicationRequest?patient={patient_id}"
        response = requests.get(url, headers={"Accept": "application/fhir+json"})
        response.raise_for_status()

        data = response.json()
        medications = []
        if "entry" in data:
            for entry in data["entry"]:
                if "resource" in entry:
                    medications.append(FHIRMedicationRequest(**entry["resource"]))

        return medications

    def get_medication_by_id(self, medication_id: str) -> Optional[FHIRMedication]:
        """
        Get a medication resource by its ID from the FHIR server.

        Args:
            medication_id: The ID of the medication to retrieve

        Returns:
            FHIRMedication object or None if not found
        """
        url = f"{self.base_url}/Medication/{medication_id}"
        response = requests.get(url, headers={"Accept": "application/fhir+json"})

        if response.status_code == 404:
            return None

        response.raise_for_status()
        data = response.json()

        return FHIRMedication(**data)

    def get_patient_by_id(self, patient_id: str) -> Optional[FHIRPatient]:
        """
        Get patient resource by its ID from the FHIR server.

        Args:
            patient_id: The ID of the patient to retrieve

        Returns:
            FHIRPatient object or None if not found
        """
        url = f"{self.base_url}/Patient/{patient_id}"
        response = requests.get(url, headers={"Accept": "application/fhir+json"})

        if response.status_code == 404:
            return None

        response.raise_for_status()
        data = response.json()

        return FHIRPatient(**data)


def get_fhir_client():
    """
    Initialize FHIR client with a fixed base URL.

    Returns:
        FHIRClient instance
    """
    fhir_base_url = "http://localhost:8080/fhir"
    return FHIRClient(fhir_base_url)
