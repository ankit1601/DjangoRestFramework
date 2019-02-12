from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import generics
from .models import Polls,Choice,Vote
from rest_framework import status,viewsets
from .Serializers import PollsSerializer,ChoiceSerializer,VoteSerializer,UserSerializer
from django.contrib.auth import authenticate
from rest_framework import permissions,authentication

#Using API VIEW
# class PollList(APIView):
#     def get(self, request):
#         polls = Polls.objects.all()[:20]
#         data = PollsSerializer(polls,many=True).data
#         return Response(data)
#
# class PollDetails(APIView):
#     def get(self, request, pk):
#         poll = get_object_or_404(Polls, pk=pk)
#         data = PollsSerializer(poll).data
#         return Response(data)

#USING GENERICS

class PollList(generics.ListCreateAPIView):
    queryset = Polls.objects.all()  #queryset is overridden
    serializer_class = PollsSerializer #serializer_class is overridden

class PollDetails(generics.RetrieveDestroyAPIView):
    queryset = Polls.objects.all()
    serializer_class = PollsSerializer

# class ChoiceList(generics.ListCreateAPIView):
#     queryset = Choice.objects.all()
#     serializer_class = ChoiceSerializer
#
# class VoteList(generics.CreateAPIView):
#     queryset = Vote.objects.all()
#     serializer_class = VoteSerializer

# Better url structure
# • /polls/ and /polls/<pk>
# • /polls/<pk>/choices/ to GET the choices for a specific poll, and to create choices for a specific poll.
# (Idenitfied by the <pk>)
# • /polls/<pk>/choice

class ChoiceList(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset= Choice.objects.filter(poll_id=self.kwargs["pk"])
        return queryset
    serializer_class = ChoiceSerializer

class VoteList(generics.CreateAPIView):
    def post(self,request,pk,choice_pk):
        voted_by = request.data.get("voted_by")
        data = {'choice': choice_pk, 'poll': pk, 'voted_by': voted_by}
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            vote = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer_class = VoteSerializer


class PollViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Polls.objects.all()
    serializer_class = PollsSerializer

class UserCreate(generics.CreateAPIView):
    authentication_classes = ()#to exempt from auth
    permission_classes = ()#to exempt from auth
    serializer_class = UserSerializer

class LoginView(APIView):
    permission_classes = ()

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token":user.auth_token.key})
        else:
            return Response({"error":"Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)



