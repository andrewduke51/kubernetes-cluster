# clicknext.py

from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
import pymongo
import socket
import json

# Create a Blueprint for the clicknext route
clicknext_bp = Blueprint("clicknext_bp", __name__)

# Define the IP collection variable here
mongoconnection = pymongo.MongoClient("mongodb://mongo-service.mongo:27017/")
visitorsdb = mongoconnection["ips"]
ipcollection = visitorsdb["visitors"]

# /clicknext route
@clicknext_bp.route("/clicknext")
def home():
    captured = {
        "time_stamp": datetime.now(),
        "ip_addresses": request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    }
    ipcollection.insert_one(captured)
    # Retrieve the current visitor count from the database
    total_visitors = ipcollection.count_documents({})
    ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    return render_template('clicknext.html',
                           title="page",
                           json_value=json.dumps(total_visitors),
                           ip_addr=ip_addr,
                           hostname=socket.gethostname()
                           )