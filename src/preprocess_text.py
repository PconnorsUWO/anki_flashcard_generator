# src/preprocess_text.py
from src.llm import LLMClient
from src.utils import extract_text_from_file, log_info, log_error
from dotenv import load_dotenv
from typing import List
import asyncio
from google import genai
from google.genai import types
from google.genai.types import HarmCategory, HarmBlockThreshold
import os
import json

async def preprocess_text(input_filepath: str, output_filepath: str) -> str:
    try:
        log_info(f"Extracting text from {input_filepath}")
        extracted_text = extract_text_from_file(input_filepath)
        
        load_dotenv()
        api_key = os.getenv("LLM_API_KEY")
        
        log_info("Initializing first LLM client")
        llm_client_1 = LLMClient(api_key=api_key)
        client_1 = llm_client_1.get_client()
        assert client_1 is not None, "First LLM client is not initialized."

        log_info("Applying raw to notes prompt")
        response_1 = await client_1.aio.models.generate_content(
            model="gemini-2.5-flash-preview-04-17",
            contents=extracted_text,
            config=types.GenerateContentConfig(
                system_instruction=[
                    "You are a assistant hired by a professional organization to help with note-taking.",
                    "You will be given a text and you will convert it into notes.",
                    "**Include All Content:** We may expand further however do not leave out any content that is present in the text within the notes you provide.",
                    "**Clarify Fundamental Ideas:** Expand on any necessary background context or foundational concepts to ensure a deep understanding of the topic.",
                    "**Organize Information Effectively:** Structure your notes using clear headings, subheadings, and bullet points for better readability.",
                ]
            ),
        )
        
        notes_text = response_1.text
        log_info("Successfully converted raw text to notes")
        

        log_info("Initializing second LLM client")
        llm_client_2 = LLMClient(api_key=api_key)
        client_2 = llm_client_2.get_client()
        assert client_2 is not None, "Second LLM client is not initialized."
        
        log_info("Applying notes to JSON prompt")
        response_2 = await client_2.aio.models.generate_content(
            model="gemini-2.5-flash-preview-04-17",
            contents=notes_text,
            config=types.GenerateContentConfig(
                system_instruction="""I have a large amount of well-formatted text for a machine learning course. Please parse all of the context provided and create flashcards that capture every relevant detail (do not omit any key information unless it is merely filler). Each flashcard must be formatted as a Python dictionary in plain text, following this exact structure:

{
    "question": \"\"\"<b>Your question text here:</b><br><ul>
    <li>Option A</li>
    <li>Option B</li>
    <li>Option C</li>
    <li>Option D</li>
    <li>Option E</li>
</ul>\"\"\",
    "answer": "<b>Answer:</b> [Correct Option]"
}

Ensure that:
1. Every flashcard is enclosed in curly braces `{}` and flashcards are comma-separated.
2. The 'question' field uses HTML formatting (as shown) to present the question and options.
3. The 'answer' field clearly states the correct answer, also with HTML formatting.
4. The output is returned as plain text.
5. All relevant content from the input text is used to create comprehensive flashcards on the machine learning material.

Generate the flashcards accordingly.""",
                response_schema={
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "question": {
                                "type": "string",
                                "description": "HTML formatted question with multiple choice options. Format: '<b>Question text</b><br><ul><li>Option A</li><li>Option B</li>...</ul>'"
                            },
                            "answer": {
                                "type": "string", 
                                "description": "HTML formatted answer indicating the correct option. Format: '<b>Answer:</b> [Correct Option]'"
                            }
                        },
                        "required": ["question", "answer"]
                    }
                }
            ),
        )
        
        final_text = response_2.text

        final_text = response_2.text.strip()
        
        if final_text.startswith('[') and final_text.endswith(']'):
            pass  

        elif final_text.startswith('{') and final_text.endswith('}'):
            final_text = f"[{final_text}]"
        
        else:
            idx_list = [final_text.find('['), final_text.find('{')]
            idx_list = [idx for idx in idx_list if idx != -1]
            if not idx_list:
                raise ValueError("No valid JSON start found in response")
            start_idx = min(idx_list)
            final_text = final_text[start_idx:]
            
            if final_text.startswith('['):
                if ']' in final_text:
                    final_text = final_text[:final_text.rfind(']') + 1]
                else:
                    raise ValueError("No closing ']' found in response")
            elif final_text.startswith('{'):
                if '}' in final_text:
                    final_text = final_text[:final_text.rfind('}') + 1]
                    final_text = f"[{final_text}]"
                else:
                    raise ValueError("No closing '}' found in response")
        log_info("Successfully converted notes to JSON format")
        log_info(f"Saving processed text to {output_filepath}")
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(final_text)

    except Exception as e:
        log_error(f"Error in preprocessing: {e}")
        raise

    return final_text

if __name__ == '__main__':
    from config import INPUT_TEXT_FILE, PROCESSED_TEXT_FILE
    result = asyncio.run(preprocess_text(INPUT_TEXT_FILE, PROCESSED_TEXT_FILE))
    