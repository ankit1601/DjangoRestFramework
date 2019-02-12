from django.shortcuts import render,get_object_or_404
from .models import Polls
from django.http import JsonResponse

# Create your views here.
def polls_list(request):
    MAX_OBJECTS =  20
    polls  = Polls.objects.all()[:MAX_OBJECTS]
    data = {"result":list(polls.values("question","created_by__username","pub_date"))}
    return JsonResponse(data)

def polls_details(request,pk):
    poll = get_object_or_404(Polls,pk=pk)
    data = {"result":{
        "question":poll.question,
        "created_by":poll.created_by.username,
        "pub_date":poll.pub_date
    }}
    return JsonResponse(data)