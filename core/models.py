from typing import ForwardRef
from django.db import models
from django.db.models.base import Model

# Create your models here.


class JobCatag(models.Model):
    catag = models.CharField(max_length=64)


class JobName(models.Model):
    name = models.CharField(max_length=128)
    catag = models.ForeignKey(JobCatag, on_delete=models.CASCADE)


class CompanyDetails(models.Model):
    name = models.CharField(max_length=64)
    desc = models.CharField(max_length=2048)
    location = models.CharField(max_length=128)


class JobDetails(models.Model):
    company = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE)
    position = models.CharField(max_length=256)
    location = models.CharField(max_length=128)
