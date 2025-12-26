def extract_text(resp) -> str:
    """
    Normalize LLM response content across providers
    """
    content = resp.content

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        # Gemini often returns list of strings
        joined = []
        for item in content:
            if isinstance(item, str):
                joined.append(item)
            elif isinstance(item, dict) and "text" in item:
                joined.append(item["text"])
        return "\n".join(joined).strip()

    return str(content).strip()
