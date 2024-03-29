from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
import pymongo

# Create a Blueprint for the admin route
admin_bp = Blueprint("admin_bp", __name__)

# Define the IP collection variable here
mongoconnection = pymongo.MongoClient("mongodb://mongo-service.mongo:27017/")
visitorsdb = mongoconnection["ips"]
attackcollection = visitorsdb["attacks"]

# Dictionary to keep track of IP addresses and their login attempts
ip_login_attempts = {}

# Maximum number of allowed login attempts before humorous response
max_login_attempts = 4

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

    # Check if there are more than three entries with the same IP on the same date
    today_date = datetime.now().strftime("%m/%d/%y")
    same_date_ip_count = attackcollection.count_documents({
        "time_stamp": {"$regex": f"{today_date}.*"},
        "ip_addresses": ip_address
    })

    # If the count exceeds the threshold, respond with a humorous message
    if same_date_ip_count >= 4:
        return render_template('nel_son_return.html', ip_address=ip_address)

    # Render the admin.html template
    if same_date_ip_count >= 2:
        same_date_ip_count -= 1
        return render_template('admin.html', login_attempt=same_date_ip_count)
    return render_template('admin.html')
