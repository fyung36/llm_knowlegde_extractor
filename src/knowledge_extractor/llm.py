import json
from src.config import settings
from src.core.logger import get_logger
from openai import OpenAI

logger = get_logger("llm")

if not settings.USE_LLM_MOCK:
    client = OpenAI(api_key=settings.OPENAI_API_KEY)


def analyze_text(text: str):
    if settings.USE_LLM_MOCK:
        logger.info("Using mock LLM response.")
        return mock_llm_response(text)

    prompt = f"""
    Analyze the following text and return a JSON object with the following fields:
    - "title" (string, if available)
    - "topics" (list of 3 topics)
    - "sentiment" (positive, neutral, or negative)
    - "summary" (1–2 sentence summary)

    TEXT:
    {text}
    """

    try:
        logger.debug("Sending prompt to OpenAI")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts structured data from text."},
                {"role": "user", "content": prompt}
            ]
        )

        raw = response.choices[0].message.content
        logger.debug(f"Raw response from LLM:\n{raw}")

        parsed = json.loads(raw)

        summary = parsed.get("summary")
        if not summary:
            raise ValueError("Missing 'summary' in LLM response")

        logger.info("LLM response parsed successfully")
        return summary, {
            "title": parsed.get("title"),
            "topics": [t.lower() for t in parsed.get("topics", []) if isinstance(t, str)],
            "sentiment": parsed.get("sentiment", "neutral").lower()
        }

    except json.JSONDecodeError:
        logger.error("Invalid JSON from LLM")
        raise ValueError("LLM response could not be parsed as JSON.")
    except Exception as e:
        logger.exception("LLM API failed")
        raise RuntimeError(f"LLM API call failed: {str(e)}")


def mock_llm_response(text: str):
    logger.debug("Returning mocked LLM response")
    return (
        "This is a mock summary of the input text.",
        {
            "title": "Mock Title",
            "topics": ["mocking", "testing", "llm"],
            "sentiment": "neutral"
        }
    )
