from flask import Flask, render_template, jsonify, request
from multiprocessing import Value
from datetime import datetime
import pymongo
import socket
import json
import os


# Variables ##
app = Flask(__name__, template_folder='views')
counter = Value('i', 0)
mongoconnection = pymongo.MongoClient("mongodb://mongo-service.mongo:27017/")
visitorsdb = mongoconnection["ips"]
ipcollection = visitorsdb["visitors"]

@app.route('/', methods=["GET"])
def index():
    captured = {
        "time_stamp" : datetime.now().strftime("%m/%d/%y - %H:%M:%S"),
        "ip_addresses" : request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    }
    ipcollection.insert_one(captured)
    return render_template('index.html')


@app.route("/clicknext")
def home():
    captured = {
        "time_stamp" : datetime.now(),
        "ip_addresses" : request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    }
    ipcollection.insert_one(captured)
    with counter.get_lock():
        counter.value += 1
    data = counter.value
    ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    return render_template('home.html',
                           title="page",
                           json_value=json.dumps(data),
                           ip_addr=ip_addr,
                           hostname=socket.gethostname()
                           )


@app.route('/proxy_client')
def proxy_client():
    return render_template('proxy_client.html')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
