from functools import lru_cache
from typing import Union

from fastapi import FastAPI, Depends
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware

from atlassian import Confluence

# routers: comment out next line till create them
# from routers import pdfs
from routers import confluenceWiki

import config

# app = FastAPI()
readingConfluenceApp = FastAPI()

# router: comment out next line till create it
# app.include_router(pdfs.router)
readingConfluenceApp.include_router(confluenceWiki.router)

#origins = [
#    "http://localhost:3000",
#    "https://todo-frontend-khaki.vercel.app/",
#]

# CORS configuration, needed for frontend development
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
readingConfluenceApp.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# global http exception handler, to handle errors
# @app.exception_handler(StarletteHTTPException)
# async def http_exception_handler(request, exc):
#     print(f"{repr(exc)}")
#     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

# to use the settings
@lru_cache()
def get_settings():
    return config.Settings()


# @app.get("/")
# def read_root(settings: config.Settings = Depends(get_settings)):
#     # print the app_name configuration
#     print(settings.app_name)
#     return "Hello PDF World"


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

# readingConfluenceApp

# global http exception handler, to handle errors
@readingConfluenceApp.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    print(f"{repr(exc)}")
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

@readingConfluenceApp.get("/")
def read_root(settings: config.Settings = Depends(get_settings)):
    # print the app_name configuration
    print(settings.app_name)
    return "Hello Confluence World"

import os
from dotenv import load_dotenv
load_dotenv()
import requests, json
import urllib3
import base64

@readingConfluenceApp.get("/check")
def read_root():
    print("Inside check")
    
# Replace these variable values with your Confluence API credentials
    BASE_URL = "https://ai-test-ktruch.atlassian.net/wiki"
    USERNAME = os.environ['CONFLUENCE_USERNAME']
    CONFLUENCE_API_TOKEN = os.environ['CONFLUENCE_API_TOKEN']

    # Generate a base64 encoded string for basic authentication
    auth_string = f"{USERNAME}:{CONFLUENCE_API_TOKEN}".encode("utf-8")
    auth_string_b64 = base64.b64encode(auth_string).decode()

    # Make a GET request to fetch all content from Confluence API
    response = requests.get(
        f"{BASE_URL}/rest/api/content",
        headers={"Authorization": f"Basic {auth_string_b64}"},
    )

    if response.status_code == 200:
        # Iterate through the JSON response to get titles and ids of all content
        for content in response.json()["results"]:
            title = content["title"]
            content_id = content["id"]
            print(f"Title: {title}, ID:{content_id}")

    else:
        print(f"Error: {response.status_code} - {response.text}")
    return "Inside check"


