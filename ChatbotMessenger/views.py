from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.
@csrf_exempt
def handle_messenger_webhook(request):
    if request.method == 'GET':
        # Verification request from Meta
        data = json.loads(request.body)
        token = data['hub.verify_token']
        challenge = data['hub.challenge']
        print(token)
        print(challenge)
        if token == "22154041":
            return HttpResponse(challenge)
        else:
            return HttpResponse('Error, invalid token')

    # if request.method == 'POST':
    #     # Handle the incoming messages or events
    #     try:
    #         data = json.loads(request.body)
    #         print('Received data:', data)  # You can log or process the data here
    #         return JsonResponse({'status': 'success'}, status=200)
    #     except json.JSONDecodeError:
    #         return JsonResponse({'error': 'Invalid JSON'}, status=400)
    # return JsonResponse({'error': 'Invalid method'}, status=405)