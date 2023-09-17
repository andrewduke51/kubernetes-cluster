from flask import Flask, render_template, request, Blueprint
from datetime import datetime
import pymongo
import socket
import json
import os

# Create a Blueprint for the admin routes
admin_bp = Blueprint("admin_bp", __name__)

# Define the attackcollection variable here
mongoconnection = pymongo.MongoClient("mongodb://mongo-service.mongo:27017/")
visitorsdb = mongoconnection["ips"]
ipcollection = visitorsdb["visitors"]
attackcollection = visitorsdb["attacks"]

# ... (Other imports and variables)

# Routes for /admin and /config
@admin_bp.route('/admin', methods=["GET", "POST"])
@admin_bp.route('/config', methods=["GET", "POST"])
def honeypot():
    # Log and save attack details to the "attacks" collection
    captured = {
        "time_stamp": datetime.now().strftime("%m/%d/%y - %H:%M:%S"),
        "ip_addresses": request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr),
        "request_data": {
            "path": request.path,
            "method": request.method,
            "user_agent": request.user_agent.string,
            "data": request.get_data(as_text=True),
        }
    }
    attackcollection.insert_one(captured)  # Use a separate collection for attacks
    return render_template('admin.html')
