"""
File:           ./shyLLM.py
Name:           Self Host your (own) LLM
Description:    This module launches a local server using FastAPI
                to serve a large language model (LLM).
                It dynamically loads the specified LLM, handles
                requests for text generation, and provides health checks.
                It uses environment variables for configuration
                and implements basic API key authentication.

Created by:     P.L. Harvey
LICENSE:        Apache2.0
Copyright:      2024, P.L. Harvey

Modified on:    20241120  (Update with current date when modifying)
"""
from functools import lru_cache
from logging import Logger, getLogger, basicConfig, INFO
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator, ValidationError
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from transformers.pipelines.base import Pipeline
from transformers.tokenization_utils import PreTrainedTokenizer
from transformers.tokenization_utils_fast import PreTrainedTokenizerFast

# --- Configuration ---

# Retrieve environment variables for model name and API key.
MODEL_NAME: str = os.environ.get(
    "MODEL_NAME",
    "Qwen/Qwen2.5-Coder-7B-Instruct"
    )  # Default model if not specified.

# API key for authentication (optional).
API_KEY: str | None = os.environ.get("SHYLLM_API_KEY")

# --- Logging Setup ---

# Set the basic logging level to INFO.
basicConfig(level = INFO)

# Get a logger instance for this module.
logger: Logger = getLogger(__name__)

# --- FastAPI App Initialization ---

# Create a FastAPI application instance.
app = FastAPI()

# --- Model Loading ---

# Cache the loaded model to improve performance.
@lru_cache(maxsize = 1)
def load_model(model_name: str) -> Pipeline:
    """
    Loads the specified LLM model and tokenizer.

    Args:
        model_name (str): The name of the LLM model to load.

    Returns:
        Pipeline: A transformers pipeline object for text generation.

    Raises:
        Exception: If the model fails to load. 
        The exception is re-raised to be handled by the API endpoint.
    """
    try:
        tokenizer: PreTrainedTokenizer | PreTrainedTokenizerFast = AutoTokenizer.from_pretrained(
            model_name
            )
        model = AutoModelForCausalLM.from_pretrained(
            model_name
            )
        return pipeline("text-generation",
                        model = model,
                        tokenizer = tokenizer)
    except Exception as e:
        logger.exception("Error loading model %s: %s",
                         model_name, e)
        raise


# --- Request Data Model ---

class Query(BaseModel):
    """
    Represents the input query for text generation.
    """
    prompt: str
    max_length: int = 100
    temperature: float = 1.0
    top_p: float = 0.95

    @field_validator("prompt")
    def prompt_not_empty(cls, v):
        """
        Validates that the prompt is not empty.
        """
        errors = []
        if not v:
            errors.append(ValueError("Prompt cannot be empty"))
        if not isinstance(v, str):
            errors.append(TypeError("Prompt must be a string"))
        if errors:
            raise ValidationError(errors, cls)
        return v.strip()

    @field_validator("max_length")
    def validate_max_length(cls, v) -> int:
        """
        Validates that max_length is a strictly pos. integer.
        """
        if not isinstance(v, int) or v <= 0:
            raise ValidationError(
                [ValueError("max_length must be a positive integer")],
                cls
                )
        return v

# --- API Endpoints ---

@app.get("/")
async def root():
    """
    Root endpoint: returns a welcome message.
    """
    return {"message": "LLM Backend is running!"}


@app.get("/health")
async def health_check():
    """
    Health check endpoint: returns the server status.
    """
    return {"status": "ok"}

@app.post("/generate")
async def generate_text(query: Query,
                        api_key: str = ''):
    """
    Generates text based on the provided prompt.

    Args:
        query (Query): The input query containing the prompt and parameters.
        api_key (str, optional):  The API key for authentication.
        Defaults to the value of the environment variable API_KEY.

    Returns:
        dict: A dictionary containing the prompt and the generated response.

    Raises:
        HTTPException: 401 Unauthorized if the API key is incorrect.
        HTTPException: 500 Internal Server Error if text generation fails.
    """
    # Check and compare with API_KEY from the environment
    if api_key and api_key != API_KEY:
        raise HTTPException(status_code = 401,
                            detail = "Unauthorized API key provided.")

    try:
        llm_pipeline: Pipeline = load_model(MODEL_NAME)
        output = llm_pipeline(
            query.prompt,
            max_length = query.max_length,
            temperature = query.temperature,
            top_p = query.top_p,
        )
        return {
            "prompt": query.prompt,
            "response": output[0]["generated_text"],
        }
    except Exception as e:
        logger.exception("Error generating text")
        raise HTTPException(status_code = 500,
                            detail = "Failed to generate text.") from e
