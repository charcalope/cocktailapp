from django.db import models
from accounts.models import User

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    written_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    photo = models.URLField()

    def __str__(self):
        return self.title

    def preview(self):
        if len(self.content) > 150:
            return self.content[:150]
        else:
            return self.content
