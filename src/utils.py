# src/utils.py
import logging
import os
import PyPDF2 
import random
from src.llm import LLMClient

# Configure a basic logger for the project
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_info(message: str) -> None:
    logging.info(message)

def log_error(message: str) -> None:
    logging.error(message)

def extract_text_from_file(file_path: str) -> str:
    extension = os.path.splitext(file_path)[1].lower()
    if extension == ".pdf":
        text = ""
        try:
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text() or ""
                    text += page_text
        except Exception as e:
            log_error(f"Error reading PDF {file_path}: {e}")
            raise
    elif extension == ".txt":
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            log_error(f"Error reading text file {file_path}: {e}")
            raise
    else:
        log_error(f"Unsupported file type: {extension}")
        raise ValueError(f"Unsupported file type: {extension}")
    return text

def load_prompt(prompt_filepath: str) -> str:
    """Loads a prompt from a file."""
    try:
        with open(prompt_filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        log_error(f"Error loading prompt from {prompt_filepath}: {e}")
        raise

def generate_unique_id() -> int:
    return random.randrange(1 << 30, 1 << 31)