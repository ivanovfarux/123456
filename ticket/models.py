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
    documents = models.FileField(upload_to='ticket/images')
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
    status = models.BooleanField(default=False)
    createDate = models.DateTimeField(auto_now_add=True)
    file = models.ImageField(upload_to='ticket/images')
    endDate = models.DateTimeField()
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    compleks = models.ForeignKey(Compleks, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,   related_name='user')
    partnyor = models.ForeignKey(Partnyor,  on_delete=models.CASCADE)
    company = models.ForeignKey(Company,  on_delete=models.CASCADE)
    updatedDate = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-createDate"]

    def __str__(self):
        return self.name

class Education(models.Model):
    name = models.CharField(max_length=200)
    info = models.CharField(max_length=220)
    date = models.DateTimeField()
    createDate = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='ticket/images')
    read = models.CharField(max_length=200)
    toDate = models.DateTimeField(auto_now=True)
    endDate = models.DateTimeField()

    class Meta:
        ordering = ["-createDate"]

    def __str__(self):
        return self.name

class Duty(models.Model):
    kun = models.CharField(max_length=200)
    oy = models.CharField(max_length=200)
    yil = models.CharField(max_length=200)
    createDate = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    duty = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_duty')

    class Meta:
        ordering = ["-createDate"]

    def __str__(self):
        return self.kun

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('duty_edit', kwargs={'pk': self.pk})


class Events(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "tblevents"
