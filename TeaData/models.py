from django.db import models

# Create your models here.
class County(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class City(models.Model):
    County = models.ForeignKey(County, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Person(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=300, blank=True)
    County = models.ForeignKey(County, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    recieve_report = models.BooleanField(default=False)

    def __str__(self):
        return self.name