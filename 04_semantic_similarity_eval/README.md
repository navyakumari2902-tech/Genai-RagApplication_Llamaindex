Semantic Similarity Evaluation with LlamaIndex

This repository demonstrates how to evaluate semantic similarity between two texts using the LlamaIndex evaluation framework.

The script compares a response text with a reference text and calculates a similarity score based on embeddings. It also determines whether the similarity meets a defined threshold.

This project is part of my LlamaIndex and Generative AI learning journey.

Overview

Semantic similarity measures how close two texts are in meaning, even if the wording is different.

For example:

Response:

cat is on the table
mat is on the floor

Reference:

table is occupied by cat
floor is occupied by mat

Even though the wording differs, both texts express the same meaning.
The evaluator detects this using embedding-based similarity scoring.

Module Used

This example uses the following component from LlamaIndex:

SemanticSimilarityEvaluator

Import path:

from llama_index.core.evaluation import SemanticSimilarityEvaluator
Purpose

The evaluator:

Computes semantic similarity between two texts

Uses embedding models to capture meaning

Returns evaluation results including:

Output	Description
score	Similarity score between response and reference
passing	Boolean indicating whether the similarity exceeds the threshold

Default similarity threshold: 0.8

Project Structure
semantic-similarity-llamaindex
│
├── semantic_similarity.py
└── README.md

This repository contains a single Python script demonstrating semantic similarity evaluation.

Implementation Logic

The script follows these steps:

Import the SemanticSimilarityEvaluator

Initialize the evaluator

Define a response text and reference text

Run the evaluator to compute semantic similarity

Print the similarity score and pass/fail result

Code
from llama_index.core.evaluation import SemanticSimilarityEvaluator

# Create evaluator instance
evaluator = SemanticSimilarityEvaluator()

# Function to evaluate semantic similarity
def evaluate_similarity():

    response = """cat is on the table
                  mat is on the floor"""

    reference = """table is occupied by cat
                   floor is occupied by mat"""

    result = evaluator.evaluate(
        response=response,
        reference=reference
    )

    print("score:", result.score)
    print("pass:", result.passing)


def main():
    evaluate_similarity()


if __name__ == "__main__":
    main()
Installation

Install the required dependencies:

pip install llama-index
pip install openai
Running the Script

Run the program:

python semantic_similarity.py
Example Output
score: 0.91
pass: True

Explanation:

score → similarity between the response and reference texts

pass → indicates whether the score meets the threshold (0.8)

Common Error
OpenAI Quota Error

Example error:

RateLimitError: You exceeded your current quota
Reason

This occurs when:

OpenAI API quota is exhausted

Billing is not enabled

API key is not configured

Solution

Set your OpenAI API key:

Linux / Mac:

export OPENAI_API_KEY="your_api_key"

Windows PowerShell:

setx OPENAI_API_KEY "your_api_key"

Ensure that billing and quota are active in your OpenAI account.