"""
FILE: test.py
PURPOSE: Data Ingestion and Validation Schema

This file is a utility module responsible for safely loading the raw data from
'tests.jsonl' into structured Python objects so the evaluation engine can interact
with it cleanly.

--- CLASSES ---
1. TestQuestion (Pydantic BaseModel):
   Acts as a strict blueprint for what a valid test case must look like. When reading
   the JSONL file, if a line is missing a 'question' string or a list of 'keywords',
   Pydantic will instantly throw a validation error rather than letting the script
   fail silently later during the evaluation math.

--- FUNCTIONS ---
2. load_tests():
   Calculates the absolute path to 'tests.jsonl'. It opens the file, reads it line-by-line,
   parses the JSON string into a Python dictionary, and pushes that dictionary through
   the `TestQuestion` Pydantic model for validation. It returns a clean, fully validated
   list of TestQuestion objects ready for the eval.py script.
"""

import json
from pathlib import Path
from pydantic import BaseModel, Field

TEST_FILE = str(Path(__file__).parent / "tests.jsonl")


class TestQuestion(BaseModel):
    """A test question with expected keywords and reference answer."""

    question: str = Field(description="The question to ask the RAG system")
    keywords: list[str] = Field(description="Keywords that must appear in retrieved context")
    reference_answer: str = Field(description="The reference answer for this question")
    category: str = Field(description="Question category (e.g., direct_fact, spanning, temporal)")


def load_tests() -> list[TestQuestion]:
    """Load test questions from JSONL file."""
    tests = []
    with open(TEST_FILE, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line.strip())
            tests.append(TestQuestion(**data))
    return tests
