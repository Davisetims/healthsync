from django.urls import path
from chat_ai.views import chat_box_area_view, chat_completion, get_chat_history

urlpatterns = [
    path("chat/", chat_box_area_view, name="chat"),
    path("askme/", chat_completion, name="askme"),
    path("chat/history/", get_chat_history, name="chat_history")
]