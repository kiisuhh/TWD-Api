from flask import *
import json


app  = Flask(__name__)


@app.route("/api/v1/serverinfo", methods=["GET"])
def serverinfo():
    jsonraw = dict
    with open("data.json", "r") as f:
        fulldata = json.load(f)
    dataset = {
        "membercount": fulldata["Serverstats"]["membercount"],
        "roles": fulldata["Serverstats"]["rolecount"],
        "boosts": fulldata["Serverstats"]["boosts"],
        "twilights": fulldata["Serverstats"]["twilights"],
        "channel": fulldata["Serverstats"]["channel"]
    }
    json_dump = json.dumps(dataset)
    return json_dump


if __name__ == "__main__":
    app.run(port=6969)
