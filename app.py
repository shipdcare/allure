import json, os
from flask import Flask, request, redirect, url_for, make_response, render_template, g
from kiteconnect import KiteConnect

import models

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['port'] = 6999
##api_key = "2kagnzo0t3tk8i0l"
##api_secret = "eh5pyqmao4dr366zxjy34cs8q4klbxuy"

api_key = "9culfaktxf3ywh4s"
api_secret = "6ulgdvbqrj1hqx0k211yu64iituj62eq"
kite = KiteConnect(api_key=api_key)



@app.before_request
def before_request():
    """Connect to the database before each request"""
    g.db = models.DATABASE
    g.db.get_conn()
    g.db.create_tables([models.Instrument, models.SavedInstruments], safe=True)


@app.after_request
def after_request(response):
    """"Close the database connection after each request"""
    g.db.close()
    return response


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.route("/")
def index():
    return redirect("https://kite.trade/connect/login?api_key=" + api_key)


@app.route("/home")
def home():
    return render_template("home.html")


@app.route('/get_quote')
def get_quote():
    access_token = request.cookies.get('access_token')
    kite.set_access_token(access_token)
    tradingsymbol = request.args.get('tradingsymbol')
    quote = kite.quote(exchange="NSE", tradingsymbol="INFY")
    return json.dumps(quote)


@app.route('/save_instrument', methods=['POST'])
def save_instrument():
    content = request.get_json()
    instrument = models.SavedInstruments.get_or_create(instrument_token=content["token"],
                                                       tradingsymbol=content["tradingsymbol"],
                                                       name=content["name"],
                                                       exchange=content["exchange"])
    return 'done'


@app.route('/saved_instruments')
def saved_instruments():
    elems = []
    data = models.SavedInstruments.select()
    for d in data:
        elems.append({"instrument_token": d.instrument_token,
                      "tradingsymbol": d.tradingsymbol,
                      "name": d.name,
                      "exchange": d.exchange })
    return json.dumps(elems)



@app.route("/data_dump")
def data_dump():
    access_token = request.cookies.get('access_token')
    # res = requests.get("https://api.kite.trade/user/margins/equity?api_key=2kagnzo0t3tk8i0l&access_token=" + access_token)
    kite.set_access_token(access_token)
    models.Instrument.delete().where(models.Instrument.instrument_token != "").execute()
    db = models.DATABASE
    db.get_conn()
    with db.atomic():
        for instruments in kite.instruments(exchange="NSE"):
            models.Instrument.create(**instruments)
    return "DONE"


@app.route("/instruments")
def instruments():
    elems = []
    data = models.Instrument.select().where(models.Instrument.exchange << ["NSE"])
    for d in data:
        elems.append(
            {"value": d.tradingsymbol, "tradingsymbol": d.tradingsymbol, "token": d.instrument_token, "name": d.name,
             "exchange": d.exchange})
    return json.dumps(elems)


@app.route("/connect")
def connect():
    request_token = request.args.get('request_token')
    data = kite.request_access_token(request_token, secret=api_secret)
    response = make_response(redirect(url_for("home")))
    response.set_cookie('access_token', data["access_token"])
    response.set_cookie('public_token', data["public_token"])
    response.set_cookie('user_id', data["user_id"])
    return response


@app.route('/settings')
def settings():
    return render_template('settings.html')


@app.route('/set_settings', methods=['POST'])
def set_settings():
    response = make_response(redirect(url_for("home")))
    response.set_cookie('squareoff_value', request.form['squareoff_value'])
    response.set_cookie('stoploss_value', request.form["stoploss_value"])
    response.set_cookie('trigger_percent', request.form["trigger_percent"])
    return response


@app.route('/order', methods=['POST'])
def order():
    access_token = request.cookies.get('access_token')
    kite.set_access_token(access_token)
    response = make_response(redirect(url_for("home")))
    try:
        if request.form["orderRadios"] == "MARKET":
            order_id = kite.order_place(tradingsymbol=request.form["tradingSymbol"],
                                        exchange=request.form["tradingExchange"],
                                        transaction_type=request.form["action"],
                                        quantity=request.form.get("quantity", 0),
                                        order_type="MARKET",
                                        product="MIS",
                                        disclosed_quantity=request.form.get("disclosed_quantity", 0))
            print("Order placed. ID is", order_id)
        elif request.form["orderRadios"] == "LIMIT":
            order_id = kite.order_place(tradingsymbol=request.form["tradingSymbol"],
                                        exchange=request.form["tradingExchange"],
                                        transaction_type=request.form["action"],
                                        quantity=request.form.get("quantity", 0),
                                        order_type="LIMIT",
                                        product="MIS",
                                        price=request.form.get("price", 0),
                                        disclosed_quantity=request.form.get("disclosed_quantity", 0))
            print("Order placed. ID is", order_id)
        elif request.form["orderRadios"] == "SL":
            order_id = kite.order_place(tradingsymbol=request.form["tradingSymbol"],
                                        exchange=request.form["tradingExchange"],
                                        transaction_type=request.form["action"],
                                        quantity=request.form.get("quantity", 1),
                                        order_type="SL",
                                        product="MIS",
                                        price=request.form.get("price", 0),
                                        disclosed_quantity=request.form.get("disclosed_quantity", 0),
                                        trigger_price=request.form.get("trigger_price", 0))
            print(order_id)
        elif request.form["orderRadios"] == "SL-M":
            order_id = kite.order_place(tradingsymbol=request.form["tradingSymbol"],
                                        exchange=request.form["tradingExchange"],
                                        transaction_type=request.form["action"],
                                        quantity=request.form.get("quantity", 1),
                                        order_type="SL-M",
                                        product="MIS",
                                        disclosed_quantity=request.form.get("disclosed_quantity", 0),
                                        trigger_price=request.form.get("trigger_price", 0))
            print(order_id)
        elif request.form["orderRadios"] == "BO":
            order_id = kite.order_place(tradingsymbol=request.form["tradingSymbol"],
                                        variety="bo",
                                        exchange=request.form["tradingExchange"],
                                        transaction_type=request.form["action"],
                                        quantity=request.form.get("quantity", 0),
                                        order_type="LIMIT",
                                        product="MIS",
                                        price=request.form.get("price", 0),
                                        trailing_stoploss=request.form.get('trailing_stoploss', None),
                                        stoploss_value=request.form['stoploss_value'],
                                        squareoff_value=request.form['squareoff_value'],
                                        validity="DAY")
            print("Order placed. ID is", order_id)
        elif request.form["orderRadios"] == "CO":
            order_id = kite.order_place(tradingsymbol=request.form["tradingSymbol"],
                                        exchange=request.form["tradingExchange"],
                                        variety="co",
                                        transaction_type=request.form["action"],
                                        quantity=request.form.get("quantity", 0),
                                        order_type="MARKET",
                                        product="MIS",
                                        trigger_price=request.form["trigger_price"],
                                        disclosed_quantity=request.form.get("disclosed_quantity", 0))
            print("Order placed. ID is", order_id)
        else:
            print("UNKNOWN ORDER TRIGGERED")
    except Exception as e:
        print(str(e))
        raise
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0')
