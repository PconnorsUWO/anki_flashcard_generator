## Overview

This project streamlines the process of turning your lecture notes, textbooks, or PDFs into ready-to-use Anki decks. It leverages large language models (LLMs) to extract, summarize, and format educational content into flashcards, saving you hours of manual work.

## Demo

### Project Workflow

![Project Workflow](PLACEHOLDER_FOR_WORKFLOW_IMAGE)

### Example Flashcards

![Flashcard Example 1](assets/wo_answer.png)
![Flashcard Example 2](assets/with_answer.png)

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

## Customization

- **Prompts:**  
  Modify the prompts in `src/preprocess_text.py` to suit your subject or style.

- **Deck Styling:**  
  Edit the CSS in `config.py` or `src/create_anki_deck.py` to change the look of your flashcards.

