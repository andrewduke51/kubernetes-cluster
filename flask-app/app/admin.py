from flask import Blueprint, render_template, request, g
from datetime import datetime
import pymongo

# Create a Blueprint for the admin route
admin_bp = Blueprint("admin_bp", __name__)

# Define the IP collection variable here
mongoconnection = pymongo.MongoClient("mongodb://mongo-service.mongo:27017/")
visitorsdb = mongoconnection["ips"]
attackcollection = visitorsdb["attacks"]

# Create a counter to track login attempts
login_attempts = {}

@admin_bp.route('/admin', methods=["GET", "POST"])
@admin_bp.route('/config', methods=["GET", "POST"])
def honeypot():
    remote_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)

    # Increment the login attempt count for this IP
    if remote_address not in login_attempts:
        login_attempts[remote_address] = 0
    login_attempts[remote_address] += 1

    # Check if the login attempts exceed the limit (3 attempts)
    if login_attempts[remote_address] >= 3:
        return "Oops! You stumbled into our honeypot. No secrets for you! 😄"

    if request.method == "POST":
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

    return render_template('admin.html')
