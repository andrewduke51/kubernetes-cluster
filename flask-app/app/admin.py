from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
import pymongo

# Create a Blueprint for the admin route
admin_bp = Blueprint("admin_bp", __name__)

# Define the IP collection variable here
mongoconnection = pymongo.MongoClient("mongodb://mongo-service.mongo:27017/")
visitorsdb = mongoconnection["ips"]
attackcollection = visitorsdb["attacks"]

# Dictionary to keep track of IP addresses and their request counts
ip_request_counts = {}

@admin_bp.route('/admin', methods=["GET", "POST"])
@admin_bp.route('/config', methods=["GET", "POST"])
def honeypot():
    # Get the IP address of the requester
    ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)

    # Log and save attack details to the "attacks" collection
    captured = {
        "time_stamp": datetime.now().strftime("%m/%d/%y - %H:%M:%S"),
        "ip_addresses": ip_address,
        "request_data": {
            "path": request.path,
            "method": request.method,
            "user_agent": request.user_agent.string,
            "data": request.get_data(as_text=True),
        }
    }
    attackcollection.insert_one(captured)  # Use a separate collection for attacks

    # Check if the IP address has made multiple requests
    if ip_address in ip_request_counts:
        ip_request_counts[ip_address] += 1
        if ip_request_counts[ip_address] >= 3:
            # After three requests, respond with a funny message
            funny_response = "Ha-ha! You've stumbled into our honeypot! 😜"
            return jsonify({"message": funny_response}), 200

    # Render the admin.html template
    return render_template('admin.html')
