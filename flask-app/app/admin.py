from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
import pymongo
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Create a Blueprint for the admin route
admin_bp = Blueprint("admin_bp", __name__)

# Define the IP collection variable here
mongoconnection = pymongo.MongoClient("mongodb://mongo-service.mongo:27017/")
visitorsdb = mongoconnection["ips"]
attackcollection = visitorsdb["attacks"]

# Create a limiter instance with a rate limit of 3 attempts per minute for login
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379/0"  # Use Redis for storage
)
# Define the rate limit: 3 requests per minute
limiter.limit("3 per minute")(admin_bp)

@admin_bp.route('/admin', methods=["GET", "POST"])
@admin_bp.route('/config', methods=["GET", "POST"])
def honeypot():
    if request.method == "POST":
        # Check if the login attempts exceed the limit (3 attempts)
        if request.endpoint in ["admin_bp.honeypot", "admin_bp.config"]:
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

    # Render the admin.html template
    return render_template('admin.html')
