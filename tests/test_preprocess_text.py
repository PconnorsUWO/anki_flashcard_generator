import os
import sys
import asyncio
import tempfile
import unittest
import json
import datetime
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'scripts')))
from src.preprocess_text import preprocess_text


class TestPreprocessText(unittest.TestCase):
    def setUp(self):
        self.test_output_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "tests", "test_output"
        )
        if os.path.exists(self.test_output_dir):
            for filename in os.listdir(self.test_output_dir):
                file_path = os.path.join(self.test_output_dir, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")
        os.makedirs(self.test_output_dir, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.temp_input = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
        self.notes_output_path = os.path.join(
            self.test_output_dir, f"notes_{timestamp}.txt"
        )
        self.flashcards_output_path = os.path.join(
            self.test_output_dir, f"flashcards_{timestamp}.json"
        )
        sample_text = """
        # Machine Learning Basics
        
        ## Supervised Learning
        Supervised learning is a type of machine learning where models are trained using labeled data.
        Common algorithms include:
        - Linear Regression
        - Decision Trees
        - Support Vector Machines
        - Neural Networks
        
        ## Unsupervised Learning
        Unsupervised learning uses unlabeled data to identify patterns.
        Examples include:
        - Clustering (K-means, hierarchical)
        - Dimensionality reduction (PCA)
        - Association rule learning
        """
        with open(self.temp_input.name, 'w', encoding='utf-8') as f:
            f.write(sample_text)
        self.temp_input.close()

    def tearDown(self):
        try:
            os.unlink(self.temp_input.name)
        except Exception as e:
            print(f"Error cleaning up input file: {e}")

        print("Test output files saved to:")
        print(f"  - Flashcards: {self.flashcards_output_path}")

    async def _test_preprocess(self):
        result = await preprocess_text(self.temp_input.name, self.flashcards_output_path)
        self.assertTrue(os.path.exists(self.flashcards_output_path), "Output file was not created")

        with open(self.flashcards_output_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertGreater(len(content), 0, "Output file is empty")

        with open(self.flashcards_output_path.replace('_raw.txt', ''), 'w', encoding='utf-8') as f:
            f.write(result)

        self.assertIn("question", result, "No questions found in output")
        self.assertIn("answer", result, "No answers found in output")
        print("Preprocessing test completed successfully!")
        print(f"All output files saved to {self.test_output_dir}")
        return result

    def test_preprocess_text(self):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self._test_preprocess())


if __name__ == "__main__":
    unittest.main()