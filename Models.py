import peewee
from peewee import *


class PatientMeasurements(peewee.Model):
    subject_id = peewee.IntegerField()
    feature_name = peewee.TextField()
    value = peewee.TextField(null=True)
    delta = peewee.IntegerField(null=True)


class Features(peewee.Model):
    feature_name = peewee.TextField()
    form_name = peewee.TextField()
