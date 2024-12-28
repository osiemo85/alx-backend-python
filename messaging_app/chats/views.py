from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username']  # Allow searching by participant usernames

    @action(detail=False, methods=['post'])
    def create_conversation(self, request):
        """
        Create a new conversation with participants.
        """
        participants = request.data.get('participants')
        if not participants or len(participants) < 2:
            return Response(
                {"error": "A conversation must have at least two participants."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            conversation = serializer.save()
            return Response(
                ConversationSerializer(conversation).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['sent_at']  # Allow ordering by the sent date

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """
        Send a message to an existing conversation.
        """
        conversation = self.get_object()
        sender = request.user
        message_body = request.data.get('message_body')

        if not message_body:
            return Response(
                {"error": "Message body cannot be empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body,
        )
        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED,
        )
