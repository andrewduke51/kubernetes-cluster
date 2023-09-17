from flask import Blueprint, render_template, request
from datetime import datetime
import pymongo
import socket
import json
import os

# Create a Blueprint for the admin route
admin_bp = Blueprint("admin_bp", __name__)

# Define the IP collection variable here
mongoconnection = pymongo.MongoClient("mongodb://mongo-service.mongo:27017/")
visitorsdb = mongoconnection["ips"]
attackcollection = visitorsdb["attacks"]

# Initialize the login attempt counter
login_attempts = {}

# Create a counter to track login attempts
from multiprocessing import Value

counter = Value('i', 0)

@admin_bp.route('/admin', methods=["GET", "POST"])
@admin_bp.route('/config', methods=["GET", "POST"])
def honeypot():
    if request.method == "POST":
        # Get the IP address of the requester
        remote_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)

        # Check if the IP address has reached the login attempts threshold (3 attempts)
        if login_attempts.get(remote_address, 0) >= 3:
            return "Oops! You stumbled into our honeypot. No secrets for you! 😄"

        # Increment the login attempt count for this IP
        login_attempts[remote_address] = login_attempts.get(remote_address, 0) + 1

        # Log and save attack details to the "attacks" collection
        captured = {
            "time_stamp": datetime.now().strftime("%m/%d/%y - %H:%M:%S"),
            "ip_addresses": remote_address,
            "request_data": {
                "path": request.path,
                "method": request.method,
                "user_agent": request.user_agent.string,
                "data": request.get_data(as_text=True),
            }
        }
        attackcollection.insert_one(captured)  # Use a separate collection for attacks

    # Render the admin.html template
    return render_template('admin.html')
