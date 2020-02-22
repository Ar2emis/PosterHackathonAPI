from django.db import models


class Role(models.Model):
    uid = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class User(models.Model):
    uid = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=40)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.role} {self.name}'


class WatchType(models.Model):
    uid = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Progress(models.Model):
    uid = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=50)
    text = models.TextField()
    worker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    progress = models.ForeignKey(Progress, on_delete=models.SET_NULL, null=True, blank=True)
    work_type = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Watch(models.Model):
    date = models.DateField(primary_key=True)
    watch_type = models.ForeignKey(WatchType, on_delete=models.SET_NULL, null=True)
    tasks = models.ManyToManyField(Task, related_name='watch_tasks')

    def __str__(self):
        return f'{self.date} {self.watch_type.name}'