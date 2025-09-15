import requests
from langchain.agents import Tool
from config.settings import PUSHOVER_TOKEN, PUSHOVER_USER, PUSHOVER_URL

def push(text: str):
    """Send a push notification to the user"""
    requests.post(PUSHOVER_URL, data={"token": PUSHOVER_TOKEN, "user": PUSHOVER_USER, "message": text})
    return "success"

def get_notification_tool():
    """Get a tool for sending push notifications"""
    return Tool(
        name="send_push_notification", 
        func=push, 
        description="Use this tool when you want to send a push notification"
    )
