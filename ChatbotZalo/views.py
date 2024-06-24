from django.http import JsonResponse, HttpResponse
import os;
from dotenv import load_dotenv
import requests
import json
import threading
from . import models
import queue

load_dotenv()

messages_queue = queue.Queue()


def process_and_send_message():
    while True:
        message_text, user_id =  messages_queue.get()
        try:
            res_bot = processMessages(messages_text=message_text)
            print(res_bot)
            if 'error' not in res_bot:
                token = getToken()
                res = SendMessages(token=token, user_id=user_id, messages=res_bot['messages'])
                print(f"Zalo response: {res}")
            else:
                print(f"Error processing messages: {res_bot.error}")
            messages_queue.task_done()
        except Exception as e:
            print(f"Error processing and sending message: {e}")
            messages_queue.task_done()

processing_thread = threading.Thread(target=process_and_send_message)
processing_thread.daemon = True
processing_thread.start()

def webhook_handler(request):
    data = json.loads(request.body.decode('utf-8'))
    message_text = data['message']['text']
    user_id = data['sender']['id']
    immediate_response = {"status": "success"}
    print(f"webhook user id: {user_id}")
    # try:    
    #     return HttpResponse(json.dumps(immediate_response), content_type='application/json')
    # except Exception as e:
    #     print(f"Error parsing webhook data: {e}")
    # message_thread = Thread(target=process_and_send_message, args=(message_text, user_id))
    # message_thread.start()
    messages_queue.put((message_text, user_id))
    return HttpResponse(json.dumps(immediate_response), content_type='application/json')
    # token = getToken()
    # print(f'token: {token}')
    # res = SendMessages(token=token, user_id=user_id, messages=res_messages)
    # print(res)
    # return HttpResponse(json.dumps(res), content_type='application/json')
def verify_domain(request):
    return HttpResponse(request, 'verify/index.html');

def getToken():
    access_token = models.get_access_token()
    if access_token == None or not access_token:
        access_token =  TokenByAuthCode()
    print("get token: ", access_token)
    return  access_token

def TokenByAuthCode():
    header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Secret_key': os.getenv("APP_SECRET_KEY")
    }
    payload = {
        'app_id': os.getenv("APP_ID"),
        'code': os.getenv("CODE"),
        'grant_type': os.getenv("GRANT_TYPE")
    }
    res = requests.post(os.getenv("GET_TOKEN_API"), headers=header, data=payload).json()
    print(res)
    updatedToken = models.updateToken(newAccessToken=res['access_token'],
                       newRefreshToken=res['refresh_token']
                       )
    print("updated token: ", updatedToken)
    return res['access_token']

def TokenByRefreshToken(refresh_token):
    header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Secret_key': os.getenv("APP_SECRET_KEY")
    }
    payload = {
        'app_id': os.getenv("APP_ID"),
        'refresh_token': refresh_token,
        'grant_type': "refresh_token"
    }
    res = requests.post(os.getenv("GET_TOKEN_API"), headers=header, data=payload).json()
    print(f"get token by refresh token: {res}")
    if res['error'] == -14014:
        access_token = TokenByAuthCode()
        return access_token
    updatedToken = models.updateToken(newAccessToken=res['access_token'],
                       newRefreshToken=res['refresh_token']
                       )
    print("updated token: ", updatedToken)
    return res['access_token']


def processMessages(messages_text):
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
        return {'messages':  chatbot_res['choices'][0]['message']['content']}
    except Exception as e:
        return {'error': str(e)}
def SendMessages(token, messages, user_id):
    api_url = "https://openapi.zalo.me/v3.0/oa/message/cs"
    print(f"send message user id: {user_id}")
    header = {
        'Content-Type': "application/json",
        'access_token': token
    }
    payload = { 
        "recipient":{
            "user_id": user_id
        },
        "message":{
            "text": messages
        }
    }
    
    res = requests.post(api_url, headers=header, json=payload).json()
    print(res)
    if(res['message'] == "Success"):
        print(200)
        return {"status": "success","response": res}
    elif (res['error'] == -216):
        print(300)
        refresh_token = models.get_refresh_token()
        access_token = TokenByRefreshToken(refresh_token)
        return SendMessages(access_token, messages, user_id)
    else:
        print(400)
        return {"status": "failed","response": res}


