from flask import Flask

app = Flask(__name__)

@app.route("/members")
def members():
    devices = [
        {   
            "devId": "a84041e081893e7f",
            "name": "Demo unit",
            "lng": -33.707055119346386, 
            "lat": 151.14593296712843,
            "full": 0,
            "emergency": 0,
            "current": 0,
        },
    ]

    return devices
    # return {"members": ["Member1", "Member2", "Member3"]}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")