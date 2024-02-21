from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'message', 'subject', 'creation_date']
""" 
    def create(self, validated_data):
        # The sender is automatically set to the request user.
        validated_data['sender'] = self.context['request'].user
        new_message = Message(validated_data)
        new_message.save()
        return JsonResponse({'id': new_message.id})

"""
