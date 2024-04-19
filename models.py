from peewee import Model, CharField, IntegerField, DateField, SqliteDatabase , CompositeKey

# Define SQLite database
db = SqliteDatabase('data.db')

# Define model for TZDB_TIMEZONES data
class TZDB_TIMEZONES(Model):
    COUNTRY_CODE = CharField(null=False)
    COUNTRY_NAME = CharField(null=False)
    ZONENAME = CharField(primary_key=True, null=False)
    GMTOFFSET = IntegerField(null=True)
    IMPORT_DATE = DateField(null=True)

    class Meta:
        database = db

class TZDB_ERROR_LOG(Model):
    ERROR_DATE = DateField(null=True)
    ERROR_MESSAGE = CharField(null=False)

    class Meta:
        database = db

# Define model for TZDB_ZONE_DETAILS data
class TZDB_ZONE_DETAILS(Model):
    COUNTRY_CODE = CharField(null=False)
    COUNTRY_NAME = CharField(null=False)
    ZONE_NAME = CharField(null=False)
    GMTOFFSET = IntegerField(null=False)
    DST = IntegerField(null=False)
    ZONESTART = IntegerField(null=False)
    ZONEEND = IntegerField(null=False)
    IMPORT_DATE = DateField(null=True)

    class Meta:
        database = db
        primary_key = CompositeKey('ZONE_NAME', 'ZONESTART', 'ZONEEND')

# Initialize database
db.connect()
db.create_tables([TZDB_TIMEZONES,TZDB_ZONE_DETAILS,TZDB_ERROR_LOG])
