import os
import asyncio
import datetime
from src.preprocess_text import preprocess_text
from src.create_anki_deck import create_anki_deck
from src.utils import log_info, log_error
from dotenv import load_dotenv

async def generate_flashcards(
    input_filepath: str,
    output_dir: str = "out",
    deck_name: str = None
) -> str:
    """
    Generate Anki flashcards from an input file by preprocessing it and creating an Anki deck.
    
    Args:
        input_filepath: Path to the input file (PDF, TXT)
        output_dir: Directory where the output files will be saved
        deck_name: Name for the Anki deck (defaults to input filename)
        
    Returns:
        Path to the created Anki deck file
    """
    try:
        # Make sure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate timestamp for unique filenames
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Set interim and output filenames
        json_output_path = os.path.join(output_dir, f"flashcards_{timestamp}.json")
        
        if deck_name is None:
            # Use the input filename as the deck name (without extension)
            deck_name = os.path.splitext(os.path.basename(input_filepath))[0]
        
        log_info(f"Starting flashcard generation process for {input_filepath}")
        
        # Step 1: Preprocess text to generate JSON flashcards
        log_info(f"Preprocessing text from {input_filepath}")
        processed_json = await preprocess_text(input_filepath, json_output_path)
        log_info(f"Text preprocessing complete. JSON output saved to {json_output_path}")
        
        # Step 2: Create Anki deck from JSON flashcards
        log_info("Creating Anki deck from processed flashcards")
        anki_output_path = create_anki_deck(json_output_path, output_dir, deck_name)
        log_info(f"Anki deck created and saved to {anki_output_path}")
        
        return anki_output_path
        
    except Exception as e:
        log_error(f"Error in flashcard generation process: {e}")
        raise

# CLI script functionality
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate Anki flashcards from text or PDF files")
    parser.add_argument("input_file", help="Path to input file (PDF, TXT)")
    parser.add_argument("-o", "--output", default="out", help="Output directory")
    parser.add_argument("-n", "--name", help="Name for the Anki deck")
    args = parser.parse_args()
    
    # Load environment variables (.env)
    load_dotenv()
    
    # Run the flashcard generation process
    output_path = asyncio.run(generate_flashcards(
        args.input_file,
        args.output,
        args.name
    ))
    
    print(f"\nFlashcard generation complete!")
    print(f"Anki deck saved to: {output_path}")