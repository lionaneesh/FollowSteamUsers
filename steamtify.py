import pynotify
import requests
import time

steam_ids = ["76561198183777685"]
last_state = {}
last_game = {}
personastates = ["Offline", "Online", "Busy", "Away", "Snooze", "Looking for Trade", "Looking to Play"]

def sendmessage(title, message):
    pynotify.init("Steam players notification")
    n = pynotify.Notification(title, message)
    n.set_urgency(pynotify.URGENCY_NORMAL)

    n.show()
    return

while 1:
        r = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=B6216A6CF0669D37FC7E49BA34256ADE&steamids=" + ','.join
        (steam_ids))
        players = r.json()
        try:
                players = players["response"]["players"]
        except KeyError:
                print "Invalid response, sleeping for 5 minutes"
                time.sleep(60 * 5)

        for p in players:
                if p["personastate"] >= 1:
                        if p["steamid"] in last_state:
                                if p["personastate"] != last_state[p["steamid"]]:
                                	sendmessage("Steam", "%s is now %s" % (p["personaname"], personastates[p["personastate"]]))
			else:
				sendmessage("Steam", "%s is now %s" % (p["personaname"], personastates[p["personastate"]]))
			last_state[p["steamid"]] = p["personastate"]

			if "gameextrainfo" in p:
				if p["steamid"] in last_game:
					if p["gameextrainfo"] != last_game[p["steamid"]]:
                                		sendmessage("Steam", "%s is now playing %s" % (p["personaname"], p["gameextrainfo"]))
				else:
					sendmessage("Steam", "%s is now playing %s" % (p["personaname"], p["gameextrainfo"]))
				last_game[p["steamid"]] = p["gameextrainfo"]
                        else:
                                last_game[p["steamid"]] = None

	time.sleep(10)
