from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count


# Create your models here.


class Questions(models.Model):
    description=models.CharField(max_length=300)
    image=models.ImageField(upload_to="images",null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.description

    @property
    def question_answers(self):
        return Answers.objects.filter(question=self).annotate(ucount=Count('upvote')).order_by('-ucount')


class Answers(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    question=models.ForeignKey(Questions,on_delete=models.CASCADE)
    answer=models.CharField(max_length=300)
    created_date=models.DateTimeField(auto_now_add=True)
    upvote=models.ManyToManyField(User,related_name="answer")

    @property
    def upvote_count(self):
        return self.upvote.all().count()

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    profile_pic=models.ImageField(upload_to="profiles",null=True)
    bio=models.CharField(max_length=200)