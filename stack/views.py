from django.shortcuts import render,redirect
from stack.forms import RegistrationForm,LoginForm,QuestionForm
from django.views.generic import View, CreateView, FormView,TemplateView,ListView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from stack.models import Questions,Answers

# Create your views here.

class SignUpView(CreateView):
    model=User
    form_class=RegistrationForm
    template_name="register.html"
    success_url=reverse_lazy("signin")
   
   
    # def get(self,request,*args,**kwargs):
    #     form=RegistrationForm()
    #     return render(request,"register.html",{"form":form})
    # def post(self,request,*args,**kwargs):
    #     form=RegistrationForm(request.POST)

    #     if form.is_valid():
    #         form.save()
    #         return redirect("register")
    #     else:
    #         return render(request,"register.html",{"form":form})


class SignInView(FormView):
    template_name="login.html"
    form_class=LoginForm

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("index")
            else:
                return render(request,"login.html",{"form":self.form_class})


class IndexView(CreateView,ListView):
    model=Questions
    form_class=QuestionForm
    template_name="home.html"
    success_url=reverse_lazy("index")
    context_object_name="questions"

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)

# localhost:8000/questions/2/answers/add

class AddAnswerView(View):
     def post(self,request,*args,**kwargs):
        qid=kwargs.get("id")
        ques=Questions.objects.get(id=qid)
        ans=request.POST.get("answer")
        usr=request.user
        Answers.objects.create(user=usr,question=ques,answer=ans)
        return redirect("index")


class UpVoteView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get("id")
        ans=Answers.objects.get(id=id)
        ans.upvote.add(request.user)
        ans.save()
        return redirect("index")
