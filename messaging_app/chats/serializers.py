from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    full_name = serializers.CharField(source="get_full_name", read_only=True)  # Derived field for full name

    class Meta:
        model = User
        fields = [
            'user_id', 'username', 'first_name', 'last_name',
            'email', 'phone_number', 'role', 'created_at', 'full_name'
        ]
        read_only_fields = ['user_id', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model.
    """
    sender_email = serializers.CharField(source='sender.email', read_only=True)  # Nested field for sender email

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_email', 'conversation', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation model.
    """
    participants = serializers.SerializerMethodField()  # Custom field for participant names
    messages = MessageSerializer(many=True, read_only=True, source='messages')

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']

    def get_participants(self, obj):
        """
        Returns a list of participant full names.
        """
        return [participant.get_full_name() for participant in obj.participants.all()]

    def validate(self, data):
        """
        Custom validation for conversation creation.
        """
        if len(data.get('participants', [])) < 2:
            raise serializers.ValidationError("A conversation must have at least two participants.")
        return data
