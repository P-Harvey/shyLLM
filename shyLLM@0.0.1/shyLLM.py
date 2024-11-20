"""
File:           ./shyLLM.py
Name:           Self Host your (own) LLM
Description:    This module launches a local server
                using the uvicorn python package.
                Some attempts have been made to handle
                busy ports, however this is still experimental.

Created by:     P.L. Harvey
LICENSE:        Apache2.0
Copyright:      2024, P.L. Harvey

Modified on:    20241120
"""
import subprocess
from logging import Logger, getLogger, basicConfig, INFO
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from transformers.pipelines.base import Pipeline
from transformers.tokenization_utils import PreTrainedTokenizer
from transformers.tokenization_utils_fast import PreTrainedTokenizerFast

def run_scripts():
    """
    Runs all scripts in the /app directory.
    
    This function is not currently used in this example,
    but could be used to run other scripts in the future.
    """
    subprocess.run(["/app/run_script.sh"],
                   check = True)

# Setup logging
basicConfig(level = INFO)
logger: Logger = getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Replace with your desired model
# TODO: preload a lightweight and reliable model into
#       the docker container.
MODEL_NAME = "bartowski/Llama-3.2-3B-Instruct-GGUF"
logger.info("Loading model: %s",
            MODEL_NAME)

###########################################################################################
# try:
#     tokenizer = AutoTokenizer.from_pretrained(...)
#     model = AutoModelForCausalLM.from_pretrained(...)
#     llm_pipeline = pipeline(...)
# except Exception as e:
#     logger.error("Error loading model: %s", e)
#     # ... (handle the error, e.g., exit or return an error response)
###########################################################################################

# Load LLM model and tokenizer
tokenizer: PreTrainedTokenizer | PreTrainedTokenizerFast = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    use_fast = True,
    trust_remote_code = False,
    cache_dir = "./cache"
    )
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# Create pipeline
llm_pipeline: Pipeline = pipeline(
    "text-generation",
    model = model,
    tokenizer = tokenizer)

# Define request and response models using Pydantic
class Query(BaseModel):
    """
    Model for query parameters.
    
    Attributes:
        prompt (str): The input text to generate a
        response with.

        max_length (int): The maximum length of the
        generated response. Defaults to 100.

        temperature (float): The temperature control
        for the LLM model. Defaults to 1.0.

        top_p (float): The top-p threshold for the
        LLM model. Defaults to 0.95.
    """
    prompt: str = "Hello, introduce yourself briefly."
    max_length: int = 100
    temperature: float = 1.0
    top_p: float = 0.95

# API root endpoint
@app.get("/")
async def root() -> dict[str, str]:
    """
    Returns a message indicating that the LLM Backend
    is running.
    
    This endpoint serves as a placeholder and does not
    perform any actual functionality.
    """
    return {"message": "LLM Backend is running!"}

# Generate response endpoint
@app.post("/generate")
async def generate_text(query: Query,
                        api_key: str):
    """
    Generates a response to the input prompt using the
    LLM model.
    
    Args:
        query (Query): The input text to generate a
        response with.

        api_key (str): An API key for authentication
        (not currently used in this example).
    
    Returns:
        A dictionary containing the prompt and generated
        response.
    
    Raises:
        HTTPException: If an error occurs during generation
        or if no response is returned.
    """
    try:
        logger.info("Received query: %s", query.prompt)
        output = llm_pipeline(
            query.prompt,
            max_length = query.max_length,
            temperature = query.temperature,
            top_p = query.top_p,
        )
        return {
            "prompt": query.prompt,
            "response": output[0]["generated_text"]
            }
    except Exception as e:
        logger.error("Error generating text: %s",
                     e)
        raise HTTPException(
            status_code = 500,
            detail = "Failed to generate text."
            ) from e

# Streaming response endpoint
@app.post("/stream")
async def stream_text(query: Query):
    """
    Generates a streaming response to the input prompt using the LLM model.
    
    Args:
        query (Query): The input text to generate a response with.
    
    Returns:
        A FastAPI Response containing the generated response as plain text.
    
    Raises:
        HTTPException: If an error occurs during generation or if no response is returned.
    """
    try:
        output = llm_pipeline(
            query.prompt,
            max_length = query.max_length,
            temperature = query.temperature,
            top_p = query.top_p,
        )

        # TODO: Add markdown support
        response = Response(
            content = output[0]["generated_text"],
            media_type = "text/plain")
        
        return await response
    
    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail = "Error streaming text."
            ) from e
