from flask import Blueprint, render_template, request
from datetime import datetime
import pymongo
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Create a Blueprint for the admin route
admin_bp = Blueprint("admin_bp", __name__)

# MongoDB connection
mongoconnection = pymongo.MongoClient("mongodb://mongo-service.mongo:27017/")
visitorsdb = mongoconnection["ips"]
attackcollection = visitorsdb["attacks"]

# Counter to track login attempts
login_attempts = {}

@admin_bp.route('/admin', methods=["GET", "POST"])
@admin_bp.route('/config', methods=["GET", "POST"])
@limiter.request_filter
def honeypot():
    if request.method == "POST":
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
