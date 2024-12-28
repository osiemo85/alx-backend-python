# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import ConversationViewSet, MessageViewSet

# router = DefaultRouter()
# router.register(r'conversations', ConversationViewSet, basename='conversation')
# router.register(r'messages', MessageViewSet, basename='message')

# urlpatterns = [
#     path('', include(router.urls)),
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter  # Import NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Create a DefaultRouter instance
router = DefaultRouter()

# Register ConversationViewSet
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Create a NestedDefaultRouter instance to handle messages within conversations
conversation_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversation_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# Define URL patterns to include both the base routes and nested routes
urlpatterns = [
    path('', include(router.urls)),  # Include the base router URLs
    path('', include(conversation_router.urls)),  # Include the nested router URLs for messages
]
