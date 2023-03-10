from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
  name = models.CharField(max_length=100)
  memo = models.TextField(blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  completed_at = models.DateTimeField(null=True, blank=True)
  is_important = models.BooleanField(default=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.name
