from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Problem(models.Model):
    name = models.CharField(max_length=200)
    status = models.BooleanField(default=False)
    createDate = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('problem_edit', kwargs={'pk': self.pk})


class Company(models.Model):
    name = models.CharField(max_length=200)
    createDate = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


class Compleks(models.Model):
    name = models.CharField(max_length=200)
    createDate = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    schema_net = models.ImageField(upload_to='ticket/images')
    documents = models.ImageField(upload_to='ticket/images')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


class Partnyor(models.Model):
    fio = models.CharField(max_length=200)
    login = models.CharField(max_length=12)
    password = models.CharField(max_length=10)
    createDate = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ticket/images', blank=True)
    contacts = models.CharField(max_length=10)
    status = models.BooleanField(default=False)
    companyId = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company')
    age = models.IntegerField()

    def __str__(self):
        return self.fio

    def __str__(self):
        return self.login

    def __str__(self):
        return self.companyId


class Ticket(models.Model):
    name = models.CharField(max_length=250)
    note = models.CharField(max_length=250)
    compleks = models.ForeignKey(Compleks, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, null=True, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    partnyor = models.ForeignKey(Partnyor, null=True, on_delete=models.CASCADE)
    createDate = models.DateTimeField(auto_now_add=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    updatedDate = models.DateTimeField(auto_now=True)
    file = models.ImageField(upload_to='ticket/images', null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,   related_name='user1')
    color = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=False)

    class Meta:
        ordering = ["-createDate"]

    def __str__(self):
        return self.name


class Education(models.Model):
    name = models.CharField(max_length=200)
    info = models.CharField(max_length=220)
    date = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True)
    createDate = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='ticket/images')
    read = models.CharField(max_length=200)
    toDate = models.DateTimeField(auto_now=True)
    endDate = models.DateTimeField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_teacher')

    class Meta:
        ordering = ["-createDate"]

    def __str__(self):
        return self.name

class Duty(models.Model):
    status = models.BooleanField(default=False)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE) # default  authentifacet user
    duty = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_duty')
    createDate = models.DateTimeField(auto_now_add=True)  # default sysdate
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    color = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        ordering = ["-createDate"]

    def __str__(self):
        return self.kun

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('duty_edit', kwargs={'pk': self.pk})


class ToDo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    note = models.CharField(max_length=250, null=True, blank=True)
    compleks = models.ForeignKey(Compleks, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userTodo')
    updatedDate = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authorTodo')
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    color = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=False)
    file = models.FileField(upload_to='ticket/images')

    class Meta:
        ordering = ["-start"]

    def __str__(self):
        return self.name

    def __str__(self):
        return str(self.id)

class Events(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "tblevents"
