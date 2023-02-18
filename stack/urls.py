from django.urls import path
from stack import views

urlpatterns=[
    path("register/",views.SignUpView.as_view(),name="register"),
    path("login",views.SignInView.as_view(),name="signin"),
    path("home",views.IndexView.as_view(),name="index"),
    path("questions/<int:id>/answers/add",views.AddAnswerView.as_view(),name="add-answer"),
    
]