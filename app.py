import os
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variable
API_KEY = os.getenv("ANTHROPIC_API_KEY")

# API endpoint
API_URL = "https://api.anthropic.com/v1/messages"

app = Flask(__name__)

def chat_with_claude(prompt):
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY,
        "anthropic-version": "2023-06-01"
    }
    
    data = {
        "model": "claude-3-sonnet-20240229",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(API_URL, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()["content"][0]["text"]
    else:
        return f"Error: {response.status_code} - {response.text}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    claude_response = chat_with_claude(user_message)
    return jsonify({'response': claude_response})

if __name__ == '__main__':
    app.run(debug=True)