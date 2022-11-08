from flask import Flask, render_template, jsonify, request
from multiprocessing import Value
import socket
import json
import os

# Connect to Redis
counter = Value('i', 0)
app=Flask(__name__,template_folder='views')

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/clicknext")
def home():
    with counter.get_lock():
        counter.value += 1
    data=counter.value
    ip_addr=request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    return render_template('home.html',
                           title="page",
                           json_value=json.dumps(data),
                           ip_addr=ip_addr,
                           hostname=socket.gethostname()
                           )

@app.route('/proxy_client')
def proxy_client():
    return render_template('proxy_client.html')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)