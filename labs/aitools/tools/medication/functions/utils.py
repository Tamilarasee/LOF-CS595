from agents import function_tool

from lof.services import FDBService

@function_tool
def get_medication_info_from_fdb(drug_name: str) -> str:
    """
    Get detailed medication information from FDB (First Databank) database.

    Args:
        drug_name: Name of the medication to look up

    Returns:
        Formatted string with medication information from FDB
    """
    try:
        fdb_service = FDBService()
        result = fdb_service.get_drug_info(drug_name)

        if not result or "error" in result:
            return f"No information found in FDB for medication: {drug_name}"

        formatted_result = f"FDB Information for {drug_name}:\n"

        if "title" in result:
            formatted_result += f"- Name: {result['title']}\n"

        if "uses" in result:
            formatted_result += f"- Uses: {result['uses']}\n"

        if "description" in result:
            formatted_result += f"- response['content']['instructions']: {result['description']}\n"

        if "contraindications" in result and result["contraindications"]:
            formatted_result += "- Contraindications:\n"
            for contraindication in result["contraindications"]:
                formatted_result += f"  * {contraindication}\n"

        if "side_effects" in result and result["side_effects"]:
            formatted_result += "- Common Side Effects:\n"
            for effect in result["side_effects"]:
                formatted_result += f"  * {effect}\n"

        if "dosage" in result:
            formatted_result += f"- Typical Dosage: {result['dosage']}\n"

        if "interactions" in result and result["interactions"]:
            formatted_result += "- Drug Interactions:\n"
            for interaction in result["interactions"]:
                formatted_result += f"  * {interaction}\n"

        return formatted_result
    except Exception as e:
        return f"Error retrieving FDB information for {drug_name}: {str(e)}"