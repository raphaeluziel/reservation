from bot.chat import check_user_role
from django.shortcuts import render
from .models import Dialogue
import datetime
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
import json


def chat(request):
    return render(request, 'chatbot/chatbot.html')


@csrf_protect
def chatbot(request):
    if request.method == 'POST':
        # Get the user's message from the POST request
        data = json.loads(request.body)
        message = data['message']
        # Process the message using the chatbot model
        response = check_user_role(message)
        # Save the dialogue to the database
        Dialogue.objects.create(user=message, bot=response)
        # Get the current time
        current_time = datetime.datetime.now()
        # Convert the timestamp to a string
        timestamp_string = current_time.strftime('%Y-%m-%d %H:%M:%S')
        data = {
            'answer': response
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'error'})
