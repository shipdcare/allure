from peewee import *
import json

# import urlparse

# urlparse.uses_netloc.append('postgres')
# url = urlparse.urlparse(os.environ["DATABASE_URL"])
# DATABASE = PostgresqlDatabase(database=url.path[1:], user=url.username, password=url.password, host=url.hostname,
#                         port=url.port)

DATABASE = PostgresqlDatabase('allure', user='postgres', host="localhost", port="5432")

## DATABASE = SqliteDatabase("Allure.db")

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


class Trades(Model):
    order_id =  CharField()
    exchange_order_id = CharField()
    placed_by = CharField()
    status = CharField()
    status_message = CharField()
    tradingsymbol = CharField()
    exchange = CharField()
    order_type = CharField()
    transaction_type = CharField()
    validity= CharField()
    product = CharField()
    average_price = CharField()
    price = CharField()
    quantity = CharField()
    filled_quantity = CharField()
    unfilled_quantity = CharField()
    trigger_price = CharField()
    status_message = CharField()
    user_id = CharField()
    order_timestamp = CharField()
    exchange_timestamp= CharField()
    checksum = CharField()