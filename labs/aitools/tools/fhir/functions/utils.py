from agents import function_tool

from labs.aitools.constants import patient_data
from labs.aitools.tools.fhir.fhir_client import get_fhir_client

fhir_client = get_fhir_client()


@function_tool
def get_patient_conditions(patient_id: str) -> str:
    """
    Retrieve all conditions (diagnoses) for a specific patient from the FHIR server.

    Args:
        patient_id: The ID of the patient to retrieve conditions for

    Returns:
        Formatted string with patient conditions
    """
    try:
        conditions = fhir_client.get_patient_conditions(patient_id)
        if not conditions:
            return f"No conditions found for patient {patient_id}."

        patient_data["conditions"] = []

        result = f"Found {len(conditions)} conditions for patient {patient_id}:\n"
        for condition in conditions:
            display = condition.code.get("text", "Unknown condition")
            if not display and "coding" in condition.code:
                for coding in condition.code["coding"]:
                    if "display" in coding:
                        display = coding["display"]
                        break

            status = ""
            if condition.clinicalStatus and "coding" in condition.clinicalStatus:
                for coding in condition.clinicalStatus["coding"]:
                    if "code" in coding:
                        status = coding["code"]
                        break

            patient_data["conditions"].append({
                "name": display,
                "status": status or "unknown"
            })

            result += f"- {display} (Status: {status or 'unknown'})\n"

        return result
    except Exception as e:
        return f"Error retrieving conditions: {str(e)}"


@function_tool
def get_patient_medications(patient_id: str) -> str:
    """
    Retrieve all medication requests for a specific patient from the FHIR server.

    Args:
        patient_id: The ID of the patient to retrieve medications for

    Returns:
        Formatted string with patient medications
    """
    try:
        medications = fhir_client.get_patient_medications(patient_id)
        if not medications:
            return f"No medications found for patient {patient_id}."

        patient_data["medications"] = []

        result = f"Found {len(medications)} medication requests for patient {patient_id}:\n"
        for med in medications:
            med_name = "Unknown medication"

            if med.medicationCodeableConcept:
                if "text" in med.medicationCodeableConcept:
                    med_name = med.medicationCodeableConcept["text"]
                elif "coding" in med.medicationCodeableConcept:
                    for coding in med.medicationCodeableConcept["coding"]:
                        if "display" in coding:
                            med_name = coding["display"]
                            break
            elif med.medicationReference:
                if "reference" in med.medicationReference:
                    ref = med.medicationReference["reference"]
                    if ref.startswith("Medication/"):
                        med_id = ref.split("/")[1]
                        medication = fhir_client.get_medication_by_id(med_id)
                        if medication and medication.code:
                            if "text" in medication.code:
                                med_name = medication.code["text"]
                            elif "coding" in medication.code:
                                for coding in medication.code["coding"]:
                                    if "display" in coding:
                                        med_name = coding["display"]
                                        break

            dosage_info = ""
            if med.dosageInstruction and len(med.dosageInstruction) > 0:
                dosage = med.dosageInstruction[0]
                if "text" in dosage:
                    dosage_info = dosage["text"]

            patient_data["medications"].append({
                "name": med_name,
                "status": med.status,
                "dosage": dosage_info
            })

            result += f"- {med_name} (Status: {med.status}){' - Dosage: ' + dosage_info if dosage_info else ''}\n"

        return result
    except Exception as e:
        return f"Error retrieving medications: {str(e)}"


@function_tool
def get_patient_biography(patient_id: str) -> str:
    """
    Retrieve biographical information for a specific patient from the FHIR server.

    Args:
        patient_id: The ID of the patient to retrieve information for

    Returns:
        Formatted string with patient biographical information
    """
    try:
        patient = fhir_client.get_patient_by_id(patient_id)
        if not patient:
            return f"No patient found with ID {patient_id}."

        patient_data["biography"] = {}

        name = "Unknown"
        if patient.name and len(patient.name) > 0:
            name_parts = []
            if "given" in patient.name[0] and patient.name[0]["given"]:
                name_parts.extend(patient.name[0]["given"])
            if "family" in patient.name[0]:
                name_parts.append(patient.name[0]["family"])
            if name_parts:
                name = " ".join(name_parts)

        address = "Not available"
        if patient.address and len(patient.address) > 0:
            addr_parts = []
            addr = patient.address[0]
            if "line" in addr and addr["line"]:
                addr_parts.extend(addr["line"])
            if "city" in addr:
                addr_parts.append(addr["city"])
            if "state" in addr:
                addr_parts.append(addr["state"])
            if "postalCode" in addr:
                addr_parts.append(addr["postalCode"])
            if "country" in addr:
                addr_parts.append(addr["country"])
            if addr_parts:
                address = ", ".join(addr_parts)

        contact = "Not available"
        if patient.telecom and len(patient.telecom) > 0:
            contact_parts = []
            for telecom in patient.telecom:
                if "system" in telecom and "value" in telecom:
                    contact_parts.append(f"{telecom['system']}: {telecom['value']}")
            if contact_parts:
                contact = ", ".join(contact_parts)

        marital_status = "Not available"
        if patient.maritalStatus and "coding" in patient.maritalStatus:
            for coding in patient.maritalStatus["coding"]:
                if "display" in coding:
                    marital_status = coding["display"]
                    break

        patient_data["biography"] = {
            "name": name,
            "id": patient.id,
            "gender": patient.gender or "Not specified",
            "birthDate": patient.birthDate or "Not available",
            "maritalStatus": marital_status,
            "address": address,
            "contact": contact
        }

        result = f"Patient Information:\n"
        result += f"- Name: {name}\n"
        result += f"- ID: {patient.id}\n"
        result += f"- Gender: {patient.gender or 'Not specified'}\n"
        result += f"- Birth Date: {patient.birthDate or 'Not available'}\n"
        result += f"- Marital Status: {marital_status}\n"
        result += f"- Address: {address}\n"
        result += f"- Contact: {contact}\n"

        return result
    except Exception as e:
        return f"Error retrieving patient information: {str(e)}"
