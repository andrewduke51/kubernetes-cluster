

@app.route("/clicknext")
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