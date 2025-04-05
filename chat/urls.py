from django.urls import path
from .views import ChatRoomListCreateView, MessageListCreateView

urlpatterns = [
    path('rooms/', ChatRoomListCreateView.as_view(), name='room-list'),
    path('messages/<int:room_id>/', MessageListCreateView.as_view(), name='message-list'),
]
