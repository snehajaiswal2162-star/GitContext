import os

from google import genai
from google.genai import errors
from dotenv import load_dotenv

load_dotenv()


class GeminiLLM:

    def __init__(
        self,
        model_name: str = "gemini-3.8-flash",
    ):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not set."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.model_name = model_name

    def generate(
        self,
        prompt: str,
    ) -> str:

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={
                    "temperature": 0.2,
                    "max_output_tokens": 512,
                },
            )

            return response.text

        except errors.ServerError:
            return (
                "The AI model is temporarily unavailable. "
                "Please try the question again in a few seconds."
            )

        except Exception as e:
            return f"LLM error: {str(e)}"