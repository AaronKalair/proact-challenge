import csv
import peewee
from peewee import *
from Models import PatientMeasurements, Features
from functools import partial

TRAINING_DATA_FILE_NAME = "all_forms_PROACT.txt"
SUBJECT_ID = 0
FORM_NAME = 1
FEATURE_NAME = 2
FEATURE_VALUE = 3
FEATURE_UNIT = 4
FEATURE_DELTA = 5
HOST = "localhost"
USERNAME = "root"
PASSWORD = ""
DATABASE = "als"
DONT_RECREATE_TABLES = False

db = MySQLDatabase(DATABASE, user=USERNAME, passwd=PASSWORD)
db.connect()
PatientMeasurements.drop_table()
Features.drop_table()
db.create_tables([PatientMeasurements, Features], safe=DONT_RECREATE_TABLES)

with open(TRAINING_DATA_FILE_NAME, "rb") as csvfile:
    reader = csv.reader(csvfile, delimiter="|")
    next(reader, None)
    for count, row in enumerate(reader):
        print count
        insert_fn = partial(
            PatientMeasurements,
            subject_id=row[SUBJECT_ID],
            feature_name=row[FEATURE_NAME],
        )
        try:
            insert_fn(
                delta=row[FEATURE_DELTA],
                value=row[FEATURE_VALUE]
            ).save()
        except ValueError:
            print row[SUBJECT_ID]
            print row[FEATURE_NAME]
            print row[FEATURE_DELTA]
            print row[FEATURE_VALUE]
            insert_fn(
                delta=None,
                value=None
            ).save()
        try:
            Features.get(feature_name=row[FEATURE_NAME])
        except Features.DoesNotExist:
            Features(
                feature_name=row[FEATURE_NAME],
                form_name=row[FORM_NAME]
            ).save()
