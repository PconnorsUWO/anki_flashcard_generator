# config.py
import genanki
from src.utils import generate_unique_id
# File paths
INPUT_TEXT_FILE = "data/8 Trees and Ensembles.txt"
PROCESSED_TEXT_FILE = "out/out.txt"
FLASHCARDS_JSON_FILE = "data/flashcards.json"
ANKI_OUTPUT_FILE = "data/flashcards.apkg"

# LLM API configuration (if applicable)
LLM_API_KEY = "your_api_key_here"
LLM_ENDPOINT = "https://api.your-llm-provider.com/v1/complete"


# Flashcards format
FLASHCARD_TEMPLATE = genanki.Model(
        generate_unique_id(),
        'Custom Flashcard Model',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Question}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
        ],
        css="""
        .card {
            font-family: Arial, sans-serif;
            font-size: 20px;
            text-align: left;
            color: black;
            background-color: white;
        }
        """
    )