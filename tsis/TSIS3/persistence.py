import json

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"


def load_settings():

    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)

    except:

        return {
            "sound": True,
            "difficulty": "normal"
        }


def save_settings(settings):

    with open(SETTINGS_FILE, "w") as f:

        json.dump(
            settings,
            f,
            indent=4
        )


def load_leaderboard():

    try:

        with open(LEADERBOARD_FILE, "r") as f:

            return json.load(f)

    except:

        return []


def save_score(name, score, distance):

    data = load_leaderboard()

    data.append({
        "name": name,
        "score": score,
        "distance": distance
    })

    data = sorted(
        data,
        key=lambda x: x["score"],
        reverse=True
    )[:10]

    with open(LEADERBOARD_FILE, "w") as f:

        json.dump(
            data,
            f,
            indent=4
        )