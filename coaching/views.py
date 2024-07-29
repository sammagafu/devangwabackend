from rest_framework import viewsets
from .models import Event, Participant 
from .serializers import EventSerializer, ParticipantSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated,IsAdminUser



class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.action == 'create':
            self.permission_classes = [IsAdminUser]
        elif self.action == 'attend':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super().get_permissions()

# class SessionViewSet(viewsets.ModelViewSet):
#     queryset = Session.objects.all()
#     serializer_class = SessionSerializer

class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
