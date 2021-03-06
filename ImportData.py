from __future__ import division
import csv
import datetime
from math import ceil

from peewee import MySQLDatabase

from Models import PatientMeasurement, Feature
import settings


TRAINING_DATA_FILE_NAME = "all_forms_PROACT.txt"
#TRAINING_DATA_FILE_NAME = "all_forms_validate_spike.txt"
#TRAINING_DATA_FILE_NAME = "test_data.txt"
SUBJECT_ID = 0
FORM_NAME = 1
FEATURE_NAME = 2
FEATURE_VALUE = 3
FEATURE_UNIT = 4
FEATURE_DELTA = 5
DROP_EXISTING_TABLES = False
CREATE_TABLES = True
BATCH_SIZE = 1000
seen_features = set()


def validate_feature_value(value):
    """Some missing values are stored as NA, we can't insert NA into numeric
    field so set it to None which ends up being converted to null
    Other fields have a semicolon seperated list of numbers some of which are
    NA
    """
    if value == "NA":
        return None
    if ";" in value:
        #print "Value contained a ; seperated list, decide what to do with " \
        #    "these"
        return None
    return value


def drop_tables():
    """Drops the tables so you can start again fresh"""
    try:
        PatientMeasurement.drop_table()
        Feature.drop_table()
    except Exception as e:
        print "Failed to drop tables", e
        raise


def create_database_connection():
    """Creates a connection to a MySQLDatabase using the parmeters specified
    in the setting file"""
    try:
        db = MySQLDatabase(
            settings.DATABASE,
            user=settings.USERNAME,
            passwd=settings.PASSWORD,
            host=settings.HOST
        )
        db.connect()
    except Exception as e:
        print "Failed to connect to database", e
    return db


def create_tables():
    """Creates the required tables assuming they dont exist and a database
    connection db exists as a global object"""
    try:
        db.create_tables([PatientMeasurement, Feature], safe=True)
    except Exception as e:
        print "Failed to create tables", e
        raise


def insert_feature_if_not_present(row):
    if not row[FEATURE_NAME].lower() in seen_features:
        Feature(
            feature_name=row[FEATURE_NAME].lower(),
            form_name=row[FORM_NAME].lower()
        ).save()
        seen_features.add(row[FEATURE_NAME].lower())


def yield_x_rows(rows, start_index, x):
    """Yields x rows beginning at start_index from rows"""
    for i in xrange(x):
        try:
            row = rows[start_index + i]
        except IndexError:
            # Batch size is larger than whats left we're done
            break
        insert_feature_if_not_present(row)
        res = {
            "subject_id": row[SUBJECT_ID],
            "feature_name": row[FEATURE_NAME].lower(),
            "delta": validate_feature_value(row[FEATURE_DELTA]),
            "value": validate_feature_value(row[FEATURE_VALUE])
        }
        yield res


print "Creating database connection"
db = create_database_connection()
if DROP_EXISTING_TABLES:
    drop_tables()
if CREATE_TABLES:
    create_tables()


with open(TRAINING_DATA_FILE_NAME, "rb") as csvfile:
    reader = csv.reader(csvfile, delimiter="|")
    next(reader, None)
    row_list = list(reader)
    number_of_rows = len(row_list)
    start_index = 0
    print "Inserting %s rows" % number_of_rows
    # xrange does not include the final number but its fine because we index
    # from 0
    start_time = datetime.datetime.now()
    upper_limit = int(ceil(number_of_rows / BATCH_SIZE))
    for _ in xrange(upper_limit):
        batch_start_time = datetime.datetime.now()
        PatientMeasurement.insert_many(
            yield_x_rows(row_list, start_index, BATCH_SIZE)
        ).execute()
        batch_end_time = datetime.datetime.now()
        batch_time_taken = \
            (batch_end_time - batch_start_time).total_seconds()
        print "Inserted %s rows in %s seconds" % (BATCH_SIZE, batch_time_taken)
        start_index += BATCH_SIZE
        rows_remaining = number_of_rows - start_index
        estimated_time_remaining = \
            (rows_remaining / BATCH_SIZE) * batch_time_taken
        print "%d rows remaining, estimated time %d" % (
            rows_remaining, estimated_time_remaining
        )
    end_time = datetime.datetime.now()
    time_taken = \
        (end_time - start_time).total_seconds()
    print "Inserted %s rows in %s seconds" % (number_of_rows, time_taken)
