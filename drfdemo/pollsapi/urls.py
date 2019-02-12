from django.urls import path
from .apiview import  PollList,PollDetails,ChoiceList,VoteList,PollViewSet,UserCreate,LoginView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

router = DefaultRouter()
router.register("polls",PollViewSet,base_name='polls')

urlpatterns = [
    #Below commented code is for nor django api without using serializers
    # path('polls/',views.polls_list, name="polls_list"),
    # path('polls/<int:pk>/',views.polls_details,name="polls_details")

    # path('polls/', PollList.as_view(), name="polls_list"),
    # path('polls/<int:pk>/',PollDetails.as_view(),name="polls_details"),
    # path('choice/',ChoiceList.as_view(),name="choice_list"),
    # path('vote/',VoteList.as_view(),name="vote_list"),
    path("polls/<int:pk>/choices/", ChoiceList.as_view(), name="choice_list"),
    path("polls/<int:pk>/choices/<int:choice_pk>/vote/", VoteList.as_view(), name="create_vote"),
    path("users/", UserCreate.as_view(), name = "user_create"),
    path("login/", LoginView.as_view(), name="login")

]

urlpatterns += router.urls

# Better url structure
# • /polls/ and /polls/<pk>
# • /polls/<pk>/choices/ to GET the choices for a specific poll, and to create choices for a specific poll.
# (Idenitfied by the <pk>)
# • /polls/<pk>/choice
# path('choice/',ChoiceList.as_view(),name="choice_list"),
# path('vote/',VoteList.as_view(),name="vote_list"),



#The /polls/ and /polls/<pk>/ urls require two view classes, with the same serializer and base queryset. We
# can group them into a viewset, and connect them to the urls using a router.

