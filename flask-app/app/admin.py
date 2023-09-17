from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
import pymongo
import socket
import json
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Create a Blueprint for the admin route
admin_bp = Blueprint("admin_bp", __name__)

# Define the IP collection variable here
mongoconnection = pymongo.MongoClient("mongodb://mongo-service.mongo:27017/")
visitorsdb = mongoconnection["ips"]
ipcollection = visitorsdb["visitors"]

# Create a limiter instance with a rate limit of 3 attempts per minute for login
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="memory://",  # You can choose a different storage option
    default_limits=["3 per minute"]
)

# Counter to track login attempts
login_attempts = {}


@admin_bp.route('/admin', methods=["GET", "POST"])
@admin_bp.route('/config', methods=["GET", "POST"])
@limiter.request_filter
def honeypot():
    # Check if the subpath matches "/admin"
    if request.method == "POST":
        # Check login credentials here (you can implement your logic)
        username = request.form.get("username")
        password = request.form.get("password")

        # Replace this with your actual login validation logic
        valid_credentials = validate_login(username, password)

        if valid_credentials:
            return render_template('admin.html')
        else:
            # Increment the login attempt count for this IP
            remote_address = get_remote_address()
            login_attempts[remote_address] = login_attempts.get(remote_address, 0) + 1

            # Check if the login attempts exceed the limit (3 attempts)
            if login_attempts[remote_address] >= 3:
                return "Oops! You stumbled into our honeypot. No secrets for you! 😄"

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
