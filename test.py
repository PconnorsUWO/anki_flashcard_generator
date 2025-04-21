from src.llm import LLMClient
from dotenv import load_dotenv
from src.preprocess_text import preprocess_text
import os

load_dotenv()
our_client = LLMClient(api_key=os.getenv("LLM_API_KEY"))

output = preprocess_text(
    "data/8 Trees and Ensembles.pdf",
    "out/out.txt",
    [
    "prompts/raw_to_processed.txt",
    "prompts/processed_to_notes.txt"
    ],
    our_client,
)