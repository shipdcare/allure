from peewee import *
import json
import psycopg2
import os
import urlparse
from peewee import PostgresqlDatabase

if 'HEROKU' in os.environ:
    urlparse.uses_netloc.append('postgres')
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    DATABASE = PostgresqlDatabase(database=url.path[1:], user=url.username, password=url.password, host=url.hostname,
                            port=url.port)
else:
    DATABASE = PostgresqlDatabase(
        'allure',
        host= 'localhost',
        port= 5432,
        user= 'mohakmac'
    )

class MyModel(Model):

  def __str__(self):
    r = {}
    for k in self._data.keys():
      try:
         r[k] = str(getattr(self, k))
      except:
         r[k] = json.dumps(getattr(self, k))
    return str(r)

class Instrument(MyModel):
    instrument_token = CharField()
    exchange_token = CharField()
    tradingsymbol = CharField()
    name = CharField()
    last_price = FloatField()
    expiry = CharField()
    strike = FloatField()
    tick_size = FloatField()
    lot_size = IntegerField()
    instrument_type = CharField()
    segment = CharField()
    exchange = CharField()

    class Meta:
        database = DATABASE

class SavedInstruments(Model):
    instrument_token = CharField()
    tradingsymbol = CharField()
    exchange = CharField()
    name = CharField()

    class Meta:
        database = DATABASE




