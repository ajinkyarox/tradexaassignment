from django.db import models

# Create your models here.

class LoginCredentials(models.Model):
    id=models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=256)
    lastname = models.CharField(max_length=256)
    username = models.CharField(max_length=256)
    password = models.CharField(max_length=256)

    class Meta:
        db_table = "LoginCredentials"

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    lid=models.OneToOneField(LoginCredentials, on_delete=models.CASCADE)
    message= models.CharField(max_length=256)
    created_at=models.DateTimeField()
    updated_at = models.DateTimeField()
    class Meta:
        db_table="Message"
