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
max_login_attempts = 3

@admin_bp.route('/admin', methods=["GET", "POST"])
@admin_bp.route('/config', methods=["GET", "POST"])
def honeypot():
    # Get the IP address of the requester
    ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)

    # Check if the IP address has exceeded the max_login_attempts
    if ip_address in ip_login_attempts and ip_login_attempts[ip_address] >= max_login_attempts:
        # After max_login_attempts, respond with a humorous message
        funny_response = "Ha-ha! You've stumbled into our honeypot! 😜"
        return jsonify({"message": funny_response}), 200

    # Handle the login form submission
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check username and password (replace with your authentication logic)
        if username == "your_username" and password == "your_password":
            # Successful login, clear login attempts
            ip_login_attempts.pop(ip_address, None)
            # Redirect to admin panel or some other page
            return render_template("admin_panel.html")

        # If login fails, increment login attempts
        ip_login_attempts[ip_address] = ip_login_attempts.get(ip_address, 0) + 1

    # Render the admin.html template with login_attempt count
    login_attempt = ip_login_attempts.get(ip_address, 0)
    return render_template('admin.html', login_attempt=login_attempt)
