import json
import os

# Always resolve paths relative to THIS file so the game works
# regardless of which directory it is launched from.
_DIR = os.path.dirname(os.path.abspath(__file__))
LEADERBOARD_FILE = os.path.join(_DIR, "leaderboard.json")
SETTINGS_FILE    = os.path.join(_DIR, "settings.json")
DEFAULT_SETTINGS = {
    "sound":       False,       # True / False
    "car_color":   "green",     # "green" / "blue" / "yellow"
    "difficulty":  "normal",    # "easy" / "normal" / "hard"
    "username":    ""
}


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
        # Fill in any missing keys with defaults
        for k, v in DEFAULT_SETTINGS.items():
            data.setdefault(k, v)
        return data
    return dict(DEFAULT_SETTINGS)


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)


def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r") as f:
                data = json.load(f)
            # Guard against old string-format entries (e.g. ["name:score"])
            if isinstance(data, list) and all(isinstance(e, dict) for e in data):
                return data
        except (json.JSONDecodeError, Exception):
            pass
    return []


def save_score(username, score, distance):
    board = load_leaderboard()
    board.append({"name": username, "score": score, "distance": distance})
    # Sort by score descending, keep top 10
    board.sort(key=lambda x: x["score"], reverse=True)
    board = board[:10]
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(board, f, indent=2)
    return board
