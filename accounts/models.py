from django.db import models
from core.models import Recipe

# Create your models here.

from django.contrib.auth.models import AbstractUser
from core.models import Ingredient

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.URLField(blank=True, null=True)
    cabinet = models.ManyToManyField(Ingredient)
    wishlist = models.ManyToManyField(Recipe)

    def ingredient_set_with_aliases(self):
        search_space = []
        for i in self.cabinet.all():
            search_space.append(i.name)
            for alias in i.aliases.all():
                search_space.append(alias.alias_name)
        return search_space
