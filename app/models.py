from django.db import models

class UserDetails(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    pass_word = models.CharField(max_length=200)
    account_type = models.CharField(max_length=50)

    def __str__(self):
        return self.username