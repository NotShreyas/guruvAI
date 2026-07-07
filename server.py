from fastapi import FastAPI, HTTPException, Body, Request
import asyncio
import conva_ai
from fastapi.responses import FileResponse
import boto3
import os
import json
import base64
from typing import Callable
from functools import wraps
from fastapi.middleware.cors import CORSMiddleware

# Initialize the FastAPI app
app = FastAPI()
response = None
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# AWS Polly client setup
aws_region = os.getenv("AWS_REGION", "us-east-1")
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

session_kwargs = {"region_name": aws_region}
if aws_access_key_id and aws_secret_access_key:
    session_kwargs["aws_access_key_id"] = aws_access_key_id
    session_kwargs["aws_secret_access_key"] = aws_secret_access_key

polly_client = boto3.Session(**session_kwargs).client("polly")

# Initialize the AsyncConvaAI bot
assistant_id = os.getenv("CONVA_ASSISTANT_ID")
api_key = os.getenv("CONVA_API_KEY")
assistant_version = os.getenv("CONVA_ASSISTANT_VERSION", "46.0.0")

if not assistant_id or not api_key:
    raise RuntimeError("Set CONVA_ASSISTANT_ID and CONVA_API_KEY before starting the app.")

bot = conva_ai.AsyncConvaAI(
    assistant_id=assistant_id,
    api_key=api_key,
    assistant_version=assistant_version,
)

# def supress_exception(*args: type[Exception]) -> Callable:
#     def decorator(func: Callable) -> Callable:
#         @wraps(func)
#         def wrapper(*argsinner, **kwargs):
#             try:
#                 return func(*argsinner, **kwargs)
#             except args as e:
#                 print(f"Supressed Error in {func.__qualname__}: {e}")
#         return wrapper
#     return decorator

# ses = Session(region_name="us-east-1")
# polly = ses.client("polly")


def synthesize(ssml:str):

    # Generate speech using AWS Polly
    response = polly_client.synthesize_speech(
        VoiceId='Matthew',
        OutputFormat='mp3',
        TextType="ssml",
        Text=ssml,
    )
    
    output_file = 'response.mp3'
    
    # Save the audio to a file
    # with open(output_file, 'wb') as file:
    #     file.write(response['AudioStream'].read())
    
    # Return the audio file
    return base64.b64encode(response['AudioStream'].read()).decode('utf-8')

# Async function to invoke capability
async def get_response(text: str):
    global response
    try:
        resp = await bot.invoke_capability(text, history=response.conversation_history if response else "{}")
        messages = resp.message
        print(resp.parameters)
        voiceFile = synthesize(resp.parameters["ssml"]) if resp.parameters.get("ssml",None) else False
        response = resp
        return {
            "response": messages,
            "parameters": resp.parameters,
            "voiceFile": voiceFile
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# API endpoint to invoke capability
@app.post("/invoke_capability/")
async def invoke_capability(data: dict=Body(...)):
    return await get_response(data.get("text"))

# API endpoint to invoke a capability by name
@app.post("/invoke_capability_name/{capability_name}")
async def invoke_capability_name(capability_name: str,data: dict=Body(...)):
    global response
    try:
        resp = await bot.invoke_capability_name(data.get("text"), capability_name, history=response.conversation_history if response else "{}")
        print(resp.parameters)
        voiceFile = synthesize(resp.parameters["ssml"]) if resp.parameters["ssml"] else False
        response = resp
        return {
            "response": resp.message,
            "parameters": resp.parameters,
            "voiceFile": voiceFile
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
