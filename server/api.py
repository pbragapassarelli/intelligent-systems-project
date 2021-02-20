from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/hello", methods=["POST"])
def hello_world():
    name = request.json['name']
    
    if name.isnumeric():
        return {}, 400

    return { "message": f"Hey {name}" }