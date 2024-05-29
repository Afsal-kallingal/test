from django.db import models
from apps.user_account.models import User
# from apps.course import models as course_models
from apps.main.models import BaseModel


class Project(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="+")    
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tudo(BaseModel):
    project = models.ForeignKey(Project, related_name='todos', on_delete=models.CASCADE)
    description = models.CharField(max_length=200,null=True,blank=True)

    status = models.BooleanField(default=False)

    def __str__(self):
        return self.description
