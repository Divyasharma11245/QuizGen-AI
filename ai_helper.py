import os
import json
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors


# Load API key and model settings from .env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL")
FALLBACK_MODEL = os.getenv("GEMINI_FALLBACK_MODEL")


# Check configuration
if not API_KEY:
    raise ValueError(
        "Gemini API key not found. Please add it to your .env file."
    )

if not MODEL_NAME:
    raise ValueError(
        "Gemini model name not found. Please set GEMINI_MODEL in your .env file."
    )


# Connect to Gemini
client = genai.Client(api_key=API_KEY)


def call_gemini_with_fallback(prompt):
    """
    Call Gemini, retry temporary server errors,
    and optionally try a fallback model.
    """
    models_to_try = [MODEL_NAME]

    if FALLBACK_MODEL and FALLBACK_MODEL != MODEL_NAME:
        models_to_try.append(FALLBACK_MODEL)

    last_error = None

    for model_name in models_to_try:
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config={
                        "response_mime_type": "application/json",
                    },
                )
                return response

            except errors.ServerError as error:
                last_error = error

                # Wait before retrying.
                if attempt == 0:
                    time.sleep(1)

    raise RuntimeError(
        "Gemini could not complete the request with the configured model(s). "
        "Please check model availability and try again later. "
        f"Last server error: {last_error}"
    )


def generate_questions(
    topic,
    question_type,
    difficulty,
    number_of_questions,
    study_text="",
):
    """
    Generate questions using Gemini and return them as Python data.
    """

    # Use study material if provided; otherwise use the topic.
    if study_text and study_text.strip():
        content = study_text.strip()
    else:
        content = (topic or "").strip()

    if not content:
        raise ValueError("Please enter a topic or study material.")

    # Prepare instructions for the selected question type.
    if question_type == "MCQs":
        question_instructions = """
        Generate multiple-choice questions.
        Each question must have four options: A, B, C, and D.
        The answer must be the letter of the correct option.
        Include a short explanation.
        """

        answer_format = '"answer": "A"'

        options_format = """
        "options": {
            "A": "First option",
            "B": "Second option",
            "C": "Third option",
            "D": "Fourth option"
        }
        """
    else:
        question_instructions = """
        Generate short-answer questions.
        Include a correct, clear answer and a short explanation.
        The options object must be empty.
        """

        answer_format = '"answer": "Correct answer text"'
        options_format = '"options": {}'

    # Construct the prompt.
    prompt = f"""
You are an educational question-generation assistant.

Create exactly {number_of_questions} questions based on the academic
content provided below.

Difficulty level: {difficulty}
Question type: {question_type}

Instructions:
{question_instructions}

Return only a valid JSON array. Do not include markdown code fences
or any extra text.

Each question must follow this structure:
{{
    "question": "Question text",
    {options_format},
    {answer_format},
    "explanation": "Explanation of the answer"
}}

Academic content:
{content}
"""

    # Call Gemini with retry and fallback support.
    response = call_gemini_with_fallback(prompt)

    if not response.text:
        raise ValueError(
            "Gemini returned an empty response. Please try again."
        )

    # Convert the JSON response into Python objects.
    try:
        questions = json.loads(response.text)
    except json.JSONDecodeError as error:
        raise ValueError(
            "Could not process the AI response. Please try again."
        ) from error

    # Validate the overall response.
    if not isinstance(questions, list) or not questions:
        raise ValueError(
            "Gemini did not return a valid question list."
        )

    if len(questions) != number_of_questions:
        raise ValueError(
            f"Requested {number_of_questions} questions, "
            f"but Gemini returned {len(questions)}."
        )

    # Validate each question.
    required_fields = {
        "question",
        "options",
        "answer",
        "explanation",
    }

    for question in questions:
        if not isinstance(question, dict):
            raise ValueError("Invalid question format received.")

        if not required_fields.issubset(question):
            raise ValueError(
                "A generated question is missing required fields."
            )

        if not isinstance(question["question"], str):
            raise ValueError(
                "A generated question has invalid question text."
            )

        if not isinstance(question["options"], dict):
            raise ValueError("Invalid options format received.")

        if not isinstance(question["answer"], str):
            raise ValueError(
                "A generated question has an invalid answer."
            )

        if not isinstance(question["explanation"], str):
            raise ValueError(
                "A generated question has an invalid explanation."
            )

        # Validate MCQ options and answer.
        if question_type == "MCQs":
            expected_options = {"A", "B", "C", "D"}

            if not expected_options.issubset(question["options"]):
                raise ValueError(
                    "An MCQ does not contain all four required options."
                )

            if question["answer"].strip().upper() not in expected_options:
                raise ValueError(
                    "An MCQ answer must be A, B, C, or D."
                )

    return questions
