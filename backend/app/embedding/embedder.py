import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


class Embedder:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set.")

        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-embedding-2"
        self.output_dimensionality = 768

    def encode(self, text: str) -> list[float]:
        result = self.client.models.embed_content(
            model=self.model_name,
            contents=text,
            config=types.EmbedContentConfig(
                output_dimensionality=self.output_dimensionality,
            ),
        )

        return result.embeddings[0].values