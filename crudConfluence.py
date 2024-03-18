from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
import requests, json
import os
from dotenv import load_dotenv
import base64
from bs4 import BeautifulSoup


load_dotenv()

BASE_URL = "https://ai-test-ktruch.atlassian.net/wiki"
USERNAME = os.environ['CONFLUENCE_USERNAME']
CONFLUENCE_API_TOKEN = os.environ['CONFLUENCE_API_TOKEN']

auth_string = f"{USERNAME}:{CONFLUENCE_API_TOKEN}".encode("utf-8")
auth_string_b64 = base64.b64encode(auth_string).decode()

def getListContent():
    response = requests.get(
        f"{BASE_URL}/rest/api/content",
        headers={"Authorization": f"Basic {auth_string_b64}"},
    )
    print("Loading titles...")
    if response.status_code == 200:
        listOfTitles = []
        for content in response.json()["results"]:
            title = content["title"]
            content_id = content["id"]
            print(f"Title: {title}, ID:{content_id}")
            listOfTitles.append(f"Title: {title}, ID:{content_id}")
        return listOfTitles
        # return response.json()

    else:
        return "Error: {response.status_code} - {response.text}"
    
def getArticle(id: int):
    response = requests.get(
        f"{BASE_URL}/rest/api/content/{id}?expand=body.storage",
        headers={"Authorization": f"Basic {auth_string_b64}"},
    )
    if response.status_code == 200:
        article_data = response.json()
        text_content = article_data.get("body", {}).get("storage", {}).get("value", "")
        # return BeautifulSoup(text_content).get_text()
        return text_content

    else:
        return "Error: {response.status_code} - {response.text}"
        
