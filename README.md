# Automated Flashcard Generator

Automate the creation of high-quality Anki flashcards from your course materials using LLM-powered text processing!

---

## Overview

This project streamlines the process of turning your lecture notes, textbooks, or PDFs into ready-to-use Anki decks. It leverages large language models (LLMs) to extract, summarize, and format educational content into flashcards, saving you hours of manual work.

---

## Features

- **PDF and Text File Support:** Upload your study materials in `.pdf` or `.txt` format.
- **LLM-Powered Processing:** Automatically preprocesses and structures your content for optimal flashcard generation.
- **Anki Deck Export:** Generates `.apkg` files compatible with Anki.
- **Minimal Web Interface:** Simple, intuitive UI for uploading files and downloading decks.
- **Preview:** (Optional) See a sample of generated flashcards before downloading.

---

## Demo

### Project Workflow

![Project Workflow](PLACEHOLDER_FOR_WORKFLOW_IMAGE)

### Example Flashcards

![Flashcard Example 1]("Assets/wo_answer.png)")
![Flashcard Example 2]("Assets/with_answer.png")

---

## Directory Structure

```
.
├── src/                # Source code for processing and deck creation
├── data/               # Input and output files
├── tests/              # Unit tests
├── out/                # Generated decks and intermediate files
├── requirements.txt    # Python dependencies
├── config.py           # Configuration
├── README.md           # This file
└── ...
```

---

## How It Works

1. **Preprocess Text:**  
   Extracts and formats text from your input file for LLM comprehension.

2. **Generate Flashcards:**  
   Uses LLM prompts to create comprehensive flashcards in JSON format.

3. **Create Anki Deck:**  
   Converts the JSON flashcards into an Anki `.apkg` deck.

---

## Usage

1. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

2. **Set up your API keys:**  
   Create a `.env` file and add your LLM API key:
    ```
    LLM_API_KEY=your_api_key_here
    ```

3. **Run the generator:**
    ```sh
    python generate_flashcards.py <input_file> -o <output_dir> -n <deck_name>
    ```



---

## Customization

- **Prompts:**  
  Modify the prompts in `src/preprocess_text.py` to suit your subject or style.

- **Deck Styling:**  
  Edit the CSS in `config.py` or `src/create_anki_deck.py` to change the look of your flashcards.

---

## Contributing

Pull requests and suggestions are welcome! Please open an issue to discuss your ideas.

---

## License

[MIT License](LICENSE)

---

## Screenshots

> Replace the placeholders below with your own screenshots.

- ![Screenshot of Web UI](PLACEHOLDER_FOR_WEB_UI_IMAGE)
- ![Screenshot of Anki Deck](PLACEHOLDER_FOR_ANKI_DECK_IMAGE)
```
