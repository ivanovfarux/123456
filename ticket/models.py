from django.contrib.auth.models import User
from django.db import models


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Problem.Status.Published)


class Problem(models.Model):
    class Status(models.TextChoices):
        Activ = "1", "Activ"
        Noactiv = "0", "Noactiv"
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.Activ
                              )
    creatorId = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Compleks(models.Model):
    class Status(models.TextChoices):
        Activ = "1", "Activ"
        Noactiv = "0", "Noactiv"
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.Activ
                              )
    schema_net = models.ImageField(upload_to='ticket/images')
    documents = models.FileField(upload_to='ticket/images')
    creatorId = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


class Company(models.Model):
    class Status(models.TextChoices):
        Activ = "1", "Activ"
        Noactiv = "0", "Noactiv"

    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.Activ)
    creatorId = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name

class Partnyor(models.Model):
    class Status(models.TextChoices):
        Activ = "1", "Activ"
        Noactiv = "0", "Noactiv"

    fio = models.CharField(max_length=200)
    login = models.CharField(max_length=12)
    password = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.Activ)
    creatorId = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ticket/images')
    contacts = models.CharField(max_length=10)
    companyId = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.fio

class Tickets(models.Model):
    class Status(models.TextChoices):
        Activ = "1", "Activ"
        Noactiv = "0", "Noactiv"

    name = models.CharField(max_length=250)
    note = models.CharField(max_length=250)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.Activ
                              )
    createDate = models.DateTimeField(auto_now_add=True)
    file = models.ImageField(upload_to='ticket/images')
    endDate = models.DateTimeField()
    problem = models.ForeignKey(Problem,
                                on_delete=models.CASCADE)
    compleks = models.ForeignKey(Compleks,
                                 on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='comments')
    partnyor = models.ForeignKey(Partnyor,
                                 on_delete=models.CASCADE)
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE)
    update_Time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-createDate"]

    def __str__(self):
        return self.name

class Education(models.Model):
    class Status(models.TextChoices):
        Activ = "1", "Activ"
        Noactiv = "0", "Noactiv"

    name = models.CharField(max_length=200)
    info = models.CharField(max_length=220)
    date = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.Activ)
    creatorId = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='ticket/images')
    read = models.CharField(max_length=200)
    toDate = models.DateTimeField(auto_now=True)
    endDate = models.DateTimeField()

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.name

class Navbatchilik(models.Model):
    class Status(models.TextChoices):
        Activ = "1", "Activ"
        Noactiv = "0", "Noactiv"

    kun = models.CharField(max_length=200)
    oy = models.CharField(max_length=200)
    yil = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.Activ)
    creatorId = models.ForeignKey(User, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.RESTRICT)
    ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.kun
