from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests
from django.http import JsonResponse
import json
import os
from chat_ai.models import ChatSession
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url='/login/') 
def chat_box_area_view(request):
    return render(request, 'chat.html')


@login_required(login_url='/login/') 
@csrf_exempt
def chat_completion(request):
    GROQ_API_KEY = os.getenv("TOKEN")
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")

        if not user_message:
            return JsonResponse({"error": "Message is required"}, status=400)

        try:
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            }

            payload = {
                "model": "llama3-8b-8192",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a healthSync AI assistant created by Davis. You provide responses related to all aspects of health, "
                            "including physical health, nutrition, fitness, medical advice, disease prevention, "
                            "mental well-being, stress management, and overall wellness. "
                            "If the user asks about unrelated topics, gently guide them back to health-related discussions."
                        )

                    },
                    {"role": "user", "content": user_message}
                ],
            }

            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload,
            )

            ai_response = response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response")

            # Retrieve or create a chat session for the user
            chat_session, created = ChatSession.objects.get_or_create(user=request.user)

            # Update conversation history
            chat_session.conversation.append({"user_message": user_message, "ai_response": ai_response})
            chat_session.save()

            return JsonResponse({"reply": ai_response})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@login_required(login_url='/login/') 
def get_chat_history(request):
    try:
        # Get the latest chat session for the user
        chat_session = ChatSession.objects.filter(user=request.user).first()
        
        # Return the conversation history if available
        if chat_session:
            return JsonResponse({"conversation": chat_session.conversation}, safe=False)
        else:
            return JsonResponse({"conversation": []})  # Return an empty conversation if none exist

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)