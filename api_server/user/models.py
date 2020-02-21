from django.db import models


class TestSubModel(models.Model):
    name = models.TextField()


class TestModel(models.Model):
    name = models.TextField()
    submodel = models.ForeignKey(TestSubModel, on_delete=models.CASCADE, null=True)
    image = models.ImageField(null=True)