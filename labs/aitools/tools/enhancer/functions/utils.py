from agents import function_tool

from lof.services import IMONormalizeService


@function_tool
def normalize_medication_with_imo(medication_name: str) -> str:
    """
    Normalize a medication name using IMO Precision Normalize API

    Args:
        medication_name: Name of medication to normalize

    Returns:
        Formatted string with normalized medication data
    """
    try:
        imo_service = IMONormalizeService()
        result = imo_service.normalize_text(entities=[medication_name], domain="medication")

        if "error" in result:
            return f"Error normalizing medication: {result['error']}"

        formatted_result = "IMO Normalized Medication:\n"

        if "requests" in result and result["requests"]:
            response = result["requests"][0].get("response", {})
            if "items" in response and response["items"]:
                item = response["items"][0]
                imo_title = item.get("default_lexical_title", "")
                imo_code = item.get("default_lexical_code", "")
                imo_score = item.get("score", "")
                imo_match_type = item.get("match_type", "")

                formatted_result += f"- Title: {imo_title}\n"
                formatted_result += f"- Code: {imo_code}\n"
                if imo_score:
                    formatted_result += f"- Match Score: {imo_score}\n"
                if imo_match_type:
                    formatted_result += f"- Match Type: {imo_match_type}\n"

                if "semantic_tags" in item and item["semantic_tags"]:
                    tags = ", ".join(item["semantic_tags"])
                    formatted_result += f"- Semantic Tags: {tags}\n"

                if "ingredients" in item and item["ingredients"]:
                    formatted_result += "- Ingredients:\n"
                    for ing in item["ingredients"]:
                        ing_name = ing.get("name", "")
                        ing_code = ing.get("code", "")
                        if ing_name and ing_code:
                            formatted_result += f"  * {ing_name} ({ing_code})\n"
            else:
                formatted_result += "No normalized items found.\n"
        else:
            formatted_result += "No response data available.\n"

        return formatted_result
    except Exception as e:
        return f"Error processing IMO normalization: {str(e)}"

@function_tool
def normalize_problem_with_imo(problem_name: str) -> str:
    """
    Normalize a problem/condition name using IMO Precision Normalize API

    Args:
        problem_name: Name of problem/condition to normalize

    Returns:
        Formatted string with normalized problem data
    """
    try:
        imo_service = IMONormalizeService()
        result = imo_service.normalize_text(entities=[problem_name], domain="problem")

        if "error" in result:
            return f"Error normalizing problem: {result['error']}"

        formatted_result = "IMO Normalized Problem:\n"

        if "requests" in result and result["requests"]:
            response = result["requests"][0].get("response", {})
            if "items" in response and response["items"]:
                item = response["items"][0]
                imo_title = item.get("default_lexical_title", "")
                imo_code = item.get("default_lexical_code", "")
                imo_score = item.get("score", "")
                imo_match_type = item.get("match_type", "")

                formatted_result += f"- Title: {imo_title}\n"
                formatted_result += f"- Code: {imo_code}\n"
                if imo_score:
                    formatted_result += f"- Match Score: {imo_score}\n"
                if imo_match_type:
                    formatted_result += f"- Match Type: {imo_match_type}\n"

                if "semantic_tags" in item and item["semantic_tags"]:
                    tags = ", ".join(item["semantic_tags"])
                    formatted_result += f"- Semantic Tags: {tags}\n"
            else:
                formatted_result += "No normalized items found.\n"
        else:
            formatted_result += "No response data available.\n"

        return formatted_result
    except Exception as e:
        return f"Error processing IMO normalization: {str(e)}"