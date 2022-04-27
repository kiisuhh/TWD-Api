from flask import *
from flask_cors import CORS, cross_origin
import json


app  = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/api/v1/serverinfo", methods=["GET"])
@cross_origin()
def serverinfo():
    jsonraw = dict
    with open("data.json", "r") as f:
        fulldata = json.load(f)
    dataset = {
        "membercount": fulldata["Serverstats"]["membercount"],
        "roles": fulldata["Serverstats"]["rolecount"],
        "boosts": fulldata["Serverstats"]["boosts"],
        "twilights": fulldata["Serverstats"]["twilights"],
        "channel": fulldata["Serverstats"]["channel"],
        "bans": fulldata["Serverstats"]["bans"],
        "days": fulldata["Serverstats"]["days"],
        "bots": fulldata["Serverstats"]["bots"]
    }
    json_dump = json.dumps(dataset)
    return json_dump

@app.route("/api/v2/serverinfo", methods=["GET"])
@cross_origin()
def serverinfov2():
    jsonraw = dict
    with open("datav2.json", "r") as f:
        fulldata = json.load(f)
    dataset = {
        "membercount": fulldata["ServerStats"]["membercount"],
        "roles": fulldata["ServerStats"]["rolecount"],
        "boosts": fulldata["ServerStats"]["boosts"],
        "twilights": fulldata["ServerStats"]["twilights"],
        "channel": fulldata["ServerStats"]["channel"],
        "bans": fulldata["ServerStats"]["bans"],
        "days": fulldata["ServerStats"]["days"],
        "bots": fulldata["ServerStats"]["bots"],
        "acetag": fulldata["Team"]["Ace"]["name_format"],
        "aceav": fulldata["Team"]["Ace"]["Avatar"],
        "reiswafltag": fulldata["Team"]["Reiswafl"]["name_format"],
        "reiswaflav": fulldata["Team"]["Reiswafl"]["Avatar"],
        "pentag": fulldata["Team"]["Penmon"]["name_format"],
        "penav": fulldata["Team"]["Penmon"]["Avatar"],
        "azratag": fulldata["Team"]["azra"]["name_format"],
        "azraav": fulldata["Team"]["azra"]["Avatar"],
        "livtag": fulldata["Team"]["LIV"]["name_format"],
        "livav": fulldata["Team"]["LIV"]["Avatar"],
        "lucatag": fulldata["Team"]["luca"]["name_format"],
        "lucaav": fulldata["Team"]["luca"]["Avatar"],
        "carotag": fulldata["Team"]["caro"]["name_format"],
        "caroav": fulldata["Team"]["caro"]["Avatar"],
        "Maxtag": fulldata["Team"]["Max"]["name_format"],
        "Maxav": fulldata["Team"]["Max"]["Avatar"],
        "Picosohntag": fulldata["Team"]["Picosohn"]["name_format"],
        "Picosohnav": fulldata["Team"]["Picosohn"]["Avatar"],
        "kasumitag": fulldata["Team"]["kasumi"]["name_format"],
        "kasumiav": fulldata["Team"]["kasumi"]["Avatar"],
        "Paulustag": fulldata["Team"]["Paulus"]["name_format"],
        "Paulusav": fulldata["Team"]["Paulus"]["Avatar"],
        "Teejaytag": fulldata["Team"]["Teejay"]["name_format"],
        "Teejayav": fulldata["Team"]["Teejay"]["Avatar"],
        "Amelietag": fulldata["Team"]["Amelie"]["name_format"],
        "Amelieav": fulldata["Team"]["Amelie"]["Avatar"],
    }
    json_dump = json.dumps(dataset)
    return json_dump

if __name__ == "__main__":
    app.run(port=6969)
