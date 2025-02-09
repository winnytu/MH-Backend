import requests
import json
import os
from dotenv import load_dotenv
from .exceptions import DifyAPIError, ValidationError

load_dotenv()

DIFY_API_KEY = os.getenv("DIFY_API_KEY")
DIFY_API_URL = os.getenv("DIFY_API_URL")

def get_recommended_departments(symptoms):
    """調用Dify API獲取推薦科別"""
    if not DIFY_API_KEY or not DIFY_API_URL:
        raise DifyAPIError("Missing Dify API configuration", 500)

    if not symptoms or not isinstance(symptoms, list):
        raise ValidationError("Symptoms must be a non-empty list")

    try:
        prompt = f"當有{symptoms}等症狀時,推薦看什麼科?只需要回覆科別即可,並以陣列格式回覆,並依優先順序排序."
        
        response = requests.post(
            f"{DIFY_API_URL}/chat-messages",
            headers={
                "Authorization": f"Bearer {DIFY_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "inputs": {},
                "query": prompt,
                "response_mode": "blocking",
                "conversation_id": "",
                "user": "user"
            }
        )
        
        if response.status_code != 200:
            error_message = response.json().get('message', 'Unknown error')
            raise DifyAPIError(f"Dify API request failed: {error_message}", response.status_code)
        
        try:
            answer_text = response.json()['answer']
            departments = json.loads(answer_text.replace("'", '"'))
            
            if not isinstance(departments, list):
                raise DifyAPIError("Invalid response format: expected list of departments")
            
            return departments
            
        except (json.JSONDecodeError, KeyError) as e:
            raise DifyAPIError(f"Failed to parse Dify API response: {str(e)}")
            
    except requests.RequestException as e:
        raise DifyAPIError(f"Network error while calling Dify API: {str(e)}") 