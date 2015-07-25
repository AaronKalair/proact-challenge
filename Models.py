from peewee import Model, IntegerField, MySQLDatabase, CharField
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
    feature_name = CharField(index=True)
    value = CharField(null=True)
    delta = IntegerField(index=True, null=True)


class Feature(BaseModel):
    feature_name = CharField(unique=True)
    form_name = CharField()
