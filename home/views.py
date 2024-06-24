
from django.http import JsonResponse
import os;
from dotenv import load_dotenv
import requests
import json

load_dotenv()


def processMessages(request):
    data = json.loads(request.body)
    messages_text = data['message']
    api_url = os.getenv("API_URL")  

    headers = {
        'Content-Type': 'application/json',
        'Authorization':  f'Bearer {os.getenv("OPENAI_API_KEY")}'
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": messages_text}],
        # "max_tokens": 7,
        "temperature": 1
    }
    try:
        chatbot_res = requests.post(api_url, headers=headers, json=payload).json()
        return JsonResponse({'status': 'success', 'messages':  chatbot_res['choices'][0]['message']['content']}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


