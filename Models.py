from peewee import Model, TextField, IntegerField, MySQLDatabase
import settings

database = MySQLDatabase(
    settings.DATABASE,
    user=settings.USERNAME,
    passwd=settings.PASSWORD,
    host=settings.HOST
)


class BaseModel(Model):
    class Meta:
        database = database


class PatientMeasurement(BaseModel):
    subject_id = IntegerField(index=True)
    feature_name = TextField(index=True)
    value = TextField(null=True)
    delta = IntegerField(index=True, null=True)


class Feature(BaseModel):
    feature_name = TextField(index=True)
    form_name = TextField()
