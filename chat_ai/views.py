from django.shortcuts import render,redirect
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
            # Retrieve or create a chat session
            chat_session, _ = ChatSession.objects.get_or_create(user=request.user)

            # Count total messages
            total_messages = len(chat_session.conversation)

            # If user is on a free plan and exceeds 5 messages, AI suggests upgrading
            if request.user.plan == "free" and total_messages >= 5:
                premium_message = (
                    "You have reached the free chat limit. "
                    "Upgrade to premium for unlimited access: "
                    "<a href='/premium/' style='color: blue; text-decoration: underline;'>Upgrade Now</a>"
                )
                return JsonResponse({"reply": premium_message})

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
                            "You are a health assistant. You ONLY provide responses related to health, "
                            "such as stress management, anxiety relief, therapy, self-care, and emotional well-being. "
                            "If the user asks an unrelated question, gently redirect the conversation to health topics."
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

            # Save conversation history
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
        
        if chat_session:
            # Count total messages (user + AI responses)
            total_messages = len(chat_session.conversation)  

            # Check if the user is on a free plan
            if request.user.plan == "free" and total_messages > 5:
                return redirect('premium')  # Change '/premium/' to your actual premium page URL

            return JsonResponse({"conversation": chat_session.conversation}, safe=False)
        else:
            return JsonResponse({"conversation": []})  # Return an empty conversation if none exist

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    

def premium(request):
    return render(request, 'premium.html')