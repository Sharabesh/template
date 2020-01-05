"""
Model definitions for database calls
"""
from playhouse import signals
from playhouse.postgres_ext import *
from urllib.parse import urlparse
import sys
sys.path.extend("..")
from constants import DATABASE_URL


url = urlparse(DATABASE_URL)

config = dict(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port,
    sslmode='require'
)

conn = PostgresqlExtDatabase(
    autocommit=True,
    autorollback=True,
    register_hstore=False,
    **config
)


class BaseModel(signals.Model):

    class Meta:
        database = conn


class Users(BaseModel): # TODO: Index on uid, email_address, session_id separately
    uid = IntegerField(primary_key=True)
    email_address = CharField()
    username = CharField(null=True)
    password = CharField(null=True)
    date_added = DateTimeField(null=True)
    session_id = CharField(null=True)
    profile_image = CharField(null=True)
    phone = CharField(null=True)


    class Meta:
        db_table = "Test"