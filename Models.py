from peewee import Model, TextField, IntegerField, MySQLDatabase
import settings

database = MySQLDatabase(
    settings.DATABASE,
    user=settings.USERNAME,
    passwd=settings.PASSWORD
)


class BaseModel(Model):
    class Meta:
        database = database


class PatientMeasurement(BaseModel):
    subject_id = IntegerField()
    feature_name = TextField()
    value = TextField(null=True)
    delta = IntegerField(null=True)


class Feature(BaseModel):
    feature_name = TextField()
    form_name = TextField()
