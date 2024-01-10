from flask import Flask, make_response, jsonify
from config import Config
from time import sleep


app = Flask(__name__)
app.config.from_object(Config)


@app.route("/api/<email>/<sus>/<area>")
def index(email: str, sus: str, area: str):

    res = make_response(jsonify({
        'Email': email,
        'Suspicion': sus,
        'Location': area
    }), 200)
    
    return res
    

if __name__ == "__main__":
    app.run(debug=True)