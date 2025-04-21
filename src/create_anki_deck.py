# src/create_anki_deck.py
import random
import ast
import genanki
import json
import os
import sys
import datetime

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils import generate_unique_id, log_info, log_error

def load_flashcards(input_source: str) -> list:
    try:
        if os.path.exists(input_source):
            with open(input_source, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = input_source
            
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            try:
                parsed_data = ast.literal_eval(content)
                if isinstance(parsed_data, list):
                    return parsed_data
                elif isinstance(parsed_data, dict):
                    return [parsed_data]
                else:
                    raise ValueError("Data structure must be a list or dict")
            except (SyntaxError, ValueError) as e:
                log_error(f"Failed to parse content as JSON or Python literal: {e}")
                raise
                
    except Exception as e:
        log_error(f"Error loading flashcards from {input_source}: {e}")
        raise

def build_anki_deck(flashcards: list, deck_name: str, model: genanki.Model) -> genanki.Deck:
    deck = genanki.Deck(generate_unique_id(), deck_name)
    for card in flashcards:
        try:
            question = card['question']
            answer = card['answer']
        except KeyError as e:
            log_error(f"Missing key in flashcard: {e}")
            continue
        note = genanki.Note(
            model=model,
            fields=[question, answer]
        )
        deck.add_note(note)
    return deck

def create_anki_deck(input_json_path=None, output_dir=None, deck_name=None):
    # Set defaults if parameters are not provided
    if input_json_path is None:
        input_json_path = os.path.join("data", "flashcards_20250421_161832.json")
    
    if output_dir is None:
        output_dir = "out"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate output filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"anki_deck_{timestamp}.apkg"
    output_path = os.path.join(output_dir, output_filename)
    
    if deck_name is None:
        # Use the input filename as the deck name (without extension)
        deck_name = os.path.splitext(os.path.basename(input_json_path))[0]

    log_info(f"Creating Anki deck from {input_json_path}")
    
    anki_model = genanki.Model(
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

    flashcards = load_flashcards(input_json_path)
    deck = build_anki_deck(flashcards, deck_name, anki_model)
    
    try:
        genanki.Package(deck).write_to_file(output_path)
        log_info(f"Anki deck created and saved as {output_path}")
        return output_path
    except Exception as e:
        log_error(f"An error occurred while creating the Anki deck: {e}")
        raise

if __name__ == '__main__':
    create_anki_deck()