from flask import Flask

app = Flask(__name__)

@app.route("/members")
def members():
    devices = [
        {   
            "devId": "a84041e081893e7f",
            "name": "Home",
            "lat": -33.707055119346386,
            "lng": 151.14593296712843,
            "full": 0,
            "emergency": 0,
            "current": 0,
        },
        {   
            "devId": "a84041e081893e80",
            "name": "Dog Lost",
            "lat": -33.703436,
            "lng": 151.152421,
            "full": 0,
            "emergency": 0,
            "current": 0,
        },
        {   
            "devId": "a84041e081893e81",
            "name": "Demo unit",
            "lat": -33.703273,
            "lng": 151.149308,
            "full": 0,
            "emergency": 0,
            "current": 0,
        },
    ]

    return devices
    # return {"members": ["Member1", "Member2", "Member3"]}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")