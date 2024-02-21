#from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer
from django.contrib.auth.models import User  # Or your custom user model
from django.shortcuts import get_object_or_404

# Create your views here
 


class MessageViewSet(viewsets.ViewSet):
    """
    A viewset that provides to create (send) a msg, retrieve a msg and delete a msg.
    """
    permission_classes = [permissions.IsAuthenticated]
    def create(self, request):
        if not 'receiver' in request.data:
            return Response({'missing field': "receiver must be provided"}, status=status.HTTP_400_BAD_REQUEST)
        if not "subject" in request.data:
            return Response({'missing field': "subject must be provided"}, status=status.HTTP_400_BAD_REQUEST)
        if not "message" in request.data:
            return Response({'missing field': "message must be provided"}, status=status.HTTP_400_BAD_REQUEST)

        receiver_id = request.data['receiver']
        receiver = get_object_or_404(User, pk=receiver_id)
        new_message = Message(sender=request.user, receiver=receiver, subject=request.data['subject'], message=request.data['message'] )
        new_message.save()
        return Response({'id': new_message.id})

    def retrieve(self, request,pk=None):
         try:
            message = Message.objects.filter(receiver=request.user).get(pk = pk)
         except:
            return Response({'not found': 'messages not found.'}, status=status.HTTP_404_NOT_FOUND)
         else:
             serializer = MessageSerializer(message)
             response_data = serializer.data
             message.has_been_read = True
             message.save()
             return Response(response_data)

    def destroy(self, request,pk):
        message = get_object_or_404(Message, pk=pk)
		#try:
            #message = Message.objects.get(pk=pk)
        #except:
            #return Response({'detail': 'Message not found.'}, status=status.HTTP_404_NOT_FOUND)
        #else:
        if True:
        # Check if the request.user is the sender or receiver of the message
            if request.user == message.sender or request.user == message.receiver:
                message.delete()
                return Response({'success': f"Message {pk} deleted successfully."})#, status=status.HTTP_204_NO_CONTENT)
            return Response({'forbidden': 'You do not have permission to delete this message.'}, status=status.HTTP_403_FORBIDDEN)




class AllMessageViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing all messages sent to the logged-in user.
    """
    permission_classes = [permissions.IsAuthenticated]
    def list(self, request):
        all_messages = Message.objects.filter(receiver=request.user).all()
        if all_messages:
            serializer = MessageSerializer(all_messages, many=True)
            response_data = serializer.data
            all_messages.update(has_been_read = True)
            return Response(serializer.data)
        return Response({'not found': 'No messages found.'}, status=status.HTTP_404_NOT_FOUND)


class UnreadMessageViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing unread messages sent to the logged-in user.
    """
    permission_classes = [permissions.IsAuthenticated]
    def list(self, request):
        queryset = Message.objects.filter(receiver=request.user).filter(has_been_read = False).all()
        if queryset:
            serializer = MessageSerializer(queryset, many=True)
            response_data = serializer.data
            queryset.update(has_been_read = True)
            return Response(response_data)
        return Response({'detail': 'No unread messages found.'}, status=status.HTTP_404_NOT_FOUND)

