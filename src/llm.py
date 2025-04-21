from google import genai

class LLMClient:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)

    def get_client(self) -> genai.Client:
        return self.client

    def set_client(self, client) -> None:
        self.client = client

    