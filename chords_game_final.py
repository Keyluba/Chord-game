import random
import json
import os
import hashlib
import secrets
import time
import sys


# ============================================================
# CONFIGURATION
# ============================================================

VERITIES = [
    # Original verities
    "obesity", "falsity", "lovity", "larpity", "moggity", "cruelty", "curiosity", "purity",
    # Expanded Chords vocabulary
    "chord", "absurdity", "chaosity", "goobity", "sillity", "glorbity",
    "fluffity", "bonkity", "sparkity", "zoomity", "snackity", "wobblity",
    "quirkity", "mysticity", "cosmicity", "voidity", "royality", "chaosity",
    "giggleity", "gremlinity", "draconity", "shadowity", "dreamity", "luckity",
    "pointity", "xpity", "petity", "eggity", "boxity", "tradeity",
    "legendity", "mythicity", "secretity", "neonity", "goldity", "frostity",
    "emberity", "stormity", "toxicty", "angelity", "demonity", "rainbowity",
    "starity", "moonity", "sunity", "galaxity", "quantumity", "infinity"
]

SCOREBOARD_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "chord_scoreboard.json"
)

# Developer testing account. The raw access code is not stored in plaintext.
DEV_PLAYER_CODE = "DEV"
DEV_ACCESS_CODE_HASH = hashlib.sha256(
    "CHORDS-DEV-ACCESS-2026".encode("utf-8")
).hexdigest()

TIMED_MODE_SECONDS = 60
BASE_EVENT_CHANCE = 0.12      # chance of a random event per question


# Difficulty affects challenge size and reward multiplier. No daily systems are used.
DIFFICULTIES = {
    "Easy": {"reward": 0.80, "normal_len": (6, 10), "timed": 90, "memory_len": (3, 10)},
    "Normal": {"reward": 1.00, "normal_len": (8, 15), "timed": 60, "memory_len": (4, 20)},
    "Hard": {"reward": 1.25, "normal_len": (12, 20), "timed": 45, "memory_len": (8, 25)},
    "Extreme": {"reward": 1.60, "normal_len": (16, 28), "timed": 30, "memory_len": (12, 30)},
}

PRESTIGE_LEVEL = 50
PRESTIGE_BONUS = 0.10

PET_DATA = {
    "pointy_cat": {"name": "Pointy Cat", "rarity": "Common", "pointy": .05, "xp": 0, "event": 0},
    "xp_bunny": {"name": "XP Bunny", "rarity": "Common", "pointy": 0, "xp": .05, "event": 0},
    "sleepy_dog": {"name": "Sleepy Dog", "rarity": "Common", "pointy": .03, "xp": .02, "event": 0},
    "tiny_frog": {"name": "Tiny Frog", "rarity": "Common", "pointy": 0, "xp": .03, "event": .01},
    "hamster": {"name": "Hamster", "rarity": "Common", "pointy": .04, "xp": .01, "event": 0},
    "lucky_fox": {"name": "Lucky Fox", "rarity": "Rare", "pointy": 0, "xp": 0, "event": .08},
    "blue_penguin": {"name": "Blue Penguin", "rarity": "Rare", "pointy": .06, "xp": .03, "event": 0},
    "mushroom_mouse": {"name": "Mushroom Mouse", "rarity": "Rare", "pointy": .02, "xp": .06, "event": 0},
    "cloud_puppy": {"name": "Cloud Puppy", "rarity": "Rare", "pointy": .04, "xp": .04, "event": .03},
    "ninja_owl": {"name": "Ninja Owl", "rarity": "Rare", "pointy": 0, "xp": .08, "event": .03},
    "golden_slime": {"name": "Golden Slime", "rarity": "Epic", "pointy": .10, "xp": .05, "event": 0},
    "lava_lizard": {"name": "Lava Lizard", "rarity": "Epic", "pointy": .08, "xp": .08, "event": .02},
    "crystal_deer": {"name": "Crystal Deer", "rarity": "Epic", "pointy": .05, "xp": .12, "event": .02},
    "storm_crow": {"name": "Storm Crow", "rarity": "Epic", "pointy": .03, "xp": .06, "event": .10},
    "rainbow_axolotl": {"name": "Rainbow Axolotl", "rarity": "Epic", "pointy": .12, "xp": .04, "event": .04},
    "cosmic_dragon": {"name": "Cosmic Dragon", "rarity": "Legendary", "pointy": .15, "xp": .15, "event": .05},
    "phoenix": {"name": "Phoenix", "rarity": "Legendary", "pointy": .12, "xp": .18, "event": .06},
    "celestial_wolf": {"name": "Celestial Wolf", "rarity": "Legendary", "pointy": .18, "xp": .12, "event": .08},
    "galaxy_whale": {"name": "Galaxy Whale", "rarity": "Legendary", "pointy": .20, "xp": .10, "event": .05},
    "void_kitty": {"name": "Void Kitty", "rarity": "Mythic", "pointy": .20, "xp": .10, "event": .10},
    "nebula_serpent": {"name": "Nebula Serpent", "rarity": "Mythic", "pointy": .22, "xp": .16, "event": .08},
    "time_bunny": {"name": "Time Bunny", "rarity": "Mythic", "pointy": .10, "xp": .25, "event": .05},
    "reality_glitch": {"name": "Reality Glitch", "rarity": "Mythic", "pointy": .25, "xp": .10, "event": .12},
    "pointy_god": {"name": "Pointy God", "rarity": "Divine", "pointy": .30, "xp": .25, "event": .15},
    "infinity_dragon": {"name": "Infinity Dragon", "rarity": "Divine", "pointy": .28, "xp": .30, "event": .18},
    "world_eater": {"name": "World Eater", "rarity": "Divine", "pointy": .35, "xp": .20, "event": .20},
    "secret_glitch_cat": {"name": "??? Glitch Cat", "rarity": "Secret", "pointy": .45, "xp": .35, "event": .25},
    "secret_void_dragon": {"name": "Void Emperor", "rarity": "Secret", "pointy": .50, "xp": .40, "event": .30},
    "secret_pointy": {"name": "The Forbidden Pointy", "rarity": "Secret", "pointy": .60, "xp": .50, "event": .35},
}


EGG_DATA = {
    "egg_common": {"name": "Common Egg", "rarity": "Common", "weights": {"pointy_cat": 30, "xp_bunny": 25, "sleepy_dog": 20, "tiny_frog": 15, "hamster": 10}},
    "egg_rare": {"name": "Rare Egg", "rarity": "Rare", "weights": {"xp_bunny": 10, "lucky_fox": 25, "blue_penguin": 25, "mushroom_mouse": 20, "cloud_puppy": 15, "ninja_owl": 5}},
    "egg_epic": {"name": "Epic Egg", "rarity": "Epic", "weights": {"lucky_fox": 8, "golden_slime": 30, "lava_lizard": 20, "crystal_deer": 18, "storm_crow": 14, "rainbow_axolotl": 10}},
    "egg_legendary": {"name": "Legendary Egg", "rarity": "Legendary", "weights": {"golden_slime": 8, "cosmic_dragon": 35, "phoenix": 22, "celestial_wolf": 20, "galaxy_whale": 15}},
    "egg_mythic": {"name": "Mythic Egg", "rarity": "Mythic", "weights": {"cosmic_dragon": 10, "void_kitty": 35, "nebula_serpent": 25, "time_bunny": 15, "reality_glitch": 15}},
    "egg_divine": {"name": "Divine Egg", "rarity": "Divine", "weights": {"void_kitty": 10, "pointy_god": 35, "infinity_dragon": 30, "world_eater": 25}},
    "egg_secret": {"name": "??? Secret Egg", "rarity": "Secret", "weights": {"secret_glitch_cat": 70, "secret_void_dragon": 25, "secret_pointy": 5}},
}


TRADABLE_ITEMS = {
    "trade_gem": {"name": "Trade Gem", "desc": "A shiny collectible. Tradable."},
    "golden_ticket": {"name": "Golden Ticket", "desc": "A rare collectible. Tradable."},
    "casino_chip": {"name": "Casino Chip", "desc": "A collectible casino chip. Tradable."},
    "mystery_token": {"name": "Mystery Token", "desc": "Opens special mystery rewards. Tradable."},
    "pet_token": {"name": "Pet Token", "desc": "A collectible token used for pet trades. Tradable."},
    "rainbow_ticket": {"name": "Rainbow Ticket", "desc": "A very rare achievement/shop collectible. Tradable."},
    "void_shard": {"name": "Void Shard", "desc": "A dark shard with unknown value. Tradable."},
    "secret_coin": {"name": "Secret Coin", "desc": "A hidden collectible tied to Secret pets. Tradable."},
    "jackpot_chip": {"name": "Jackpot Chip", "desc": "A casino collectible worth bragging about. Tradable."},
    "achievement_medal": {"name": "Achievement Medal", "desc": "A trophy collectible earned from milestones. Tradable."},
}


MYSTERY_BOX_ITEMS = ["potion", "xp_potion", "lucky_charm", "extra_time", "shield", "hint_token", "memory_peek"]


# ============================================================
# WINDOWS ANSI COLOR SUPPORT
# ============================================================

def enable_colors():
    if os.name != "nt":
        return
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)
        mode = ctypes.c_ulong()
        if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)
    except Exception:
        pass


enable_colors()


# ============================================================
# THEMES
# ============================================================

def _theme(name, title, accent, success, error, info, text="97"):
    def c(n):
        return f"\033[{n}m"
    return {
        "name": name, "reset": c(0), "title": c(title), "accent": c(accent),
        "success": c(success), "error": c(error), "info": c(info),
        "text": c(text)
    }


THEMES = {
    "default": _theme("Default", 96, 93, 92, 91, 94),
    "red":     _theme("Red", 91, 93, 91, 31, 95),
    "green":   _theme("Green", 92, 93, 92, 91, 96),
    "blue":    _theme("Blue", 94, 96, 92, 91, 95),
    "purple":  _theme("Purple", 95, 96, 92, 91, 94),
    "yellow":  _theme("Yellow", 93, 97, 92, 91, 96),
    # Shop themes
    "gold": _theme("Gold", "38;5;220", "38;5;214", "38;5;226",
                   "38;5;196", "38;5;178", "38;5;230"),
    "neon": _theme("Neon", "38;5;46", "38;5;201", "38;5;46",
                   "38;5;196", "38;5;51", "38;5;15"),
}

FREE_THEMES = ["default", "red", "green", "blue", "purple", "yellow"]


# ============================================================
# ACHIEVEMENTS   id: (name, description, reward_type, reward)
# ============================================================

_ACH = {
    # Normal game
    "first_game": ("First Steps", "Complete your first game.", "pointys", 5),
    "five_games": ("Getting Serious", "Complete 5 games.", "pointys", 10),
    "ten_games": ("Regular", "Complete 10 games.", "pointys", 20),
    "games_25": ("Dedicated", "Complete 25 games.", "pointys", 25),
    "fifty_games": ("Veteran", "Complete 50 games.", "pointys", 50),
    "games_100": ("Centurion", "Complete 100 games.", "xp", 500),
    "games_250": ("Chords Legend", "Complete 250 games.", "xp", 1500),
    "first_correct_5": ("First Answer", "Get 5 correct answers.", "xp", 50),
    "correct_25": ("25 Correct", "Get 25 correct answers.", "xp", 100),
    "correct_100": ("100 Correct", "Get 100 correct answers.", "xp", 250),
    "correct_250": ("250 Correct", "Get 250 correct answers.", "xp", 500),
    "correct_500": ("500 Correct", "Get 500 correct answers.", "xp", 1000),
    "correct_1000": ("1,000 Correct", "Get 1,000 correct answers.", "xp", 2500),
    "perfect_game": ("Perfectity", "Complete a game without a wrong answer.", "pointys", 25),
    # Combos
    "combo_5": ("Combo Starter", "Reach a 5x combo.", "xp", 75),
    "combo_10": ("Combo Machine", "Reach a 10x combo.", "xp", 150),
    "combo_20": ("Unstoppable", "Reach a 20x combo.", "xp", 300),
    "combo_30": ("Combo 30", "Reach a 30x combo.", "xp", 600),
    "combo_50": ("Combo 50", "Reach a 50x combo.", "xp", 1000),
    "combo_100": ("Combo 100", "Reach a 100x combo.", "xp", 2000),
    "combo_150": ("Combo 150", "Reach a 150x combo.", "xp", 4000),
    "combo_250": ("Combo 250", "Reach a 250x combo.", "xp", 7500),
    # Pointys
    "points_25": ("Pocket Change", "Have at least 25 pointys.", "xp", 50),
    "points_50": ("Pointy Collector", "Have at least 50 pointys.", "pointys", 5),
    "points_100": ("Pointy Hoarder", "Have at least 100 pointys.", "xp", 150),
    "points_250": ("Rich-ish", "Have at least 250 pointys.", "xp", 300),
    "points_500": ("Pointy Billionaire", "Have at least 500 pointys.", "xp", 600),
    "points_1000": ("Pointy Millionaire", "Have at least 1,000 pointys.", "xp", 1500),
    "points_5000_earned": ("Pointy Empire", "Earn 5,000 pointys over your career.", "xp", 5000),
    # Timed
    "timed_first": ("Against the Clock", "Complete your first timed game.", "pointys", 10),
    "timed_5": ("Speedy", "Get 5 correct answers in one timed game.", "xp", 75),
    "timed_10": ("Speed Demon", "Get 10 correct answers in one timed game.", "xp", 150),
    "timed_15": ("Fast Hands", "Get 15 correct answers in one timed game.", "xp", 200),
    "timed_25": ("Human Calculator", "Get 25 correct answers in one timed game.", "xp", 500),
    "timed_30": ("Lightning", "Get 30 correct answers in one timed game.", "xp", 500),
    "timed_40": ("One Minute Monster", "Get 40 correct answers in one timed game.", "xp", 1000),
    "timed_50": ("Time Lord", "Get 50 correct answers in one timed game.", "xp", 2500),
    # Memory
    "memory_first": ("Photographic Memory", "Complete your first memory game.", "pointys", 10),
    "memory_4": ("Short-Term Memory", "Correctly remember a sequence of 4.", "xp", 75),
    "memory_5": ("Rememberer", "Correctly remember a sequence of 5.", "xp", 150),
    "memory_8": ("Memory Pro", "Correctly remember a sequence of 8.", "xp", 400),
    "memory_10": ("Human RAM", "Correctly remember a sequence of 10.", "xp", 750),
    "memory_12": ("Perfect Memory", "Perfectly remember a sequence of 12.", "xp", 1500),
    "memory_20": ("Photographic Brain", "Correctly remember a sequence of 20.", "xp", 3000),
    # Endless
    "endless_first": ("Into Infinity", "Complete your first endless run.", "pointys", 10),
    "endless_10": ("Endless Beginner", "Reach 10 correct answers in endless mode.", "pointys", 20),
    "endless_20": ("Endless Veteran", "Reach 20 correct answers in endless mode.", "pointys", 30),
    "endless_25": ("Endless", "Reach 25 correct answers in endless mode.", "pointys", 50),
    "endless_50": ("Eternal Chords", "Reach 50 correct answers in endless mode.", "xp", 500),
    "endless_100": ("Never Stop", "Reach 100 correct answers in endless mode.", "xp", 2000),
    "endless_250": ("Beyond Infinity", "Reach 250 correct answers in endless mode.", "xp", 5000),
    # Blackjack
    "blackjack_first": ("First Hand", "Play your first blackjack hand.", "pointys", 10),
    "blackjack_win": ("Card Shark", "Win 5 blackjack hands.", "pointys", 25),
    "blackjack_7": ("Lucky Seven", "Win 7 blackjack hands.", "pointys", 20),
    "blackjack_blackjack": ("Blackjack!", "Get a natural blackjack.", "xp", 250),
    "blackjack_25": ("Blackjack Master", "Win 25 blackjack hands.", "xp", 750),
    "blackjack_100": ("Housebreaker", "Win 100 blackjack hands.", "xp", 3000),
    "blackjack_500": ("High Roller", "Make 500 pointys of total blackjack profit.", "xp", 750),
    "blackjack_1000": ("Casino Owner", "Make 1,000 pointys of total blackjack profit.", "pointys", 150),
    "blackjack_double": ("Double Down", "Win a blackjack hand after doubling down.", "xp", 150),
    # Levels
    "level_10": ("Chords Master", "Reach level 10.", "xp", 1000),
    "level_20": ("Chords Expert", "Reach level 20.", "xp", 5000),
    "level_50": ("Chords God", "Reach level 50.", "xp", 15000),
    # Random events
    "event_first": ("Lucky Break", "Trigger your first random event.", "pointys", 10),
    "event_10": ("Event Magnet", "Trigger 10 random events.", "xp", 150),
    "event_50": ("Fortune's Favorite", "Trigger 50 random events.", "xp", 750),
    # Shop
    "shop_first": ("Window Shopper", "Buy your first item from the Pointy Shop.", "pointys", 5),
    "shop_10": ("Big Spender", "Buy 10 items from the Pointy Shop.", "xp", 150),
    "spend_500": ("Shopaholic", "Spend 500 pointys in the shop.", "xp", 300),
    "all_upgrades": ("Fully Upgraded", "Own every permanent upgrade.", "xp", 1000),
}

ACHIEVEMENTS = {
    key: {"name": v[0], "description": v[1], "reward_type": v[2], "reward": v[3]}
    for key, v in _ACH.items()
}

# (achievement id, player stat, threshold)
ACHIEVEMENT_RULES = [
    ("first_game", "games", 1), ("five_games", "games", 5),
    ("ten_games", "games", 10), ("games_25", "games", 25),
    ("fifty_games", "games", 50), ("games_100", "games", 100),
    ("games_250", "games", 250),
    ("first_correct_5", "correct_answers", 5), ("correct_25", "correct_answers", 25),
    ("correct_100", "correct_answers", 100), ("correct_250", "correct_answers", 250),
    ("correct_500", "correct_answers", 500), ("correct_1000", "correct_answers", 1000),
    ("combo_5", "best_combo", 5), ("combo_10", "best_combo", 10),
    ("combo_20", "best_combo", 20), ("combo_30", "best_combo", 30),
    ("combo_50", "best_combo", 50), ("combo_100", "best_combo", 100),
    ("combo_150", "best_combo", 150), ("combo_250", "best_combo", 250),
    ("points_25", "coins", 25), ("points_50", "coins", 50),
    ("points_100", "coins", 100), ("points_250", "coins", 250),
    ("points_500", "coins", 500), ("points_1000", "coins", 1000),
    ("points_5000_earned", "total_pointys_earned", 5000),
    ("timed_first", "timed_games", 1), ("timed_5", "timed_best", 5),
    ("timed_10", "timed_best", 10), ("timed_15", "timed_best", 15),
    ("timed_25", "timed_best", 25), ("timed_30", "timed_best", 30),
    ("timed_40", "timed_best", 40), ("timed_50", "timed_best", 50),
    ("memory_first", "memory_games", 1), ("memory_4", "memory_best", 4),
    ("memory_5", "memory_best", 5), ("memory_8", "memory_best", 8),
    ("memory_10", "memory_best", 10), ("memory_12", "memory_perfect_best", 12),
    ("memory_20", "memory_best", 20),
    ("endless_first", "endless_games", 1), ("endless_10", "endless_best", 10),
    ("endless_20", "endless_best", 20), ("endless_25", "endless_best", 25),
    ("endless_50", "endless_best", 50), ("endless_100", "endless_best", 100),
    ("endless_250", "endless_best", 250),
    ("blackjack_first", "blackjack_games", 1), ("blackjack_win", "blackjack_wins", 5),
    ("blackjack_7", "blackjack_wins", 7), ("blackjack_blackjack", "blackjack_blackjacks", 1),
    ("blackjack_25", "blackjack_wins", 25), ("blackjack_100", "blackjack_wins", 100),
    ("blackjack_500", "blackjack_profit", 500), ("blackjack_1000", "blackjack_profit", 1000),
    ("blackjack_double", "blackjack_double_down_wins", 1),
    ("level_10", "level", 10), ("level_20", "level", 20), ("level_50", "level", 50),
    ("event_first", "events_seen", 1), ("event_10", "events_seen", 10),
    ("event_50", "events_seen", 50),
    ("shop_first", "items_bought", 1), ("shop_10", "items_bought", 10),
    ("spend_500", "pointys_spent", 500), ("all_upgrades", "upgrade_count", 4),
]


# ============================================================
# RANDOM EVENTS
# ============================================================

EVENTS = [
    {"id": "double", "weight": 4, "mult": 2,
     "name": "DOUBLE POINTYS",
     "desc": "Pointys from this answer are doubled!"},
    {"id": "triple", "weight": 2, "mult": 3,
     "name": "TRIPLE POINTYS",
     "desc": "Pointys from this answer are tripled!"},
    {"id": "guesses", "weight": 3, "guesses": 3,
     "name": "TRIPLE GUESS",
     "desc": "You get 3 guesses on this one - mistakes can't hurt you!"},
    {"id": "jackpot", "weight": 1, "bonus": 10,
     "name": "JACKPOT",
     "desc": "Answer correctly for a +10 pointy bonus!"},
    {"id": "xp_surge", "weight": 2, "xp": 15,
     "name": "XP SURGE",
     "desc": "Answer correctly for +15 bonus XP!"},
]


def roll_event(player, boosts):
    chance = BASE_EVENT_CHANCE + boosts["event_bonus"]

    if "clover" in player["upgrades"]:
        chance += 0.10
    chance += pet_bonus(player, "event")

    chance = min(chance, 0.6)

    if random.random() >= chance:
        return None

    event = random.choices(
        EVENTS,
        weights=[e["weight"] for e in EVENTS]
    )[0]

    player["events_seen"] += 1

    print(color(player, f"\n*** RANDOM EVENT: {event['name']}! ***", "accent"))
    print(color(player, event["desc"], "info"))

    return event


def difficulty_data(player):
    return DIFFICULTIES.get(player.get("difficulty", "Normal"), DIFFICULTIES["Normal"])


def pet_bonus(player, key):
    pet_id = player.get("active_pet", "")
    pet = PET_DATA.get(pet_id)
    return pet.get(key, 0.0) if pet else 0.0


def total_reward_multiplier(player):
    return float(player.get("prestige_multiplier", 1.0)) * (1.0 + pet_bonus(player, "pointy")) * difficulty_data(player)["reward"]


def total_xp_multiplier(player):
    return float(player.get("prestige_multiplier", 1.0)) * (1.0 + pet_bonus(player, "xp")) * difficulty_data(player)["reward"]


def pointy_reward(base, event, boosts, player=None):
    """Pointys for one answer after potions, difficulty, prestige, pets and events."""
    mult = boosts["pointy_mult"]

    if event and event.get("mult"):
        mult *= event["mult"]
        base = max(base, 1)

    amount = base * mult

    if event and event.get("bonus"):
        amount += event["bonus"]

    if player is not None:
        amount *= total_reward_multiplier(player)

    return int(amount)


def claim_event_xp(player, event, scoreboard):
    if event and event.get("xp"):
        print(color(player, f"+{event['xp']} bonus XP!", "info"))
        add_xp(player, event["xp"], scoreboard)


# ============================================================
# SHOP ITEMS
# ============================================================

SHOP_ITEMS = {
    # Consumables
    "hint_token": {"name": "Hint Token", "type": "consumable", "price": 8,
                   "desc": "A free hint (instead of paying 5 pointys)."},
    "shield": {"name": "Combo Shield", "type": "consumable", "price": 20,
               "desc": "Saves your combo from one wrong answer "
                       "(or saves an Endless run)."},
    "potion": {"name": "Pointy Potion", "type": "consumable", "price": 40,
               "desc": "2x pointys for one game."},
    "xp_potion": {"name": "XP Potion", "type": "consumable", "price": 30,
                  "desc": "2x XP for one game."},
    "lucky_charm": {"name": "Lucky Charm", "type": "consumable", "price": 50,
                    "desc": "Random events are much more likely for one game."},
    "extra_time": {"name": "Time Extender", "type": "consumable", "price": 35,
                   "desc": "+15 seconds in your next Timed game."},
    "memory_peek": {"name": "Memory Peek", "type": "consumable", "price": 25,
                    "desc": "Look at the sequence again in Memory mode (type peek)."},
    "mystery_box": {"name": "Mystery Box", "type": "mystery", "price": 75,
                    "desc": "Randomly gives pointys, XP, nothing, an egg, a boost, or a tradable."},
    "lucky_box": {"name": "Lucky Mystery Box", "type": "mystery", "price": 180,
                   "desc": "Better odds for rare eggs, bigger rewards, and rarer tradables."},
    # Permanent upgrades
    "magnet": {"name": "Pointy Magnet", "type": "upgrade", "price": 200,
               "desc": "+2 bonus pointys every time you finish a game."},
    "xp_booster": {"name": "XP Booster", "type": "upgrade", "price": 250,
                   "desc": "+25% XP from everything you play."},
    "clover": {"name": "Lucky Clover", "type": "upgrade", "price": 300,
               "desc": "Random events happen more often, forever."},
    "combo_saver": {"name": "Combo Saver", "type": "upgrade", "price": 150,
                    "desc": "A wrong answer halves your combo instead of resetting it."},
    # Themes
    "theme_gold": {"name": "Gold Theme", "type": "theme", "price": 60,
                   "value": "gold", "desc": "Shiny gold colors."},
    "theme_neon": {"name": "Neon Theme", "type": "theme", "price": 60,
                   "value": "neon", "desc": "Bright neon colors."},
    # Titles
    "title_enjoyer": {"name": "Title: Chords Enjoyer", "type": "title", "price": 75,
                      "value": "Chords Enjoyer", "desc": "Shown next to your name."},
    "title_tycoon": {"name": "Title: Pointy Tycoon", "type": "title", "price": 300,
                     "value": "Pointy Tycoon", "desc": "Shown next to your name."},
    "title_overlord": {"name": "Title: Chords Overlord", "type": "title", "price": 1000,
                       "value": "Chords Overlord", "desc": "Shown next to your name."},
}

SECTION_NAMES = {
    "consumable": "CONSUMABLES (one use each)",
    "upgrade": "PERMANENT UPGRADES",
    "theme": "THEMES",
    "title": "TITLES",
    "mystery": "MYSTERY BOXES",
}

BOOST_PROMPTS = [
    # item id, label, description, boost key, value
    ("potion", "Pointy Potion", "2x pointys this game", "pointy_mult", 2),
    ("xp_potion", "XP Potion", "2x XP this game", "xp_mult", 2),
    ("lucky_charm", "Lucky Charm", "more random events this game", "event_bonus", 0.15),
    ("extra_time", "Time Extender", "+15 seconds", "extra_seconds", 15),
]


# ============================================================
# COLOR / NAME HELPERS
# ============================================================

def get_theme(player):
    name = player.get("theme", "default")
    if name not in THEMES:
        name = "default"
    return THEMES[name]


def color(player, text, style="text"):
    theme = get_theme(player)
    return theme.get(style, "") + str(text) + theme.get("reset", "")


def display_name(player):
    title = player.get("title", "")
    if title:
        return f"[{title}] {player['name']}"
    return player["name"]


def banner(player, text, style="title"):
    print(color(player, "\n=================================", "title"))
    print(color(player, text.center(33).rstrip(), style))
    print(color(player, "=================================", "title"))


# ============================================================
# PASSWORD FUNCTIONS
# ============================================================

def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100_000
    ).hex()

    return salt, password_hash


def check_password(password, salt, stored_hash):
    _, password_hash = hash_password(password, salt)
    return password_hash == stored_hash


# ============================================================
# PLAYER DEFAULTS / MIGRATION
# ============================================================

def default_stats():
    return {
        "coins": 0, "total_pointys_earned": 0,
        "is_dev": False,
        "games": 0, "best_combo": 0,
        "xp": 0, "level": 1,
        "achievements": [],
        "correct_answers": 0, "wrong_answers": 0, "hints_used": 0,
        "timed_games": 0, "timed_correct": 0, "timed_best": 0,
        "memory_games": 0, "memory_best": 0,
        "memory_perfect_best": 0, "memory_correct": 0,
        "endless_games": 0, "endless_best": 0, "endless_total_correct": 0,
        "blackjack_games": 0, "blackjack_wins": 0, "blackjack_losses": 0,
        "blackjack_pushes": 0, "blackjack_blackjacks": 0,
        "blackjack_profit": 0, "blackjack_double_down_wins": 0,
        "total_questions": 0,
        # Events + shop
        "events_seen": 0, "items_bought": 0, "pointys_spent": 0,
        "inventory": {}, "upgrades": [],
        "owned_themes": [], "owned_titles": [], "title": "",
        "theme": "default",
        "difficulty": "Normal",
        "custom_mode": {"length": 10, "lives": 1, "reward": 1.0},
        "prestige": 0, "prestige_multiplier": 1.0,
        "pets": [], "active_pet": "",
        "history": {"chord": [], "timed": [], "memory": [], "endless": [], "custom": []},
        "casino_games": 0, "casino_wins": 0, "casino_profit": 0,
    }


def create_default_player_data(name, salt, password_hash):
    data = default_stats()
    data["name"] = name
    data["password_salt"] = salt
    data["password_hash"] = password_hash
    return data


def migrate_player(player):
    for key, value in default_stats().items():
        if key not in player:
            player[key] = value

    for key in ("achievements", "upgrades", "owned_themes", "owned_titles"):
        if not isinstance(player[key], list):
            player[key] = []

    if not isinstance(player["inventory"], dict):
        player["inventory"] = {}

    if player.get("difficulty") not in DIFFICULTIES:
        player["difficulty"] = "Normal"
    if not isinstance(player.get("custom_mode"), dict):
        player["custom_mode"] = {"length": 10, "lives": 1, "reward": 1.0}
    if not isinstance(player.get("pets"), list):
        player["pets"] = []
    if not isinstance(player.get("history"), dict):
        player["history"] = {}
    for mode in ("chord", "timed", "memory", "endless", "custom"):
        if not isinstance(player["history"].get(mode), list):
            player["history"][mode] = []
    if not isinstance(player.get("prestige"), int):
        player["prestige"] = 0
    if not isinstance(player.get("prestige_multiplier"), (int, float)):
        player["prestige_multiplier"] = 1.0
    if not isinstance(player.get("active_pet"), str):
        player["active_pet"] = ""

    return player


def ensure_dev_account(scoreboard):
    """Create/update the local developer testing account."""
    if DEV_PLAYER_CODE not in scoreboard:
        salt, password_hash = hash_password(secrets.token_urlsafe(24))
        player = create_default_player_data("Developer", salt, password_hash)
        player["is_dev"] = True
        player["coins"] = 999999
        player["total_pointys_earned"] = 999999
        player["level"] = PRESTIGE_LEVEL
        player["xp"] = 0
        player["prestige"] = 5
        player["prestige_multiplier"] = 1.0 + (5 * PRESTIGE_BONUS)
        player["upgrades"] = ["magnet", "xp_booster", "clover", "combo_saver"]
        player["owned_themes"] = ["gold", "neon"]
        player["owned_titles"] = [
            item["value"] for item in SHOP_ITEMS.values()
            if item.get("type") == "title" and item.get("value")
        ]
        player["title"] = "Developer"
        player["pets"] = list(PET_DATA.keys())
        player["active_pet"] = "void_kitty"

        for item_id in SHOP_ITEMS:
            player["inventory"][item_id] = 99
        for egg_id in EGG_DATA:
            player["inventory"][egg_id] = 99
        for trade_id in TRADABLE_ITEMS:
            player["inventory"][trade_id] = 99

        player["achievements"] = list(ACHIEVEMENTS.keys())
        scoreboard[DEV_PLAYER_CODE] = player
        save_scoreboard(scoreboard)
    else:
        migrate_player(scoreboard[DEV_PLAYER_CODE])
        scoreboard[DEV_PLAYER_CODE]["is_dev"] = True


def migrate_scoreboard(scoreboard):
    for code in scoreboard:
        if isinstance(scoreboard[code], dict):
            migrate_player(scoreboard[code])
    ensure_dev_account(scoreboard)
    return scoreboard


# ============================================================
# SCOREBOARD
# ============================================================

def load_scoreboard():
    if not os.path.exists(SCOREBOARD_FILE):
        return {}

    try:
        with open(SCOREBOARD_FILE, "r", encoding="utf-8") as file:
            scoreboard = json.load(file)
        return migrate_scoreboard(scoreboard)
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read scoreboard.")
        return {}


def save_scoreboard(scoreboard):
    try:
        with open(SCOREBOARD_FILE, "w", encoding="utf-8") as file:
            json.dump(scoreboard, file, indent=4)
    except OSError:
        print("Warning: Could not save scoreboard.")


# ============================================================
# POINTYS / INVENTORY HELPERS
# ============================================================

def give_pointys(player, amount, scoreboard=None):
    if amount <= 0:
        return

    player["coins"] += amount
    player["total_pointys_earned"] += amount

    if scoreboard is not None:
        save_scoreboard(scoreboard)


def inv_count(player, item_id):
    return player["inventory"].get(item_id, 0)


def add_item(player, item_id, amount=1):
    player["inventory"][item_id] = inv_count(player, item_id) + amount


def remove_item(player, item_id):
    if inv_count(player, item_id) <= 0:
        return False

    player["inventory"][item_id] -= 1

    if player["inventory"][item_id] <= 0:
        del player["inventory"][item_id]

    return True


def magnet_bonus(player):
    return 2 if "magnet" in player["upgrades"] else 0


def start_boosts(player, scoreboard, timed=False):
    """Offer any owned one-game boosts at the start of a game."""
    boosts = {
        "pointy_mult": 1, "xp_mult": 1,
        "event_bonus": 0.0, "extra_seconds": 0
    }

    for item_id, label, desc, key, value in BOOST_PROMPTS:
        if item_id == "extra_time" and not timed:
            continue

        count = inv_count(player, item_id)

        if count <= 0:
            continue

        answer = input(
            f"\nYou have {count}x {label}. Use one? ({desc}) [y/N]: "
        ).strip().lower()

        if answer in ("y", "yes"):
            remove_item(player, item_id)

            if key in ("pointy_mult", "xp_mult"):
                boosts[key] *= value
            else:
                boosts[key] += value

            print(color(player, f"{label} activated!", "success"))

    save_scoreboard(scoreboard)

    return boosts


def try_shield(player, scoreboard):
    if remove_item(player, "shield"):
        save_scoreboard(scoreboard)
        print(color(player, "COMBO SHIELD used! You're protected.", "success"))
        return True
    return False


def handle_miss(player, scoreboard, combo):
    """New combo after a wrong answer (shield / combo saver aware)."""
    if combo <= 0:
        return 0

    if try_shield(player, scoreboard):
        return combo

    if "combo_saver" in player["upgrades"]:
        new_combo = combo // 2
        print(color(player, f"Combo Saver! Combo drops to {new_combo}x.", "info"))
        return new_combo

    return 0


# ============================================================
# XP / LEVEL SYSTEM
# ============================================================

def xp_required_for_level(level):
    return 100 + ((level - 1) * 50)


def update_level(player):
    leveled_up = False

    while player["level"] < PRESTIGE_LEVEL and player["xp"] >= xp_required_for_level(player["level"]):
        player["xp"] -= xp_required_for_level(player["level"])
        player["level"] += 1
        leveled_up = True

    return leveled_up


def add_xp(player, amount, scoreboard=None):
    if amount <= 0:
        return False

    if "xp_booster" in player["upgrades"]:
        amount = int(amount * 1.25)

    amount = max(1, int(amount * total_xp_multiplier(player)))

    old_level = player["level"]
    player["xp"] += amount

    if update_level(player):
        print(color(
            player, f"\nLEVEL UP! You are now level {player['level']}!", "accent"
        ))

    if scoreboard is not None:
        save_scoreboard(scoreboard)

    return player["level"] > old_level


def xp_progress_text(player):
    return f"{player['xp']}/{xp_required_for_level(player['level'])} XP"



def prestige_player(scoreboard, player_code):
    player = scoreboard[player_code]
    if player["level"] < PRESTIGE_LEVEL:
        print(f"You need level {PRESTIGE_LEVEL} to prestige.")
        return False

    gain = player.get("prestige", 0) + 1
    bonus = 1.0 + gain * PRESTIGE_BONUS
    print("\n========== PRESTIGE ==========")
    print(f"You are about to rebirth from level {player['level']}.")
    print(f"Prestige will become {gain} and your permanent reward/XP multiplier will become {bonus:.2f}x.")
    print("Your lifetime stats, pointys, pets, inventory and achievements stay.")
    confirm = input("Type PRESTIGE to continue: ").strip().upper()
    if confirm != "PRESTIGE":
        print("Prestige cancelled.")
        return False

    player["prestige"] = gain
    player["prestige_multiplier"] = bonus
    player["level"] = 1
    player["xp"] = 0
    player["owned_titles"] = player.get("owned_titles", [])
    title = f"Prestige {gain}"
    if title not in player["owned_titles"]:
        player["owned_titles"].append(title)
    player["title"] = title
    save_scoreboard(scoreboard)
    print(color(player, f"\nREBIRTH COMPLETE! You are Prestige {gain}.", "accent"))
    print(f"Permanent multiplier: {bonus:.2f}x")
    input("\nPress ENTER to continue...")
    return True


# ============================================================
# ACHIEVEMENT UNLOCKING / CHECKING
# ============================================================

def unlock_achievement(player, achievement_id, scoreboard=None):
    if achievement_id not in ACHIEVEMENTS:
        return False

    if achievement_id in player["achievements"]:
        return False

    achievement = ACHIEVEMENTS[achievement_id]
    reward_type = achievement["reward_type"]
    reward = achievement["reward"]

    player["achievements"].append(achievement_id)

    print(color(player, "\n🏆 ACHIEVEMENT UNLOCKED!", "accent"))
    print(color(player, achievement["name"], "success"))
    print(achievement["description"])

    if reward_type == "pointys":
        player["coins"] += reward
        print(color(player, f"+{reward} pointys", "info"))

    elif reward_type == "xp":
        player["xp"] += reward
        print(color(player, f"+{reward} XP", "info"))

        while player["xp"] >= xp_required_for_level(player["level"]):
            player["xp"] -= xp_required_for_level(player["level"])
            player["level"] += 1
            print(color(
                player, f"LEVEL UP! You are now level {player['level']}!", "accent"
            ))

    if scoreboard is not None:
        save_scoreboard(scoreboard)

    return True


def check_achievements(player, scoreboard=None, perfect_game=False):
    stats = dict(player)
    stats["upgrade_count"] = len(player["upgrades"])

    for achievement_id, stat, threshold in ACHIEVEMENT_RULES:
        if stats.get(stat, 0) >= threshold:
            unlock_achievement(player, achievement_id, scoreboard)

    if perfect_game:
        unlock_achievement(player, "perfect_game", scoreboard)


# ============================================================
# PLAYER CREATION / LOGIN
# ============================================================

def create_player(scoreboard):
    print("\n========== CREATE PLAYER ==========")

    name = input("Player name: ").strip()

    while not name:
        print("Player name cannot be empty.")
        name = input("Player name: ").strip()

    while True:
        code = input("Player code: ").strip().upper()

        if not code:
            print("Player code cannot be empty.")
            continue

        if code in scoreboard:
            print("That player code is already being used. Please choose another.")
            continue

        break

    while True:
        password = input("Password: ")

        if not password:
            print("Password cannot be empty.")
            continue

        confirm = input("Confirm password: ")

        if password != confirm:
            print("Passwords don't match.")
            continue

        break

    salt, password_hash = hash_password(password)

    scoreboard[code] = create_default_player_data(name, salt, password_hash)
    save_scoreboard(scoreboard)

    print("\nPlayer successfully created.")
    print(f"Name: {name}")
    print(f"Code: {code}")
    print("\nRemember your player code and password.")

    return code


def login_player(scoreboard):
    print("\n========== PLAYER LOGIN ==========")

    while True:
        code = input("Player code: ").strip().upper()

        if code not in scoreboard:
            print("Player code not found.")
            continue

        player = scoreboard[code]
        migrate_player(player)

        password = input("Password: ")

        # Developer shortcut: the secret access code opens the DEV account
        # without exposing or requiring its generated password.
        if code == DEV_PLAYER_CODE:
            access_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
            if secrets.compare_digest(access_hash, DEV_ACCESS_CODE_HASH):
                print("\nDeveloper access granted.")
                return code

        if check_password(password, player["password_salt"], player["password_hash"]):
            print(f"\nWelcome back, {player['name']}!")
            return code

        print("Incorrect password.")


# ============================================================
# LEADERBOARDS
# ============================================================

# title, sort key, display text
LEADERBOARDS = [
    ("Highest Level",
     lambda p: (p.get("level", 1), p.get("xp", 0)),
     lambda p: f"Level {p.get('level', 1)}"),
    ("Most Pointys",
     lambda p: p.get("coins", 0),
     lambda p: f"{p.get('coins', 0)} pointys"),
    ("Highest Combo",
     lambda p: p.get("best_combo", 0),
     lambda p: f"{p.get('best_combo', 0)}x combo"),
    ("Best Timed Score",
     lambda p: p.get("timed_best", 0),
     lambda p: f"{p.get('timed_best', 0)} correct"),
    ("Best Memory",
     lambda p: p.get("memory_best", 0),
     lambda p: f"{p.get('memory_best', 0)} remembered"),
    ("Best Endless",
     lambda p: p.get("endless_best", 0),
     lambda p: f"{p.get('endless_best', 0)} streak"),
    ("Blackjack Profit",
     lambda p: p.get("blackjack_profit", 0),
     lambda p: f"{p.get('blackjack_profit', 0):+d} pointys"),
    ("Most Achievements",
     lambda p: len(p.get("achievements", [])),
     lambda p: f"{len(p.get('achievements', []))}/{len(ACHIEVEMENTS)}"),
]


def show_leaderboard_category(scoreboard, index):
    title, key_fn, text_fn = LEADERBOARDS[index]

    players = [
        p for p in scoreboard.values()
        if isinstance(p, dict) and not p.get("is_dev", False)
    ]

    print(f"\n========== {title.upper()} ==========")

    if not players:
        print("No players yet!")
    else:
        players.sort(key=key_fn, reverse=True)
        medals = {1: "🥇", 2: "🥈", 3: "🥉"}

        for rank, p in enumerate(players[:10], start=1):
            marker = medals.get(rank, f"{rank}.")
            print(
                f"{marker} {display_name(p)} (Lv.{p.get('level', 1)}) - "
                f"{text_fn(p)}"
            )

    print("=" * (22 + len(title)))
    input("\nPress ENTER to go back...")


def show_leaderboard(scoreboard):
    while True:
        print("\n========== LEADERBOARD ==========")

        for number, (title, _, _) in enumerate(LEADERBOARDS, start=1):
            print(f"{number}. {title}")

        print(f"{len(LEADERBOARDS) + 1}. Back")

        choice = input("\n> ").strip()

        if choice.isdigit():
            number = int(choice)

            if 1 <= number <= len(LEADERBOARDS):
                show_leaderboard_category(scoreboard, number - 1)
                continue

            if number == len(LEADERBOARDS) + 1:
                return

        print("Invalid option.")


# ============================================================
# ACHIEVEMENTS / STATS / INVENTORY SCREENS
# ============================================================

def show_achievements(player):
    print("\n=================================")
    print("          ACHIEVEMENTS")
    print("=================================")
    print(f"\nUnlocked: {len(player['achievements'])}/{len(ACHIEVEMENTS)}\n")

    for achievement_id, achievement in ACHIEVEMENTS.items():
        status = "[✓]" if achievement_id in player["achievements"] else "[ ]"
        unit = "pointys" if achievement["reward_type"] == "pointys" else "XP"

        print(f"{status} {achievement['name']}")
        print(f"    {achievement['description']}")
        print(f"    Reward: {achievement['reward']} {unit}\n")

    print("=================================")
    input("\nPress ENTER to return...")


def show_stats(player):
    total_questions = player.get("total_questions", 0)
    correct_answers = player.get("correct_answers", 0)

    accuracy = (correct_answers / total_questions * 100) if total_questions else 0

    print("\n=================================")
    print("             STATS")
    print("=================================")

    print(f"\nGames completed: {player['games']}")
    print(f"Total questions: {total_questions}")
    print(f"Correct answers: {correct_answers}")
    print(f"Wrong answers: {player.get('wrong_answers', 0)}")
    print(f"Accuracy: {accuracy:.1f}%")
    print(f"\nBest combo: {player['best_combo']}x")
    print(f"Pointys: {player['coins']}")
    print(f"Total pointys earned: {player['total_pointys_earned']}")
    print(f"Hints used: {player['hints_used']}")
    print(f"Difficulty: {player.get('difficulty', 'Normal')}")
    print(f"Prestige: {player.get('prestige', 0)} ({player.get('prestige_multiplier', 1.0):.2f}x permanent multiplier)")
    print(f"Active pet: {PET_DATA.get(player.get('active_pet'), {}).get('name', '(none)')}")

    print("\n---------- LEVEL ----------")
    print(f"Level: {player['level']}")
    print(f"XP: {xp_progress_text(player)}")

    print("\n-------- TIMED MODE --------")
    print(f"Timed games: {player['timed_games']}")
    print(f"Timed correct: {player['timed_correct']}")
    print(f"Timed best: {player['timed_best']}")

    print("\n-------- MEMORY MODE --------")
    print(f"Memory games: {player['memory_games']}")
    print(f"Memory correct: {player['memory_correct']}")
    print(f"Memory best: {player['memory_best']}")
    print(f"Memory perfect best: {player['memory_perfect_best']}")

    print("\n-------- ENDLESS MODE --------")
    print(f"Endless games: {player['endless_games']}")
    print(f"Endless total correct: {player['endless_total_correct']}")
    print(f"Endless best: {player['endless_best']}")

    print("\n-------- BLACKJACK --------")
    print(f"Blackjack hands: {player['blackjack_games']}")
    print(f"Blackjack wins: {player['blackjack_wins']}")
    print(f"Blackjack losses: {player['blackjack_losses']}")
    print(f"Blackjack pushes: {player['blackjack_pushes']}")
    print(f"Natural blackjacks: {player['blackjack_blackjacks']}")
    print(f"Double-down wins: {player['blackjack_double_down_wins']}")
    print(f"Blackjack profit: {player['blackjack_profit']:+d} pointys")

    print("\n------ EVENTS & SHOP ------")
    print(f"Random events triggered: {player['events_seen']}")
    print(f"Items bought: {player['items_bought']}")
    print(f"Pointys spent: {player['pointys_spent']}")

    print("\n------- ACHIEVEMENTS -------")
    print(f"{len(player['achievements'])}/{len(ACHIEVEMENTS)} unlocked")

    print("\n------ RECENT HISTORY ------")
    for mode, entries in player.get("history", {}).items():
        if entries:
            last = entries[-1]
            print(f"{mode.title()}: {last.get('result')} - {last.get('value')}")

    print("\n=================================")
    input("\nPress ENTER to return...")


def show_inventory(player):
    print("\n=================================")
    print("           INVENTORY")
    print("=================================")

    print("\nItems:")
    if player["inventory"]:
        for item_id, count in player["inventory"].items():
            item = SHOP_ITEMS.get(item_id)
            if item:
                print(f"  {count}x {item['name']} - {item['desc']}")
            elif item_id in EGG_DATA:
                print(f"  {count}x {EGG_DATA[item_id]['name']} ({EGG_DATA[item_id]['rarity']}) - hatch in Pets")
            elif item_id in TRADABLE_ITEMS:
                print(f"  {count}x {TRADABLE_ITEMS[item_id]['name']} - {TRADABLE_ITEMS[item_id]['desc']}")
    else:
        print("  (none)")

    print("\nUpgrades:")
    if player["upgrades"]:
        for item_id in player["upgrades"]:
            item = SHOP_ITEMS.get(item_id)
            if item:
                print(f"  {item['name']} - {item['desc']}")
    else:
        print("  (none)")

    themes = [THEMES[t]["name"] for t in player["owned_themes"] if t in THEMES]
    print("\nShop themes: " + (", ".join(themes) if themes else "(none)"))
    print("Titles: " + (", ".join(player["owned_titles"]) or "(none)"))

    input("\nPress ENTER to return...")


# ============================================================
# POINTY SHOP
# ============================================================

def owns_item(player, item_id):
    item = SHOP_ITEMS[item_id]
    kind = item["type"]

    if kind == "upgrade":
        return item_id in player["upgrades"]
    if kind == "theme":
        return item["value"] in player["owned_themes"]
    if kind == "title":
        return item["value"] in player["owned_titles"]

    return False


def buy_item(player, item_id, scoreboard):
    item = SHOP_ITEMS[item_id]

    if owns_item(player, item_id):
        print("\nYou already own that.")
        return

    if player["coins"] < item["price"]:
        print(
            f"\nNot enough pointys! {item['name']} costs {item['price']} "
            f"and you have {player['coins']}."
        )
        return

    player["coins"] -= item["price"]
    player["pointys_spent"] += item["price"]
    player["items_bought"] += 1

    kind = item["type"]

    if kind == "consumable":
        add_item(player, item_id)
    elif kind == "upgrade":
        player["upgrades"].append(item_id)
    elif kind == "theme":
        player["owned_themes"].append(item["value"])
        player["theme"] = item["value"]
    elif kind == "title":
        player["owned_titles"].append(item["value"])
        player["title"] = item["value"]

    print(color(player, f"\nBought {item['name']} for {item['price']} pointys!", "success"))

    if kind == "theme":
        print("Theme equipped. Change it any time in Settings.")
    elif kind == "title":
        print("Title equipped. Change it any time in Settings.")
    elif kind in ("consumable", "mystery"):
        print(f"You now own {inv_count(player, item_id)}.")

    save_scoreboard(scoreboard)
    check_achievements(player, scoreboard)
    save_scoreboard(scoreboard)


def shop_menu(scoreboard, player_code):
    categories = [
        ("1", "consumable", "Consumables"),
        ("2", "mystery", "Mystery Boxes"),
        ("3", "upgrade", "Permanent Upgrades"),
        ("4", "theme_title", "Themes & Titles"),
    ]

    while True:
        player = scoreboard[player_code]
        print(color(player, "\n╔════════════════════════════════╗", "title"))
        print(color(player, "║          POINTY SHOP           ║", "title"))
        print(color(player, "╚════════════════════════════════╝", "title"))
        print(f"\nYour pointys: {player['coins']}\n")
        print("1. Consumables")
        print("2. Mystery Boxes")
        print("3. Permanent Upgrades")
        print("4. Themes & Titles")
        print("5. Back")

        choice = input("\n> ").strip()
        if choice == "5":
            return
        category = next((c for c in categories if c[0] == choice), None)
        if category:
            shop_category_menu(scoreboard, player_code, category[1], category[2])
        else:
            print("Invalid option.")


def shop_category_menu(scoreboard, player_code, category, title):
    while True:
        player = scoreboard[player_code]
        print(color(player, f"\n========== {title.upper()} ==========", "title"))
        print(f"Pointys: {player['coins']}\n")

        if category == "theme_title":
            ids = [i for i, item in SHOP_ITEMS.items() if item["type"] in ("theme", "title")]
        else:
            ids = [i for i, item in SHOP_ITEMS.items() if item["type"] == category]

        if not ids:
            print("Nothing here yet.")
            input("\nPress ENTER to return...")
            return

        for number, item_id in enumerate(ids, 1):
            item = SHOP_ITEMS[item_id]
            if owns_item(player, item_id):
                tag = " [OWNED]"
            elif item["type"] in ("consumable", "mystery") and inv_count(player, item_id):
                tag = f" (you have {inv_count(player, item_id)})"
            else:
                tag = ""
            print(f"{number:>2}. {item['name']} - {item['price']} pointys{tag}")
            print(f"      {item['desc']}")

        if category == "mystery":
            print(f"\n{len(ids) + 1}. Open a Mystery Box")
            print(f"{len(ids) + 2}. Open a Lucky Mystery Box")
            print(f"{len(ids) + 3}. Back")
            back_number = len(ids) + 3
        else:
            print(f"\n{len(ids) + 1}. Back")
            back_number = len(ids) + 1

        choice = input("\n> ").strip()
        if not choice.isdigit():
            print("Invalid option.")
            continue
        number = int(choice)

        if 1 <= number <= len(ids):
            buy_item(player, ids[number - 1], scoreboard)
            continue

        if category == "mystery" and number == len(ids) + 1:
            open_mystery_box(player, scoreboard, False)
            continue
        if category == "mystery" and number == len(ids) + 2:
            open_mystery_box(player, scoreboard, True)
            continue
        if number == back_number:
            return

        print("Invalid option.")



# ============================================================
# PROGRESSION / HISTORY / PETS / SOCIAL / CUSTOM
# ============================================================

def record_history(player, mode, result, value, difficulty=None):
    history = player.setdefault("history", {})
    entries = history.setdefault(mode, [])
    entries.append({
        "time": time.strftime("%Y-%m-%d %H:%M"),
        "result": result,
        "value": value,
        "difficulty": difficulty or player.get("difficulty", "Normal"),
        "prestige": player.get("prestige", 0),
    })
    del entries[:-10]


def show_stats_history(player):
    print("\n=================================")
    print("         STATS HISTORY")
    print("=================================")
    labels = {"chord": "Chords", "timed": "Timed", "memory": "Memory", "endless": "Endless", "custom": "Custom"}
    for mode, label in labels.items():
        print(f"\n--- {label} (last 10) ---")
        entries = player.get("history", {}).get(mode, [])
        if not entries:
            print("  No runs recorded yet.")
            continue
        for e in entries[-10:]:
            print(f"  {e.get('time','?')} | {e.get('result','?')}: {e.get('value',0)} | {e.get('difficulty','Normal')}")
    input("\nPress ENTER to return...")


def difficulty_menu(scoreboard, player_code):
    player = scoreboard[player_code]
    while True:
        print("\n========== DIFFICULTY ==========")
        print(f"Current: {player.get('difficulty', 'Normal')}")
        for i, (name, data) in enumerate(DIFFICULTIES.items(), 1):
            print(f"{i}. {name} - reward x{data['reward']:.2f}")
        print(f"{len(DIFFICULTIES)+1}. Back")
        choice = input("> ").strip()
        if choice.isdigit():
            n = int(choice)
            names = list(DIFFICULTIES)
            if 1 <= n <= len(names):
                player["difficulty"] = names[n-1]
                save_scoreboard(scoreboard)
                print(f"Difficulty set to {player['difficulty']}.")
                continue
            if n == len(names) + 1:
                return
        print("Invalid option.")


def custom_mode_setup(scoreboard, player_code):
    player = scoreboard[player_code]
    print("\n========== CUSTOM MODE ==========")
    print("Choose a sequence length and how many mistakes you can make.")
    try:
        length = int(input("Sequence length (3-40): ").strip())
        lives = int(input("Mistakes allowed (0-5): ").strip())
    except ValueError:
        print("Invalid number.")
        return False
    if not 3 <= length <= 40 or not 0 <= lives <= 5:
        print("Length must be 3-40 and mistakes must be 0-5.")
        return False
    reward = min(2.5, 0.75 + length / 20 + lives * 0.10)
    player["custom_mode"] = {"length": length, "lives": lives, "reward": reward}
    save_scoreboard(scoreboard)
    print(f"Custom mode saved: length {length}, {lives} mistakes, reward x{reward:.2f}.")
    input("Press ENTER to continue...")
    return True


def custom_mode(scoreboard, player_code):
    player = scoreboard[player_code]
    cfg = player.get("custom_mode", {"length": 10, "lives": 1, "reward": 1.0})
    length, lives = cfg.get("length", 10), cfg.get("lives", 1)
    reward_mult = cfg.get("reward", 1.0) * float(player.get("prestige_multiplier", 1.0)) * (1 + pet_bonus(player, "pointy"))
    sequence = [random.choice(VERITIES) for _ in range(length)]
    banner(player, "CUSTOM MODE")
    print(f"Length: {length} | Mistakes allowed: {lives} | Reward: x{reward_mult:.2f}")
    boosts = start_boosts(player, scoreboard)
    position = 0
    mistakes = 0
    combo = 0
    input("\nPress ENTER to start...")
    while position < length:
        guess = input(f"Custom #{position+1} [{combo}x]: ").strip().lower()
        if guess == "quit":
            return
        if guess not in VERITIES:
            print("That's not so chord.")
            continue
        if guess != sequence[position]:
            mistakes += 1
            player["wrong_answers"] += 1
            player["total_questions"] += 1
            print(color(player, f"Wrong! It was {sequence[position]}.", "error"))
            if mistakes > lives:
                break
            continue
        combo += 1
        position += 1
        player["correct_answers"] += 1
        player["total_questions"] += 1
        if combo > player["best_combo"]:
            player["best_combo"] = combo
        earned = int((1 + max(0, combo - 1)) * boosts["pointy_mult"] * reward_mult)
        give_pointys(player, earned, scoreboard)
        print(color(player, f"Correct! +{earned} pointys.", "success"))
    success = position == length
    if success:
        bonus = int(10 * reward_mult)
        give_pointys(player, bonus, scoreboard)
        xp = int(15 * reward_mult)
        add_xp(player, xp, scoreboard)
        record_history(player, "custom", "Completed", position)
        print(color(player, f"\nCUSTOM COMPLETE! +{bonus} pointys, +{xp} XP", "success"))
    else:
        add_xp(player, max(1, position * 2), scoreboard)
        record_history(player, "custom", "Failed", position)
        print(f"\nCustom run ended at {position}/{length}.")
    save_scoreboard(scoreboard)
    input("Press ENTER to return...")


def pet_rarity_for_box(lucky=False):
    roll = random.random()
    if lucky:
        if roll < 0.02: return "egg_legendary"
        if roll < 0.09: return "egg_epic"
        if roll < 0.29: return "egg_rare"
        return "egg_common"
    if roll < 0.005: return "egg_legendary"
    if roll < 0.025: return "egg_epic"
    if roll < 0.10: return "egg_rare"
    return "egg_common"


def open_mystery_box(player, scoreboard, lucky=False):
    item_id = "lucky_box" if lucky else "mystery_box"
    if not remove_item(player, item_id):
        print("You don't have that box.")
        return
    roll = random.random()
    if lucky:
        pointy_chance, xp_chance, nothing_chance = 0.28, 0.25, 0.05
    else:
        pointy_chance, xp_chance, nothing_chance = 0.32, 0.24, 0.12
    if roll < pointy_chance:
        amount = random.randint(20, 90) * (2 if lucky else 1)
        give_pointys(player, amount, scoreboard)
        print(color(player, f"MYSTERY BOX: +{amount} pointys!", "success"))
    elif roll < pointy_chance + xp_chance:
        amount = random.randint(25, 100) * (2 if lucky else 1)
        add_xp(player, amount, scoreboard)
        print(color(player, f"MYSTERY BOX: +{amount} XP!", "info"))
    elif roll < pointy_chance + xp_chance + nothing_chance:
        print("MYSTERY BOX: ...nothing. The box was empty.")
    elif roll < pointy_chance + xp_chance + nothing_chance + 0.18:
        egg = pet_rarity_for_box(lucky)
        add_item(player, egg)
        print(color(player, f"MYSTERY BOX: You found a {EGG_DATA[egg]['name']}!", "accent"))
    elif roll < 0.94:
        boost = random.choice(MYSTERY_BOX_ITEMS)
        add_item(player, boost)
        print(color(player, f"MYSTERY BOX: You got a {SHOP_ITEMS[boost]['name']}!", "success"))
    else:
        tradable = random.choices(list(TRADABLE_ITEMS), weights=[65, 25, 10])[0]
        add_item(player, tradable)
        print(color(player, f"MYSTERY BOX: You found a {TRADABLE_ITEMS[tradable]['name']}!", "accent"))
    save_scoreboard(scoreboard)


def hatch_egg(player, scoreboard):
    eggs = [i for i in player["inventory"] if i in EGG_DATA and inv_count(player, i) > 0]
    if not eggs:
        print("You don't have any eggs.")
        return
    print("\nEggs:")
    for i, egg in enumerate(eggs, 1):
        print(f"{i}. {EGG_DATA[egg]['name']} ({inv_count(player, egg)})")
    choice = input("> ").strip()
    if not choice.isdigit() or not 1 <= int(choice) <= len(eggs):
        return
    egg = eggs[int(choice)-1]
    remove_item(player, egg)
    data = EGG_DATA[egg]
    pet = random.choices(list(data["weights"]), weights=list(data["weights"].values()))[0]
    if pet not in player["pets"]:
        player["pets"].append(pet)
    player["active_pet"] = pet
    print(color(player, f"\nHATCHED: {data['name']} -> {PET_DATA[pet]['name']} ({PET_DATA[pet]['rarity']})!", "success"))
    print("The pet has been equipped.")
    save_scoreboard(scoreboard)
    input("Press ENTER to continue...")


def pet_menu(scoreboard, player_code):
    player = scoreboard[player_code]
    while True:
        print("\n========== PETS ==========")
        print(f"Active: {PET_DATA.get(player.get('active_pet'), {}).get('name', '(none)')}")
        print("1. Hatch an egg")
        print("2. Equip a pet")
        print("3. View collection")
        print("4. Back")
        choice = input("> ").strip()
        if choice == "1":
            hatch_egg(player, scoreboard)
        elif choice == "2":
            if not player["pets"]:
                print("You don't own any pets.")
                continue
            for i, pet in enumerate(player["pets"], 1):
                print(f"{i}. {PET_DATA[pet]['name']} ({PET_DATA[pet]['rarity']})")
            n = input("> ").strip()
            if n.isdigit() and 1 <= int(n) <= len(player["pets"]):
                player["active_pet"] = player["pets"][int(n)-1]
                save_scoreboard(scoreboard)
                print("Pet equipped.")
        elif choice == "3":
            for pet in player["pets"]:
                d = PET_DATA[pet]
                print(f"- {d['name']} [{d['rarity']}] | pointys +{d['pointy']*100:.0f}% | XP +{d['xp']*100:.0f}% | event luck +{d['event']*100:.0f}%")
            input("Press ENTER to continue...")
        elif choice == "4":
            return
        else:
            print("Invalid option.")


def social_menu(scoreboard, player_code):
    player = scoreboard[player_code]
    while True:
        print("\n========== GIFTING & TRADING ==========")
        print("1. Gift pointys")
        print("2. Gift an item")
        print("3. Trade with a player")
        print("4. Back")
        choice = input("> ").strip()
        if choice == "4":
            return
        if choice not in ("1", "2", "3"):
            print("Invalid option.")
            continue
        target_code = input("Target player code: ").strip().upper()
        if target_code not in scoreboard or target_code == player_code:
            print("That player code is invalid.")
            continue
        target = scoreboard[target_code]
        if choice == "1":
            try: amount = int(input("Pointys to gift: ").strip())
            except ValueError: print("Invalid amount."); continue
            if amount <= 0 or amount > player["coins"]:
                print("You don't have that many pointys."); continue
            player["coins"] -= amount
            target["coins"] += amount
            print(f"Gifted {amount} pointys to {target['name']}.")
        elif choice == "2":
            item = input("Item ID to gift: ").strip()
            if inv_count(player, item) <= 0 or (item not in SHOP_ITEMS and item not in EGG_DATA and item not in TRADABLE_ITEMS):
                print("You don't have that item."); continue
            remove_item(player, item); add_item(target, item)
            print(f"Gifted {item} to {target['name']}.")
        else:
            print("Your tradable/owned items:")
            my_items = [i for i,c in player["inventory"].items() if c > 0 and (i in TRADABLE_ITEMS or i in EGG_DATA)]
            their_items = [i for i,c in target["inventory"].items() if c > 0 and (i in TRADABLE_ITEMS or i in EGG_DATA)]
            if not my_items or not their_items:
                print("Both players need at least one tradable item."); continue
            print("You: " + ", ".join(my_items)); print(f"{target['name']}: " + ", ".join(their_items))
            mine = input("Your item: ").strip(); theirs = input("Their item: ").strip()
            if mine not in my_items or theirs not in their_items:
                print("Invalid trade."); continue
            confirm = input(f"Trade {mine} for {theirs}? Type TRADE: ").strip().upper()
            if confirm != "TRADE":
                print("Trade cancelled."); continue
            remove_item(player, mine); remove_item(target, theirs)
            add_item(player, theirs); add_item(target, mine)
            print("Trade completed.")
        save_scoreboard(scoreboard)


def poker_hand_rank(hand):
    values = sorted([card[0] for card in hand], reverse=True)
    suits = [card[1] for card in hand]
    counts = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1

    unique = sorted(set(values), reverse=True)
    straight_high = None
    if 14 in unique:
        unique.append(1)
    for i in range(len(unique) - 4):
        window = unique[i:i + 5]
        if window[0] - window[4] == 4 and len(set(window)) == 5:
            straight_high = window[0]
            break

    flush = len(set(suits)) == 1
    if flush and straight_high:
        return (8 if straight_high != 14 else 9, straight_high)

    groups = sorted(((count, value) for value, count in counts.items()), reverse=True)
    if groups[0][0] == 4:
        quad = groups[0][1]
        kicker = max(v for v in values if v != quad)
        return (7, quad, kicker)

    triples = sorted([v for v, c in counts.items() if c == 3], reverse=True)
    pairs = sorted([v for v, c in counts.items() if c == 2], reverse=True)
    if triples and (len(triples) >= 2 or pairs):
        pair = triples[1] if len(triples) >= 2 else pairs[0]
        return (6, triples[0], pair)

    if flush:
        return (5, *values)
    if straight_high:
        return (4, straight_high)
    if triples:
        kickers = sorted([v for v in values if v != triples[0]], reverse=True)
        return (3, triples[0], *kickers)
    if len(pairs) >= 2:
        kicker = max(v for v in values if v not in pairs[:2])
        return (2, pairs[0], pairs[1], kicker)
    if len(pairs) == 1:
        kickers = sorted([v for v in values if v != pairs[0]], reverse=True)
        return (1, pairs[0], *kickers)
    return (0, *values)


def poker_hand_name(rank):
    return ["High Card", "Pair", "Two Pair", "Three of a Kind", "Straight",
            "Flush", "Full House", "Four of a Kind", "Straight Flush", "Royal Flush"][rank[0]]


def poker_card_text(card):
    faces = {14: "A", 13: "K", 12: "Q", 11: "J"}
    return f"{faces.get(card[0], str(card[0]))}{card[1]}"


def poker_mode(scoreboard, player_code):
    player = scoreboard[player_code]
    payouts = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 8, 7: 15, 8: 25, 9: 50}
    suits = ["♠", "♥", "♦", "♣"]

    while True:
        bet = casino_bet(player)
        if bet == 0:
            return

        deck = [(value, suit) for value in range(2, 15) for suit in suits]
        random.shuffle(deck)
        hand = [deck.pop() for _ in range(5)]
        dealer = [deck.pop() for _ in range(5)]

        print("\nYour hand:", " ".join(poker_card_text(c) for c in hand))
        print("You have one redraw phase. Enter card numbers to replace, e.g. 1 3 5.")
        print("Press ENTER to keep all five cards.")
        redraw = input("> ").strip()

        if redraw:
            try:
                indexes = sorted(set(int(x) - 1 for x in redraw.split()))
                if any(i < 0 or i >= 5 for i in indexes) or len(indexes) > 3:
                    raise ValueError
                for i in indexes:
                    hand[i] = deck.pop()
            except ValueError:
                print("Invalid redraw. Your original hand is kept.")

        player_rank = poker_hand_rank(hand)
        dealer_rank = poker_hand_rank(dealer)
        player_name = poker_hand_name(player_rank)
        dealer_name = poker_hand_name(dealer_rank)

        player["coins"] -= bet
        if player_rank > dealer_rank:
            profit = bet * payouts[player_rank[0]]
            result = f"You win with {player_name}!"
        elif player_rank == dealer_rank:
            profit = 0
            player["coins"] += bet
            result = f"Tie! Both have {player_name}."
        else:
            profit = -bet
            result = f"Dealer wins with {dealer_name}."

        if profit != 0:
            finish_casino(player, scoreboard, profit)
        else:
            player["casino_games"] += 1
            save_scoreboard(scoreboard)

        print("\nYour hand:   ", " ".join(poker_card_text(c) for c in hand))
        print("Dealer hand: ", " ".join(poker_card_text(c) for c in dealer))
        print(f"Your hand: {player_name} | Dealer: {dealer_name}")
        print(result)
        if profit > 0:
            print(f"+{profit} pointys")
        elif profit < 0:
            print(f"-{bet} pointys")
        else:
            print("Your bet was returned.")
        print(f"Pointys: {player['coins']}")

def casino_menu(scoreboard, player_code):
    player = scoreboard[player_code]
    while True:
        print("\n========== CASINO ==========")
        print(f"Pointys: {player['coins']}")
        print("1. Blackjack")
        print("2. Poker")
        print("3. Coin Flip")
        print("4. Roulette")
        print("5. Slots")
        print("6. Back")
        choice = input("> ").strip()
        if choice == "1": blackjack_mode(scoreboard, player_code)
        elif choice == "2": poker_mode(scoreboard, player_code)
        elif choice == "3": coin_flip_game(scoreboard, player_code)
        elif choice == "4": roulette_game(scoreboard, player_code)
        elif choice == "5": slots_game(scoreboard, player_code)
        elif choice == "6": return
        else: print("Invalid option.")


def casino_bet(player):
    try: bet = int(input("Bet (or 0 to leave): ").strip())
    except ValueError: return 0
    if bet < 0 or bet > player["coins"]:
        print("Invalid bet."); return 0
    return bet


def finish_casino(player, scoreboard, profit):
    player["casino_games"] += 1
    if profit > 0:
        player["casino_wins"] += 1
        give_pointys(player, profit, scoreboard)
    else:
        player["coins"] += profit
    player["casino_profit"] += profit
    save_scoreboard(scoreboard)


def coin_flip_game(scoreboard, player_code):
    player = scoreboard[player_code]
    while True:
        bet = casino_bet(player)
        if bet == 0: return
        pick = input("Heads or tails? ").strip().lower()
        if pick not in ("heads", "tails"): print("Pick heads or tails."); continue
        result = random.choice(("heads", "tails"))
        player["coins"] -= bet
        profit = bet if pick == result else -bet
        finish_casino(player, scoreboard, profit)
        print(f"It was {result}. {'You win!' if profit > 0 else 'You lose.'}")
        print(f"Pointys: {player['coins']}")


def roulette_game(scoreboard, player_code):
    player = scoreboard[player_code]
    while True:
        bet = casino_bet(player)
        if bet == 0: return
        print("1. Red/Black (2x)  2. Odd/Even (2x)  3. Number (36x)")
        kind = input("> ").strip()
        player["coins"] -= bet
        n = random.randint(0, 36)
        if kind == "1":
            pick = input("Red or black? ").strip().lower()
            actual = "red" if n != 0 and n % 2 else "black"
            profit = bet if pick == actual else -bet
        elif kind == "2":
            pick = input("Odd or even? ").strip().lower()
            actual = "odd" if n % 2 else "even"
            profit = bet if n != 0 and pick == actual else -bet
        elif kind == "3":
            try: pick = int(input("Number 0-36: ").strip())
            except ValueError: pick = -1
            profit = bet * 35 if pick == n else -bet
        else:
            player["coins"] += bet
            print("Invalid bet type."); continue
        finish_casino(player, scoreboard, profit)
        print(f"Roulette landed on {n}. {'You win!' if profit > 0 else 'You lose.'} Net: {profit:+d}")


def slots_game(scoreboard, player_code):
    player = scoreboard[player_code]
    symbols = ["7", "★", "●", "◆", "☘"]
    while True:
        bet = casino_bet(player)
        if bet == 0: return
        reels = [random.choice(symbols) for _ in range(3)]
        player["coins"] -= bet
        if reels[0] == reels[1] == reels[2]: profit = bet * (10 if reels[0] == "7" else 5)
        elif len(set(reels)) == 2: profit = bet * 2
        else: profit = -bet
        finish_casino(player, scoreboard, profit)
        print(" | ".join(reels), f"=> {profit:+d} pointys")

# ============================================================
# SETTINGS
# ============================================================

def reset_statistics(scoreboard, player_code):
    player = scoreboard[player_code]

    print("\n========== RESET STATISTICS ==========")
    print("This will reset:")
    print("- Pointys, lifetime pointys, games, best combo")
    print("- XP and level")
    print("- Achievements and all statistics")
    print("- All mode records (Timed, Memory, Endless, Blackjack)")
    print("- Shop items and permanent upgrades")
    print("\nYour username, player code, password, theme,")
    print("and any purchased themes/titles will remain.")

    confirm = input("\nType RESET to continue: ").strip()

    if confirm != "RESET":
        print("Reset cancelled.")
        return

    keep = {
        key: player.get(key)
        for key in ("theme", "owned_themes", "owned_titles", "title")
    }

    fresh = create_default_player_data(
        player["name"], player["password_salt"], player["password_hash"]
    )
    fresh.update(keep)

    scoreboard[player_code] = fresh
    save_scoreboard(scoreboard)

    print("\nStatistics successfully reset.")
    input("\nPress ENTER to continue...")


def change_username(scoreboard, player_code):
    player = scoreboard[player_code]

    print("\n========== CHANGE USERNAME ==========")
    print(f"Current username: {player['name']}")

    new_name = input("New username: ").strip()

    if not new_name:
        print("Username cannot be empty.")
        return

    player["name"] = new_name
    save_scoreboard(scoreboard)

    print(f"\nUsername changed to {new_name}.")
    input("\nPress ENTER to continue...")


def change_theme(scoreboard, player_code):
    player = scoreboard[player_code]

    while True:
        print("\n========== COLOR / THEME ==========")

        available = FREE_THEMES + [
            t for t in player["owned_themes"] if t in THEMES
        ]

        for index, theme_name in enumerate(available, start=1):
            print(color(player, f"{index}. {THEMES[theme_name]['name']}", "text"))

        print(f"{len(available) + 1}. Back")

        choice = input("\n> ").strip()

        if choice.isdigit():
            number = int(choice)

            if 1 <= number <= len(available):
                selected = available[number - 1]
                player["theme"] = selected
                save_scoreboard(scoreboard)

                print(color(
                    player, f"\nTheme changed to {THEMES[selected]['name']}.",
                    "success"
                ))
                continue

            if number == len(available) + 1:
                return

        print("Invalid option.")


def change_title(scoreboard, player_code):
    player = scoreboard[player_code]

    print("\n========== CHOOSE TITLE ==========")

    if not player["owned_titles"]:
        print("You don't own any titles yet. Buy some in the Pointy Shop!")
        input("\nPress ENTER to continue...")
        return

    options = ["(no title)"] + player["owned_titles"]

    for index, title in enumerate(options, start=1):
        marker = " *" if (title == player["title"] or
                          (index == 1 and not player["title"])) else ""
        print(f"{index}. {title}{marker}")

    print(f"{len(options) + 1}. Back")

    choice = input("\n> ").strip()

    if choice.isdigit():
        number = int(choice)

        if 1 <= number <= len(options):
            player["title"] = "" if number == 1 else options[number - 1]
            save_scoreboard(scoreboard)
            print("\nTitle updated.")


def settings_menu(scoreboard, player_code):
    while True:
        player = scoreboard[player_code]

        print(color(player, "\n=================================", "title"))
        print(color(player, "            SETTINGS", "title"))
        print(color(player, "=================================", "title"))

        print(f"\nCurrent theme: {get_theme(player)['name']}")
        print(f"Username: {player['name']}")
        print(f"Title: {player['title'] or '(none)'}")

        print("\n1. Color / theme")
        print("2. Change username")
        print("3. Choose title")
        print("4. Reset statistics")
        print("5. Back")

        choice = input("\n> ").strip()

        if choice == "1":
            change_theme(scoreboard, player_code)
        elif choice == "2":
            change_username(scoreboard, player_code)
        elif choice == "3":
            change_title(scoreboard, player_code)
        elif choice == "4":
            reset_statistics(scoreboard, player_code)
        elif choice == "5":
            return
        else:
            print("Invalid option.")


# ============================================================
# NORMAL GAME
# ============================================================

PRAISE = ["Perity", "It was {g}", "Great job - chord"]


def play_game(scoreboard, player_code):
    player = scoreboard[player_code]

    length = random.randint(*difficulty_data(player)["normal_len"])
    sequence = [random.choice(VERITIES) for _ in range(length)]

    position = 0
    combo = 0
    wrong_in_game = 0

    banner(player, "CHORDS GAME")

    print(f"Player: {display_name(player)} (Lv.{player['level']})")
    print(f"Pointys: {player['coins']}")
    print(f"Sequence length: {length}")

    boosts = start_boosts(player, scoreboard)

    print("\nGuess them in order.")
    print("Commands: hint | leaderboard | quit\n")

    event = None
    attempts = None
    new_round = True

    while position < length:
        if new_round:
            event = roll_event(player, boosts)
            attempts = 3 if event and event.get("guesses") else None
            new_round = False

        extra = f" | {attempts} guesses" if attempts else ""

        guess = input(
            f"Chords #{position + 1} "
            f"[{player['coins']} pointys | {combo}x combo{extra}]: "
        ).strip().lower()

        if guess == "quit":
            print("\nYou left the game.")
            print("The sequence was:", ", ".join(sequence))
            save_scoreboard(scoreboard)
            return

        if guess == "leaderboard":
            show_leaderboard(scoreboard)
            continue

        if guess == "hint":
            if inv_count(player, "hint_token") > 0:
                remove_item(player, "hint_token")
                player["hints_used"] += 1
                print(f"Hint: the first letter is '{sequence[position][0].upper()}'.")
                print(f"Hint Token used. {inv_count(player, 'hint_token')} left.")
                save_scoreboard(scoreboard)

            elif player["coins"] < 5:
                print(
                    f"You need 5 pointys (or a Hint Token) for a hint. "
                    f"You only have {player['coins']}."
                )

            else:
                player["coins"] -= 5
                player["hints_used"] += 1
                print(f"Hint: the first letter is '{sequence[position][0].upper()}'.")
                print(f"5 pointys spent. You now have {player['coins']}.")
                save_scoreboard(scoreboard)

            continue

        if guess not in VERITIES:
            print("That's not so chord")
            continue

        if guess != sequence[position]:
            print(random.choice([
                f"Stawppp, it's not {guess}",
                f"It's not {guess}",
            ]))

            wrong_in_game += 1
            player["wrong_answers"] += 1
            player["total_questions"] += 1

            if attempts is not None:
                attempts -= 1

                if attempts > 0:
                    print(color(
                        player,
                        f"{attempts} free guess(es) left - your combo is safe!",
                        "info"
                    ))
                    save_scoreboard(scoreboard)
                    continue

                attempts = None
                print(color(player, "Out of free guesses!", "error"))

            combo = handle_miss(player, scoreboard, combo)
            save_scoreboard(scoreboard)
            continue

        # ---- correct answer ----
        combo += 1

        player["correct_answers"] += 1
        player["total_questions"] += 1

        print(random.choice(PRAISE).format(g=guess))

        base = combo - 1 if combo >= 2 else 0
        earned = pointy_reward(base, event, boosts, player)

        if earned > 0:
            give_pointys(player, earned, scoreboard)

            if combo >= 2:
                print(f"{combo}x COMBO! +{earned} pointys!")
            else:
                print(f"+{earned} pointys!")

        claim_event_xp(player, event, scoreboard)

        if combo > player["best_combo"]:
            player["best_combo"] = combo

        position += 1
        new_round = True
        event = None
        attempts = None

        check_achievements(player, scoreboard)
        save_scoreboard(scoreboard)

    bonus = 3 * boosts["pointy_mult"] + magnet_bonus(player)
    give_pointys(player, bonus, scoreboard)

    player["games"] += 1

    xp_gain = 10 * boosts["xp_mult"]
    add_xp(player, xp_gain, scoreboard)

    perfect_game = wrong_in_game == 0
    record_history(player, "chord", "Perfect" if perfect_game else "Completed", length)

    check_achievements(player, scoreboard, perfect_game)
    save_scoreboard(scoreboard)

    banner(player, "GAME COMPLETED!", "success")

    print("The sequence was:", ", ".join(sequence))
    print(f"\nCompletion bonus: +{bonus} pointys!")
    print(f"+{xp_gain} XP!")

    if perfect_game:
        print(color(player, "Perfect game!", "accent"))

    print(f"\nTotal pointys: {player['coins']}")
    print(f"Best combo: {player['best_combo']}x")

    input("\nPress ENTER to return to the lobby...")


# ============================================================
# TIMED MODE
# ============================================================

def timed_mode(scoreboard, player_code):
    player = scoreboard[player_code]

    banner(player, "60 SECOND MODE")

    print("\nType as many correct verities as possible.")
    print("Wrong answers reset your combo.")

    boosts = start_boosts(player, scoreboard, timed=True)
    total_seconds = difficulty_data(player)["timed"] + boosts["extra_seconds"]

    print(f"\nYou have {total_seconds} seconds.")
    input("\nPress ENTER to start...")

    start_time = time.monotonic()

    correct = 0
    wrong = 0
    combo = 0
    best_combo = 0
    running_pointys = 0
    event_xp = 0
    time_up = False

    while not time_up:
        if total_seconds - (time.monotonic() - start_time) <= 0:
            break

        target = random.choice(VERITIES)
        event = roll_event(player, boosts)
        attempts = 3 if event and event.get("guesses") else 1
        solved = False

        while attempts > 0:
            remaining = total_seconds - (time.monotonic() - start_time)

            if remaining <= 0:
                time_up = True
                break

            extra = f" | {attempts} guesses left" if attempts > 1 else ""
            print(f"\n[{max(0, remaining):.1f}s] {combo}x combo{extra}")

            guess = input("Chords: ").strip().lower()

            if time.monotonic() - start_time >= total_seconds:
                time_up = True
                break

            if guess == "quit":
                print("\nTimed game cancelled.")
                return

            attempts -= 1

            if guess == target:
                discover_chord(player, target, scoreboard)
                solved = True
                break

            wrong += 1
            player["wrong_answers"] += 1
            player["total_questions"] += 1

            if guess not in VERITIES:
                print("That's not so chord.")
            elif attempts > 0:
                print(random.choice(["Nope!", "Stawppp!", "Wrongity!"]))
            else:
                print(random.choice([
                    "Nope!", "Stawppp!", f"It was {target}!", "Wrongity!"
                ]))

            if attempts > 0:
                print(color(player, f"{attempts} guess(es) left - combo is safe!", "info"))

        if solved:
            correct += 1
            combo += 1

            player["correct_answers"] += 1
            player["total_questions"] += 1

            best_combo = max(best_combo, combo)

            print(random.choice([
                "Perity!", "Nice!", "Great job - chord!", "It was correct!"
            ]))

            earned = pointy_reward(combo - 1 if combo >= 2 else 0, event, boosts, player)

            if earned > 0:
                give_pointys(player, earned, scoreboard)
                running_pointys += earned

                if combo >= 2:
                    print(f"{combo}x COMBO! +{earned} pointys!")
                else:
                    print(f"+{earned} pointys!")

            if event and event.get("xp"):
                event_xp += event["xp"]
                print(color(player, f"+{event['xp']} bonus XP!", "info"))

        elif time_up:
            break

        else:
            combo = handle_miss(player, scoreboard, combo)

    player["timed_games"] += 1
    player["timed_correct"] += correct

    if correct > player["timed_best"]:
        player["timed_best"] = correct

    end_bonus = correct * boosts["pointy_mult"] + magnet_bonus(player)
    give_pointys(player, end_bonus, scoreboard)

    xp_earned = correct * 2 * boosts["xp_mult"] + event_xp
    add_xp(player, xp_earned, scoreboard)

    if best_combo > player["best_combo"]:
        player["best_combo"] = best_combo

    record_history(player, "timed", "Completed", correct)
    check_achievements(player, scoreboard)
    save_scoreboard(scoreboard)

    banner(player, "TIME'S UP!", "accent")

    print(f"\nCorrect: {correct}")
    print(f"Wrong: {wrong}")
    print(f"Best combo: {best_combo}x")
    print(f"+{end_bonus + running_pointys} pointys")
    print(f"+{xp_earned} XP")
    print(f"\nTimed personal best: {player['timed_best']}")

    input("\nPress ENTER to return to the lobby...")


# ============================================================
# MEMORY MODE
# ============================================================

def memory_mode(scoreboard, player_code):
    player = scoreboard[player_code]

    length = random.randint(*difficulty_data(player)["memory_len"])
    sequence = [random.choice(VERITIES) for _ in range(length)]

    banner(player, "MEMORY MODE")

    print("\nRemember the following sequence.")
    print(f"Length: {length}")

    boosts = start_boosts(player, scoreboard)
    event = roll_event(player, boosts)
    lives = 3 if event and event.get("guesses") else 1

    input("\nPress ENTER to reveal the sequence...")

    print("\n")
    print(color(player, "  " + "  ".join(sequence), "accent"))

    input("\nPress ENTER when you are ready...")

    print("\n" * 40)
    print("Now reproduce the sequence.")
    print("Enter one chord at a time.")

    if inv_count(player, "memory_peek"):
        print(f"Type peek to look again ({inv_count(player, 'memory_peek')} Memory Peek).")

    if lives > 1:
        print(color(player, f"You can make up to {lives - 1} mistakes!", "info"))

    correct = 0
    position = 0

    while position < length:
        guess = input(f"\nMemory #{position + 1}: ").strip().lower()

        if guess == "quit":
            print("\nMemory game cancelled.")
            return

        if guess == "peek":
            if remove_item(player, "memory_peek"):
                save_scoreboard(scoreboard)
                print(color(player, "  " + "  ".join(sequence), "accent"))
            else:
                print("You don't have a Memory Peek.")
            continue

        if guess == sequence[position]:
            correct += 1
            player["correct_answers"] += 1
            player["total_questions"] += 1
            player["memory_correct"] += 1

            print(color(player, "Correct!", "success"))
            position += 1
            continue

        if guess not in VERITIES:
            print("That's not so chord.")

        print(color(player, f"Wrong! It was {sequence[position]}.", "error"))

        player["wrong_answers"] += 1
        player["total_questions"] += 1

        lives -= 1

        if lives <= 0:
            break

        print(color(player, f"{lives - 1} mistake(s) left to spare.", "info")
              if lives > 1 else
              color(player, "That was your last spare life!", "info"))

        position += 1

    player["memory_games"] += 1

    if correct > player["memory_best"]:
        player["memory_best"] = correct

    perfect = correct == length

    if perfect and length > player["memory_perfect_best"]:
        player["memory_perfect_best"] = length

    base = correct * 2

    if perfect:
        base += length
        print(color(player, "\nPERFECT MEMORY!", "accent"))

    pointys_earned = pointy_reward(base, event, boosts, player) + magnet_bonus(player)
    give_pointys(player, pointys_earned, scoreboard)

    xp_earned = correct * 3 * boosts["xp_mult"]
    add_xp(player, xp_earned, scoreboard)
    record_history(player, "memory", "Perfect" if perfect else "Completed", correct)
    claim_event_xp(player, event, scoreboard)

    check_achievements(player, scoreboard)
    save_scoreboard(scoreboard)

    banner(player, "MEMORY COMPLETE!", "success")

    print(f"\nSequence length: {length}")
    print(f"Correct: {correct}/{length}")
    print(f"+{pointys_earned} pointys")
    print(f"+{xp_earned} XP")
    print(f"Memory best: {player['memory_best']}")
    print("\nThe sequence was:")
    print(", ".join(sequence))

    input("\nPress ENTER to return to the lobby...")


# ============================================================
# ENDLESS MODE
# ============================================================

def endless_mode(scoreboard, player_code):
    player = scoreboard[player_code]

    banner(player, "ENDLESS MODE")

    print("\nKeep guessing until you get one wrong.")
    print("The longer your streak, the more pointys you earn.")
    print("Type quit to leave before answering.")

    boosts = start_boosts(player, scoreboard)

    input("\nPress ENTER to start...")

    correct = 0
    combo = 0
    pointys_earned = 0
    event_xp = 0

    while True:
        target = random.choice(VERITIES)
        event = roll_event(player, boosts)
        attempts = 3 if event and event.get("guesses") else 1
        solved = False

        while attempts > 0:
            extra = f" | {attempts} guesses" if attempts > 1 else ""

            print(
                f"\nQuestion #{correct + 1} | {combo}x combo | "
                f"{player['coins']} pointys{extra}"
            )

            guess = input("Chords: ").strip().lower()

            if guess == "quit":
                print("\nYou left the endless run.")
                return

            if guess not in VERITIES:
                print("That's not so chord.")
                continue

            attempts -= 1

            if guess == target:
                discover_chord(player, target, scoreboard)
                solved = True
                break

            player["wrong_answers"] += 1
            player["total_questions"] += 1

            if attempts > 0:
                print(color(player, f"Wrong! {attempts} guess(es) left.", "error"))

        if solved:
            correct += 1
            combo += 1

            player["correct_answers"] += 1
            player["total_questions"] += 1

            reward = pointy_reward(1 + (combo - 1 if combo >= 2 else 0), event, boosts, player)

            give_pointys(player, reward, scoreboard)
            pointys_earned += reward

            print(color(player, f"Correct! +{reward} pointys!", "success"))

            if event and event.get("xp"):
                event_xp += event["xp"]
                print(color(player, f"+{event['xp']} bonus XP!", "info"))

            if combo > player["best_combo"]:
                player["best_combo"] = combo

            check_achievements(player, scoreboard)
            save_scoreboard(scoreboard)
            continue

        # Out of guesses
        if try_shield(player, scoreboard):
            print(f"The answer was {target}. Your run continues!")
            continue

        print(color(player, "\nWRONG!", "error"))
        print(f"The answer was: {target}")
        break

    player["endless_games"] += 1
    player["endless_total_correct"] += correct

    if correct > player["endless_best"]:
        player["endless_best"] = correct

    bonus = magnet_bonus(player)
    give_pointys(player, bonus, scoreboard)
    pointys_earned += bonus

    xp_earned = correct * 2 * boosts["xp_mult"] + event_xp
    add_xp(player, xp_earned, scoreboard)
    record_history(player, "endless", "Run over", correct)

    check_achievements(player, scoreboard)
    save_scoreboard(scoreboard)

    banner(player, "ENDLESS RUN OVER", "accent")

    print(f"\nCorrect answers: {correct}")
    print(f"Final combo: {combo}x")
    print(f"Pointys earned: +{pointys_earned}")
    print(f"XP earned: +{xp_earned}")
    print(f"Endless personal best: {player['endless_best']}")

    input("\nPress ENTER to return to the lobby...")


# ============================================================
# BLACKJACK
# ============================================================

def create_deck():
    suits = ["♠", "♥", "♦", "♣"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    deck = [(rank, suit) for suit in suits for rank in ranks]
    random.shuffle(deck)

    return deck


def card_text(card):
    rank, suit = card
    return f"{rank}{suit}"


def hand_text(hand):
    return " ".join(card_text(card) for card in hand)


def hand_value(hand):
    value = 0
    aces = 0

    for rank, suit in hand:
        if rank in ["J", "Q", "K"]:
            value += 10
        elif rank == "A":
            value += 11
            aces += 1
        else:
            value += int(rank)

    while value > 21 and aces > 0:
        value -= 10
        aces -= 1

    return value


def is_blackjack(hand):
    return len(hand) == 2 and hand_value(hand) == 21


def show_blackjack_hand(player, player_hand, dealer_hand, hide_dealer=True):
    print(color(player, "\n---------------------------------", "title"))
    print("Dealer:")

    if hide_dealer:
        print(f"[?] {card_text(dealer_hand[1])}")
        print("Value: ?")
    else:
        print(hand_text(dealer_hand))
        print(f"Value: {hand_value(dealer_hand)}")

    print("\nYou:")
    print(hand_text(player_hand))
    print(f"Value: {hand_value(player_hand)}")
    print("---------------------------------")


def blackjack_play_again():
    again = input(
        "\nPress ENTER to play again, or type quit to leave: "
    ).strip().lower()

    return again != "quit"


def blackjack_mode(scoreboard, player_code):
    player = scoreboard[player_code]

    banner(player, "BLACKJACK")

    print("\nRules:")
    print("- Get as close to 21 as possible.")
    print("- J, Q and K are worth 10.")
    print("- A is worth 1 or 11.")
    print("- Dealer stands on 17.")
    print("- Natural blackjack pays 3:2.")
    print("- A tie is a push.")
    print("- Double doubles your bet and gives one extra card.")

    while True:
        print(f"\nPointys: {player['coins']}")

        if player["coins"] <= 0:
            print("\nYou don't have any pointys to bet.")
            input("\nPress ENTER to return...")
            return

        bet_input = input("\nBet amount (or quit): ").strip().lower()

        if bet_input == "quit":
            return

        if not bet_input.isdigit():
            print("Enter a valid number.")
            continue

        bet = int(bet_input)

        if bet <= 0:
            print("Your bet must be at least 1 pointy.")
            continue

        if bet > player["coins"]:
            print(f"You only have {player['coins']} pointys.")
            continue

        deck = create_deck()
        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]

        player["blackjack_games"] += 1
        unlock_achievement(player, "blackjack_first", scoreboard)
        save_scoreboard(scoreboard)

        print(color(player, f"\nBET: {bet} pointys", "accent"))
        show_blackjack_hand(player, player_hand, dealer_hand, True)

        player_bj = is_blackjack(player_hand)
        dealer_bj = is_blackjack(dealer_hand)

        # ---------------- natural blackjack ----------------
        if player_bj or dealer_bj:
            show_blackjack_hand(player, player_hand, dealer_hand, False)

            if player_bj and dealer_bj:
                player["blackjack_pushes"] += 1
                print(color(player, "\nBoth have blackjack. PUSH!", "accent"))
                print("Your bet is returned.")

            elif player_bj:
                player["blackjack_wins"] += 1
                player["blackjack_blackjacks"] += 1

                profit = (bet * 3) // 2
                give_pointys(player, profit, scoreboard)
                player["blackjack_profit"] += profit

                print(color(player, "\nBLACKJACK!", "success"))
                print(f"+{profit} pointys!")

                unlock_achievement(player, "blackjack_blackjack", scoreboard)

            else:
                player["blackjack_losses"] += 1
                player["coins"] -= bet
                player["blackjack_profit"] -= bet

                print(color(player, "\nDealer has blackjack.", "error"))
                print(f"-{bet} pointys.")

            check_achievements(player, scoreboard)
            save_scoreboard(scoreboard)

            if not blackjack_play_again():
                return

            continue

        # ---------------- player turn ----------------
        doubled = False

        while True:
            if hand_value(player_hand) > 21:
                break

            print("\n1. Hit")
            print("2. Stand")

            can_double = len(player_hand) == 2 and player["coins"] >= bet * 2

            if can_double:
                print("3. Double")

            choice = input("> ").strip()

            if choice == "1":
                player_hand.append(deck.pop())
                show_blackjack_hand(player, player_hand, dealer_hand, True)

                if hand_value(player_hand) > 21:
                    print(color(player, "\nBUST!", "error"))

                continue

            if choice == "2":
                break

            if choice == "3" and can_double:
                bet *= 2
                doubled = True

                print(color(player, f"\nBET DOUBLED TO {bet} POINTYS!", "accent"))

                player_hand.append(deck.pop())
                show_blackjack_hand(player, player_hand, dealer_hand, True)

                if hand_value(player_hand) > 21:
                    print(color(player, "\nBUST!", "error"))

                break

            print("Invalid choice.")

        # ---------------- player bust ----------------
        if hand_value(player_hand) > 21:
            player["blackjack_losses"] += 1
            player["coins"] -= bet
            player["blackjack_profit"] -= bet

            print(f"You lose {bet} pointys.")

            check_achievements(player, scoreboard)
            save_scoreboard(scoreboard)

            if not blackjack_play_again():
                return

            continue

        # ---------------- dealer turn ----------------
        print(color(player, "\nDealer's turn...", "accent"))
        time.sleep(1.2)

        show_blackjack_hand(player, player_hand, dealer_hand, False)

        while hand_value(dealer_hand) < 17:
            time.sleep(1.2)
            dealer_hand.append(deck.pop())

            print("\nDealer draws...")
            time.sleep(0.8)

            print("Dealer:", hand_text(dealer_hand))
            print(f"Dealer value: {hand_value(dealer_hand)}")

        time.sleep(1.0)

        # ---------------- result ----------------
        player_value = hand_value(player_hand)
        dealer_value = hand_value(dealer_hand)

        print("\n=================================")
        print("Your hand:", hand_text(player_hand), f"({player_value})")
        print("Dealer hand:", hand_text(dealer_hand), f"({dealer_value})")
        print("=================================")

        if dealer_value > 21 or player_value > dealer_value:
            player["blackjack_wins"] += 1
            give_pointys(player, bet, scoreboard)
            player["blackjack_profit"] += bet

            if doubled:
                player["blackjack_double_down_wins"] += 1

            if dealer_value > 21:
                print(color(player, "\nDealer busts! You win!", "success"))
            else:
                print(color(player, "\nYou win!", "success"))

            print(f"+{bet} pointys!")

        elif player_value == dealer_value:
            player["blackjack_pushes"] += 1
            print(color(player, "\nPUSH! It's a tie.", "accent"))
            print("Your bet is returned.")

        else:
            player["blackjack_losses"] += 1
            player["coins"] -= bet
            player["blackjack_profit"] -= bet

            print(color(player, "\nDealer wins.", "error"))
            print(f"-{bet} pointys.")

        check_achievements(player, scoreboard)
        save_scoreboard(scoreboard)

        print(f"\nPointys: {player['coins']}")

        if not blackjack_play_again():
            return


# ============================================================
# MENUS
# ============================================================

def menu_header(player, text):
    print("\n")
    print(color(player, "╔════════════════════════════════╗", "title"))
    print(color(player, "║" + text.center(32) + "║", "title"))
    print(color(player, "╚════════════════════════════════╝", "title"))


def choose_difficulty(player):
    names = list(DIFFICULTIES)
    while True:
        print("\n========== DIFFICULTY ==========")
        print("Choose the difficulty for this game:")
        for i, name in enumerate(names, 1):
            data = DIFFICULTIES[name]
            print(f"{i}. {name} - reward x{data['reward']:.2f}")
        print(f"{len(names) + 1}. Back")
        choice = input("> ").strip()
        if choice.isdigit():
            n = int(choice)
            if 1 <= n <= len(names):
                player["difficulty"] = names[n - 1]
                return player["difficulty"]
            if n == len(names) + 1:
                return None
        print("Invalid option.")


def games_menu(scoreboard, player_code):
    while True:
        player = scoreboard[player_code]

        menu_header(player, "GAMES")

        print("\n1. Chords")
        print("2. Timed mode")
        print("3. Memory mode")
        print("4. Endless mode")
        print("5. Custom mode")
        print("6. Casino")
        print("7. Back")

        choice = input("\n> ").strip()

        if choice in ("1", "2", "3", "4", "5"):
            difficulty = choose_difficulty(player)
            if difficulty is None:
                continue
            save_scoreboard(scoreboard)
            if choice == "1":
                play_game(scoreboard, player_code)
            elif choice == "2":
                timed_mode(scoreboard, player_code)
            elif choice == "3":
                memory_mode(scoreboard, player_code)
            elif choice == "4":
                endless_mode(scoreboard, player_code)
            elif choice == "5":
                if custom_mode_setup(scoreboard, player_code):
                    custom_mode(scoreboard, player_code)
        elif choice == "6":
            casino_menu(scoreboard, player_code)
        elif choice == "7":
            return
        else:
            print("\nThat's not a valid option.")


def profile_menu(scoreboard, player_code):
    while True:
        player = scoreboard[player_code]

        menu_header(player, "PROFILE")

        print("\n1. Stats")
        print("2. Achievements")
        print("3. Inventory")
        print("4. Stats history")
        print("5. Pets")
        print("6. Back")

        choice = input("\n> ").strip()

        if choice == "1":
            show_stats(player)
        elif choice == "2":
            show_achievements(player)
        elif choice == "3":
            show_inventory(player)
        elif choice == "4":
            show_stats_history(player)
        elif choice == "5":
            pet_menu(scoreboard, player_code)
        elif choice == "6":
            return
        else:
            print("\nThat's not a valid option.")



def casino_menu(scoreboard, player_code):
    # Keep the existing casino games; remove the extra VIP/stats submenu.
    games = [
        ("1", "Blackjack", blackjack_game),
        ("2", "Five Card Poker", poker_game),
        ("3", "Coin Flip", coin_flip_game),
        ("4", "Roulette", roulette_game),
        ("5", "Slots", slots_game),
        ("6", "Baccarat", baccarat_game),
        ("7", "Craps / Dice", dice_sum_game),
        ("8", "Sic Bo", dice_sum_game),
        ("9", "Casino War", war_game),
        ("10", "Red Dog", red_dog_game),
        ("11", "High Card", high_card_game),
        ("12", "Big Six Wheel", big_six_game),
        ("13", "Keno", keno_game),
        ("14", "Bingo", bingo_game),
        ("15", "Three Card Poker", three_card_poker_game),
        ("16", "Pai Gow", pai_gow_game),
    ]
    while True:
        player = scoreboard[player_code]
        print("\n========== CASINO ==========")
        print(f"Pointys: {player['coins']} | Jackpot: {player.get('casino_jackpot',500)} | Win streak: {player.get('casino_best_streak',0)} best")
        for n, name, _ in games:
            print(f"{n}. {name}")
        print("17. Back")
        choice = input("> ").strip()
        if choice == "17":
            return
        game = next((g for g in games if g[0] == choice), None)
        if game:
            game[2](scoreboard, player_code)
        else:
            print("Invalid option.")

def refresh_social_state(scoreboard, player_code):
    """Refresh notifications/trades for one player from the shared save file.

    The game can be run in more than one terminal at once. Each process normally
    keeps its own scoreboard in memory, so a trade created by one process would
    otherwise stay invisible to the other process until it restarted.
    """
    try:
        with open(SCOREBOARD_FILE, "r", encoding="utf-8") as file:
            fresh = json.load(file)
    except (OSError, json.JSONDecodeError):
        return scoreboard.get(player_code, {})

    if not isinstance(fresh, dict) or player_code not in fresh:
        return scoreboard.get(player_code, {})
    remote = fresh[player_code]
    if not isinstance(remote, dict):
        return scoreboard.get(player_code, {})

    local = scoreboard.setdefault(player_code, remote.copy())
    for key in ("notifications", "trade_offers", "sent_trade_offers"):
        if key in remote:
            local[key] = remote[key]
        else:
            local[key] = []

    # Keep the newest trade counter so future trade IDs remain unique.
    try:
        scoreboard["__trade_counter__"] = max(
            int(scoreboard.get("__trade_counter__", 0)),
            int(fresh.get("__trade_counter__", 0)),
        )
    except (TypeError, ValueError):
        pass
    return local


def lobby(scoreboard, player_code):
    while True:
        refresh_social_state(scoreboard, player_code)
        player = scoreboard[player_code]

        menu_header(player, "CHORDS LOBBY")

        print(f"\nPlayer:  {display_name(player)} (Lv.{player['level']})")
        print(f"Pointys: {player['coins']}")
        print(f"XP:      {xp_progress_text(player)}")
        print(f"Games:   {player['games']}")
        print(f"Best:    {player['best_combo']}x combo")
        print(f"Achieve: {len(player['achievements'])}/{len(ACHIEVEMENTS)}")

        print("\n1. Games")
        print("2. Pointy Shop")
        print("3. Profile")
        print("4. Leaderboard")
        print("5. Gifting / Trading")
        print("6. Settings")
        if player["level"] >= PRESTIGE_LEVEL:
            print("7. Prestige / Rebirth")
            print("8. Change player")
            print("9. Quit")
        else:
            print("7. Change player")
            print("8. Quit")

        choice = input("\n> ").strip()

        if choice == "1":
            games_menu(scoreboard, player_code)
        elif choice == "2":
            shop_menu(scoreboard, player_code)
        elif choice == "3":
            profile_menu(scoreboard, player_code)
        elif choice == "4":
            show_leaderboard(scoreboard)
        elif choice == "5":
            social_menu(scoreboard, player_code)
        elif choice == "6":
            settings_menu(scoreboard, player_code)
        elif choice == "7" and player["level"] >= PRESTIGE_LEVEL:
            prestige_player(scoreboard, player_code)
        elif choice == ("8" if player["level"] >= PRESTIGE_LEVEL else "7"):
            new_code = login_player(scoreboard)
            if new_code:
                player_code = new_code
        elif choice == ("9" if player["level"] >= PRESTIGE_LEVEL else "8"):
            save_scoreboard(scoreboard)
            print("\nThanks for playing Chords!")
            return
        else:
            print("\nThat's not a valid option.")



# ============================================================
# EXPANSION PACK: PETS / TRADING / SHOP / ACHIEVEMENTS / CASINO
# ============================================================

# Extra shop inventory. Eggs and tradables are deliberately separated from
# permanent upgrades so the shop can remain navigable as it grows.
SHOP_ITEMS.update({
    "egg_common": {"name": "Common Egg", "type": "pet_egg", "price": 35, "desc": "Hatches a Common pet."},
    "egg_rare": {"name": "Rare Egg", "type": "pet_egg", "price": 90, "desc": "Hatches a Rare pet."},
    "egg_epic": {"name": "Epic Egg", "type": "pet_egg", "price": 220, "desc": "Hatches an Epic pet."},
    "egg_legendary": {"name": "Legendary Egg", "type": "pet_egg", "price": 500, "desc": "Hatches a Legendary pet."},
    "egg_mythic": {"name": "Mythic Egg", "type": "pet_egg", "price": 1200, "desc": "Hatches a Mythic pet."},
    "egg_divine": {"name": "Divine Egg", "type": "pet_egg", "price": 3000, "desc": "Hatches a Divine pet."},
    "egg_secret": {"name": "??? Secret Egg", "type": "pet_egg", "price": 15000, "desc": "Extremely rare. Can hatch Secret pets."},
    "trade_gem_shop": {"name": "Trade Gem", "type": "tradable", "price": 120, "item_id": "trade_gem", "desc": "Tradable collectible."},
    "golden_ticket_shop": {"name": "Golden Ticket", "type": "tradable", "price": 600, "item_id": "golden_ticket", "desc": "Rare tradable collectible."},
    "casino_chip_shop": {"name": "Casino Chip", "type": "tradable", "price": 250, "item_id": "casino_chip", "desc": "Tradable casino collectible."},
    "pet_token_shop": {"name": "Pet Token", "type": "tradable", "price": 400, "item_id": "pet_token", "desc": "Tradable pet collectible."},
    "rainbow_ticket_shop": {"name": "Rainbow Ticket", "type": "tradable", "price": 2500, "item_id": "rainbow_ticket", "desc": "Very rare tradable collectible."},
    "void_shard_shop": {"name": "Void Shard", "type": "tradable", "price": 5000, "item_id": "void_shard", "desc": "Extremely rare tradable shard."},
})

# More achievements, including achievements that award tradeable collectibles.
_ACH_EXTRA = {
    "pets_1": ("Pet Parent", "Own your first pet.", "item", "pet_token"),
    "pets_5": ("Pet Collector", "Own 5 different pets.", "item", "trade_gem"),
    "pets_10": ("Pet Hoarder", "Own 10 different pets.", "item", "golden_ticket"),
    "pets_20": ("Pet Menagerie", "Own 20 different pets.", "item", "rainbow_ticket"),
    "rare_pet": ("Rare Friend", "Own a Rare or better pet.", "item", "pet_token"),
    "legendary_pet": ("Legendary Companion", "Own a Legendary or better pet.", "item", "golden_ticket"),
    "mythic_pet": ("Mythic Bond", "Own a Mythic or better pet.", "item", "void_shard"),
    "divine_pet": ("Divine Keeper", "Own a Divine pet.", "item", "rainbow_ticket"),
    "secret_pet": ("Beyond Chords", "Discover a Secret pet.", "item", "secret_coin"),
    "pet_10_hatched": ("Egg Enthusiast", "Hatch 10 eggs.", "pointys", 250),
    "trades_1": ("First Trade", "Complete your first trade.", "item", "trade_gem"),
    "trades_10": ("Trader", "Complete 10 trades.", "item", "golden_ticket"),
    "trades_50": ("Master Trader", "Complete 50 trades.", "item", "rainbow_ticket"),
    "tradables_10": ("Collector's Pocket", "Own 10 tradable collectibles.", "xp", 500),
    "mystery_10": ("Box Opener", "Open 10 mystery boxes.", "item", "mystery_token"),
    "mystery_50": ("Box Addict", "Open 50 mystery boxes.", "item", "jackpot_chip"),
    "casino_10": ("Casino Regular", "Play 10 casino rounds.", "item", "casino_chip"),
    "casino_win_10": ("Casino Winner", "Win 10 casino rounds.", "item", "jackpot_chip"),
    "casino_profit_1000": ("Pointy Gambler", "Earn 1,000 total casino profit.", "item", "golden_ticket"),
    "chord_25": ("Vocabulary Expansion", "Discover 25 different Chords words in the vocabulary.", "xp", 300),
    "chord_50": ("Chords Dictionary", "Discover 50 different Chords words in the vocabulary.", "item", "achievement_medal"),
}
ACHIEVEMENTS.update({k: {"name": v[0], "description": v[1], "reward_type": v[2], "reward": v[3]} for k, v in _ACH_EXTRA.items()})
ACHIEVEMENT_RULES.extend([
    ("pets_1", "pet_count", 1), ("pets_5", "pet_count", 5), ("pets_10", "pet_count", 10),
    ("pets_20", "pet_count", 20), ("pet_10_hatched", "eggs_hatched", 10),
    ("trades_1", "trades_completed", 1), ("trades_10", "trades_completed", 10),
    ("trades_50", "trades_completed", 50), ("tradables_10", "tradable_count", 10),
    ("mystery_10", "mystery_boxes_opened", 10), ("mystery_50", "mystery_boxes_opened", 50),
    ("casino_10", "casino_games", 10), ("casino_win_10", "casino_wins", 10),
    ("casino_profit_1000", "casino_profit", 1000), ("chord_25", "verities_discovered", 25),
    ("chord_50", "verities_discovered", 50),
])

# New player fields are added through the same migration path used by older saves.
_EXTRA_DEFAULTS = {
    "eggs_hatched": 0, "trades_completed": 0, "mystery_boxes_opened": 0,
    "verities_discovered": 0, "discovered_verities": [], "pet_trades": 0,
    "casino_history": [], "pet_duplicates": {},
}
_base_default_stats = default_stats

def default_stats():
    data = _base_default_stats()
    for k, v in _EXTRA_DEFAULTS.items():
        data[k] = list(v) if isinstance(v, list) else v
    return data

_base_migrate_player = migrate_player

def migrate_player(player):
    _base_migrate_player(player)
    for k, v in _EXTRA_DEFAULTS.items():
        if k not in player:
            player[k] = list(v) if isinstance(v, list) else v
    if not isinstance(player.get("discovered_verities"), list): player["discovered_verities"] = []
    if not isinstance(player.get("pet_duplicates"), dict): player["pet_duplicates"] = {}
    return player

# Rewards can now be pointys, XP, or a specific tradable collectible.
def unlock_achievement(player, achievement_id, scoreboard=None):
    if achievement_id not in ACHIEVEMENTS or achievement_id in player["achievements"]:
        return False
    achievement = ACHIEVEMENTS[achievement_id]
    player["achievements"].append(achievement_id)
    print(color(player, "\n🏆 ACHIEVEMENT UNLOCKED!", "accent"))
    print(color(player, achievement["name"], "success"))
    print(achievement["description"])
    rt, reward = achievement["reward_type"], achievement["reward"]
    if rt == "pointys":
        give_pointys(player, reward, scoreboard)
        print(color(player, f"+{reward} pointys", "info"))
    elif rt == "xp":
        add_xp(player, reward, scoreboard)
        print(color(player, f"+{reward} XP", "info"))
    elif rt == "item":
        add_item(player, reward)
        label = TRADABLE_ITEMS.get(reward, {}).get("name", reward)
        print(color(player, f"Reward: {label} (tradable)", "info"))
    if scoreboard is not None: save_scoreboard(scoreboard)
    return True

def check_achievements(player, scoreboard=None, perfect_game=False):
    stats = dict(player)
    stats.update({
        "upgrade_count": len(player.get("upgrades", [])),
        "pet_count": len(player.get("pets", [])),
        "tradable_count": sum(c for i, c in player.get("inventory", {}).items() if i in TRADABLE_ITEMS),
        "verities_discovered": len(set(player.get("discovered_verities", []))),
    })
    for aid, stat, threshold in ACHIEVEMENT_RULES:
        if stats.get(stat, 0) >= threshold:
            unlock_achievement(player, aid, scoreboard)
    if perfect_game: unlock_achievement(player, "perfect_game", scoreboard)
    if any(PET_DATA.get(p, {}).get("rarity") == "Rare" for p in player.get("pets", [])):
        unlock_achievement(player, "rare_pet", scoreboard)
    if any(PET_DATA.get(p, {}).get("rarity") == "Legendary" for p in player.get("pets", [])):
        unlock_achievement(player, "legendary_pet", scoreboard)
    if any(PET_DATA.get(p, {}).get("rarity") == "Mythic" for p in player.get("pets", [])):
        unlock_achievement(player, "mythic_pet", scoreboard)
    if any(PET_DATA.get(p, {}).get("rarity") == "Divine" for p in player.get("pets", [])):
        unlock_achievement(player, "divine_pet", scoreboard)
    if any(PET_DATA.get(p, {}).get("rarity") == "Secret" for p in player.get("pets", [])):
        unlock_achievement(player, "secret_pet", scoreboard)

# Pet duplicates are now retained as tradeable "pet copies" rather than silently discarded.
def add_pet(player, pet_id):
    if pet_id in player["pets"]:
        player["pet_duplicates"][pet_id] = player["pet_duplicates"].get(pet_id, 0) + 1
        return False
    player["pets"].append(pet_id)
    return True

def pet_copy_count(player, pet_id):
    return player.get("pet_duplicates", {}).get(pet_id, 0)

def remove_pet_copy(player, pet_id):
    count = pet_copy_count(player, pet_id)
    if count <= 0: return False
    if count == 1: player["pet_duplicates"].pop(pet_id, None)
    else: player["pet_duplicates"][pet_id] = count - 1
    return True

def pet_rarity_for_box(lucky=False):
    roll = random.random()
    if lucky:
        if roll < .002: return "egg_secret"
        if roll < .025: return "egg_divine"
        if roll < .10: return "egg_mythic"
        if roll < .27: return "egg_legendary"
        if roll < .55: return "egg_epic"
        if roll < .82: return "egg_rare"
        return "egg_common"
    if roll < .0005: return "egg_secret"
    if roll < .004: return "egg_divine"
    if roll < .015: return "egg_mythic"
    if roll < .05: return "egg_legendary"
    if roll < .16: return "egg_epic"
    if roll < .36: return "egg_rare"
    return "egg_common"

def hatch_egg(player, scoreboard):
    eggs = [i for i in player["inventory"] if i in EGG_DATA and inv_count(player, i) > 0]
    if not eggs:
        print("You don't have any eggs."); return
    print("\nEggs:")
    for i, egg in enumerate(eggs, 1): print(f"{i}. {EGG_DATA[egg]['name']} ({inv_count(player, egg)})")
    choice = input("> ").strip()
    if not choice.isdigit() or not 1 <= int(choice) <= len(eggs): return
    egg = eggs[int(choice)-1]; remove_item(player, egg)
    data = EGG_DATA[egg]
    pet = random.choices(list(data["weights"]), weights=list(data["weights"].values()))[0]
    new = add_pet(player, pet)
    player["eggs_hatched"] += 1
    if not new: print("DUPLICATE PET! The duplicate was added as a tradable pet copy.")
    player["active_pet"] = pet
    print(color(player, f"\nHATCHED: {data['name']} -> {PET_DATA[pet]['name']} ({PET_DATA[pet]['rarity']})!", "success"))
    check_achievements(player, scoreboard); save_scoreboard(scoreboard)
    input("Press ENTER to continue...")

def pet_menu(scoreboard, player_code):
    player = scoreboard[player_code]
    while True:
        print("\n========== PETS ==========")
        print(f"Active: {PET_DATA.get(player.get('active_pet'), {}).get('name', '(none)')}")
        print(f"Collection: {len(player['pets'])}/{len(PET_DATA)} unique | duplicates: {sum(player.get('pet_duplicates', {}).values())}")
        print("1. Hatch an egg\n2. Equip a pet\n3. View collection\n4. View all pet rarities\n5. Back")
        choice=input("> ").strip()
        if choice == "1": hatch_egg(player, scoreboard)
        elif choice == "2":
            if not player["pets"]: print("You don't own any pets."); continue
            for i, pet in enumerate(player["pets"],1): print(f"{i}. {PET_DATA[pet]['name']} ({PET_DATA[pet]['rarity']})")
            n=input("> ").strip()
            if n.isdigit() and 1<=int(n)<=len(player["pets"]): player["active_pet"]=player["pets"][int(n)-1]; save_scoreboard(scoreboard); print("Pet equipped.")
        elif choice == "3":
            for pet in player["pets"]:
                d=PET_DATA[pet]; dup=pet_copy_count(player,pet)
                print(f"- {d['name']} [{d['rarity']}] | pointys +{d['pointy']*100:.0f}% | XP +{d['xp']*100:.0f}% | events +{d['event']*100:.0f}% | copies: {dup}")
            input("Press ENTER to continue...")
        elif choice == "4":
            rarity_order=["Common","Rare","Epic","Legendary","Mythic","Divine","Secret"]
            for rarity in rarity_order:
                print(f"\n{rarity.upper()}:")
                for pid,d in PET_DATA.items():
                    if d['rarity']==rarity: print(f"  {d['name']}")
            input("Press ENTER to continue...")
        elif choice == "5": return
        else: print("Invalid option.")

# Trading now supports pointys, tradable items, eggs, and duplicate pet copies.
def _trade_options(player):
    opts=[]
    for item,c in player.get("inventory",{}).items():
        if c>0 and (item in TRADABLE_ITEMS or item in EGG_DATA): opts.append(("item",item))
    # Every owned pet is tradeable. The currently equipped pet is protected.
    for pet in player.get("pets",[]):
        if pet != player.get("active_pet"): opts.append(("pet",pet))
    for pet,c in player.get("pet_duplicates",{}).items():
        if c>0: opts.append(("pet_copy",pet))
    return opts

def _trade_label(kind, item):
    if kind in ("pet","pet_copy"): return f"PET: {PET_DATA[item]['name']} [{PET_DATA[item]['rarity']}]"
    if item in EGG_DATA: return f"{EGG_DATA[item]['name']} (egg)"
    return TRADABLE_ITEMS.get(item,{}).get("name",item)

def _remove_trade_asset(player, kind, item):
    if kind=="pet_copy": return remove_pet_copy(player,item)
    if kind=="pet":
        if item == player.get("active_pet") or item not in player.get("pets",[]): return False
        player["pets"].remove(item)
        return True
    return remove_item(player,item)

def _add_trade_asset(player, kind, item):
    if kind in ("pet","pet_copy"):
        add_pet(player,item); return
    add_item(player,item)

def social_menu(scoreboard, player_code):
    player=scoreboard[player_code]
    while True:
        print("\n========== GIFTING & TRADING ==========")
        print("1. Gift pointys\n2. Gift an item\n3. Trade with a player\n4. Back")
        choice=input("> ").strip()
        if choice=="4": return
        if choice not in ("1","2","3"): print("Invalid option."); continue
        target_code=input("Target player code: ").strip().upper()
        if target_code not in scoreboard or target_code==player_code: print("That player code is invalid."); continue
        target=scoreboard[target_code]
        if choice=="1":
            try: amount=int(input("Pointys to gift: ").strip())
            except ValueError: print("Invalid amount."); continue
            if amount<=0 or amount>player["coins"]: print("You don't have that many pointys."); continue
            player["coins"]-=amount; target["coins"]+=amount; print(f"Gifted {amount} pointys to {target['name']}.")
        elif choice=="2":
            item=input("Item/egg ID to gift: ").strip()
            if inv_count(player,item)<=0 or (item not in SHOP_ITEMS and item not in EGG_DATA and item not in TRADABLE_ITEMS): print("You don't have that item."); continue
            remove_item(player,item); add_item(target,item); print(f"Gifted {_trade_label('item',item)} to {target['name']}.")
        else:
            my=_trade_options(player); their=_trade_options(target)
            if not my or not their: print("Both players need a tradable item, egg, or non-equipped pet."); continue
            print("YOUR ASSETS:")
            for i,(k,x) in enumerate(my,1): print(f"{i}. {_trade_label(k,x)}")
            print(f"\n{target['name'].upper()}'S ASSETS:")
            for i,(k,x) in enumerate(their,1): print(f"{i}. {_trade_label(k,x)}")
            try: a=int(input("Your asset #: "))-1; b=int(input("Their asset #: "))-1
            except ValueError: print("Invalid trade."); continue
            if not(0<=a<len(my) and 0<=b<len(their)): print("Invalid trade."); continue
            mine,theirs=my[a],their[b]
            if input(f"Trade {_trade_label(*mine)} for {_trade_label(*theirs)}? Type TRADE: ").strip().upper()!="TRADE": print("Trade cancelled."); continue
            if not _remove_trade_asset(player,*mine) or not _remove_trade_asset(target,*theirs): print("Trade failed; one asset was unavailable."); continue
            _add_trade_asset(player,*theirs); _add_trade_asset(target,*mine)
            player["trades_completed"]+=1; target["trades_completed"]+=1
            player["pet_trades"]+=int(mine[0] in ("pet","pet_copy") or theirs[0] in ("pet","pet_copy"))
            check_achievements(player,scoreboard); check_achievements(target,scoreboard); print("Trade completed!")
        save_scoreboard(scoreboard)

# Mystery boxes can award every egg tier plus a larger tradable pool.
def open_mystery_box(player, scoreboard, lucky=False):
    item_id="lucky_box" if lucky else "mystery_box"
    if not remove_item(player,item_id): print("You don't have that box."); return
    player["mystery_boxes_opened"]+=1
    roll=random.random(); multiplier=2 if lucky else 1
    if roll < (.28 if lucky else .32):
        amount=random.randint(20,90)*multiplier; give_pointys(player,amount,scoreboard); print(color(player,f"MYSTERY BOX: +{amount} pointys!","success"))
    elif roll < (.53 if lucky else .56):
        amount=random.randint(25,100)*multiplier; add_xp(player,amount,scoreboard); print(color(player,f"MYSTERY BOX: +{amount} XP!","info"))
    elif roll < (.58 if lucky else .68): print("MYSTERY BOX: ...nothing. The box was empty.")
    elif roll < (.88 if lucky else .86):
        egg=pet_rarity_for_box(lucky); add_item(player,egg); print(color(player,f"MYSTERY BOX: You found a {EGG_DATA[egg]['name']}!","accent"))
    else:
        weights=[60,18,8,5,3,2,1,1,1,1]
        tradable=random.choices(list(TRADABLE_ITEMS),weights=weights)[0]; add_item(player,tradable); print(color(player,f"MYSTERY BOX: You found {TRADABLE_ITEMS[tradable]['name']}!","accent"))
    check_achievements(player,scoreboard); save_scoreboard(scoreboard)

# A truly segmented shop: each section is its own screen.
def shop_menu(scoreboard, player_code):
    sections=[("1","consumable","Consumables"),("2","mystery","Mystery Boxes"),("3","upgrade","Permanent Upgrades"),("4","theme_title","Themes & Titles"),("5","pet_egg","Pet Eggs"),("6","tradable","Tradable Collectibles")]
    while True:
        player=scoreboard[player_code]
        print(color(player,"\n╔════════════════════════════════╗\n║          POINTY SHOP           ║\n╚════════════════════════════════╝","title")); print(f"\nYour pointys: {player['coins']}\n")
        for n,_,label in sections: print(f"{n}. {label}")
        print(f"{len(sections)+1}. Back")
        choice=input("\n> ").strip()
        if choice==str(len(sections)+1): return
        sec=next((x for x in sections if x[0]==choice),None)
        if sec: shop_category_menu(scoreboard,player_code,sec[1],sec[2])
        else: print("Invalid option.")

def shop_category_menu(scoreboard, player_code, category, title):
    while True:
        player=scoreboard[player_code]; print(color(player,f"\n========== {title.upper()} ==========","title")); print(f"Pointys: {player['coins']}\n")
        if category=="theme_title": ids=[i for i,x in SHOP_ITEMS.items() if x["type"] in ("theme","title")]
        else: ids=[i for i,x in SHOP_ITEMS.items() if x["type"]==category]
        for number,item_id in enumerate(ids,1):
            item=SHOP_ITEMS[item_id]; owned=owns_item(player,item_id) if item["type"] in ("upgrade","theme","title") else inv_count(player,item.get("item_id",item_id))
            tag=" [OWNED]" if owned else (f" (you have {owned})" if owned else "")
            print(f"{number:>2}. {item['name']} - {item['price']} pointys{tag}\n      {item['desc']}")
        if category=="mystery":
            print(f"\n{len(ids)+1}. Open a Mystery Box\n{len(ids)+2}. Open a Lucky Mystery Box\n{len(ids)+3}. Back"); back=len(ids)+3
        else: print(f"\n{len(ids)+1}. Back"); back=len(ids)+1
        choice=input("\n> ").strip()
        if not choice.isdigit(): print("Invalid option."); continue
        n=int(choice)
        if 1<=n<=len(ids):
            item=SHOP_ITEMS[ids[n-1]]
            if player["coins"]<item["price"]: print("Not enough pointys!"); continue
            player["coins"]-=item["price"]; player["pointys_spent"]+=item["price"]; player["items_bought"]+=1
            kind=item["type"]
            if kind=="tradable": add_item(player,item["item_id"])
            elif kind=="pet_egg": add_item(player,ids[n-1])
            elif kind=="consumable": add_item(player,ids[n-1])
            elif kind=="mystery": add_item(player,ids[n-1])
            elif kind=="upgrade": player["upgrades"].append(ids[n-1])
            elif kind=="theme": player["owned_themes"].append(item["value"]); player["theme"]=item["value"]
            elif kind=="title": player["owned_titles"].append(item["value"]); player["title"]=item["value"]
            print(color(player,f"Bought {item['name']}!","success")); check_achievements(player,scoreboard); save_scoreboard(scoreboard); continue
        if category=="mystery" and n==len(ids)+1: open_mystery_box(player,scoreboard,False); continue
        if category=="mystery" and n==len(ids)+2: open_mystery_box(player,scoreboard,True); continue
        if n==back: return
        print("Invalid option.")

# ---------------- CASINO EXPANSION ----------------
def casino_result(player, scoreboard, bet, net, name):
    player["casino_games"]+=1
    if net>0: player["casino_wins"]+=1; give_pointys(player,net,scoreboard)
    else: player["coins"]+=net
    player["casino_profit"]+=net; player.setdefault("casino_history",[]).append({"game":name,"net":net,"time":time.strftime("%Y-%m-%d %H:%M")}); player["casino_history"]=player["casino_history"][-50:]
    check_achievements(player,scoreboard); save_scoreboard(scoreboard)

def baccarat_game(scoreboard, player_code):
    player=scoreboard[player_code]
    while True:
        bet=casino_bet(player)
        if bet==0:return
        choice=input("Bet on Player, Banker, or Tie? ").strip().lower()
        if choice not in ("player","banker","tie"): print("Invalid choice."); continue
        def hand():
            return [random.randint(0,9),random.randint(0,9)]
        ph,bh=hand(),hand(); pv=sum(ph)%10; bv=sum(bh)%10
        winner="player" if pv>bv else "banker" if bv>pv else "tie"
        player["coins"]-=bet
        mult=8 if choice=="tie" else 1 if choice==winner else -1
        net=bet*mult
        casino_result(player,scoreboard,bet,net,"Baccarat")
        print(f"Player {pv} | Banker {bv} -> {winner.upper()} | Net {net:+d}")

def dice_sum_game(scoreboard,player_code):
    player=scoreboard[player_code]
    while True:
        bet=casino_bet(player)
        if bet==0:return
        try: pick=int(input("Pick a dice total (3-18): "))
        except ValueError: continue
        if not 3<=pick<=18: continue
        dice=[random.randint(1,6) for _ in range(3)]; total=sum(dice); player["coins"]-=bet
        net=bet*(5 if total==pick else 1 if abs(total-pick)<=1 else -1)
        casino_result(player,scoreboard,bet,net,"Sic Bo")
        print(f"Dice {dice} = {total} | Net {net:+d}")

def war_game(scoreboard,player_code):
    player=scoreboard[player_code]
    while True:
        bet=casino_bet(player)
        if bet==0:return
        a,b=random.randint(2,14),random.randint(2,14); player["coins"]-=bet
        net=bet if a>b else -bet if a<b else 0
        casino_result(player,scoreboard,bet,net,"War"); print(f"Your card {a} | Dealer {b} | Net {net:+d}")

def red_dog_game(scoreboard,player_code):
    player=scoreboard[player_code]
    while True:
        bet=casino_bet(player)
        if bet==0:return
        a,b=random.randint(1,13),random.randint(1,13); low,high=sorted((a,b)); gap=high-low-1; c=random.randint(1,13); player["coins"]-=bet
        if c>low and c<high: net=bet*max(1,gap)
        elif c==low or c==high: net=-bet
        else: net=-bet
        casino_result(player,scoreboard,bet,net,"Red Dog"); print(f"Cards {a}, {b}; middle {c} | Net {net:+d}")

def high_card_game(scoreboard,player_code):
    player=scoreboard[player_code]

    while True:
        bet=casino_bet(player)
        if bet==0:return
        a,b=random.randint(2,14),random.randint(2,14); player["coins"]-=bet
        net=bet if a>b else -bet if a<b else 0
        casino_result(player,scoreboard,bet,net,"High Card")
        print(f"You {a} | House {b} | Net {net:+d}")

def big_six_game(scoreboard,player_code):
    player=scoreboard[player_code]; options=[("1",2),("2",5),("5",10),("10",20),("20",40),("JACKPOT",100)]
    while True:
        bet=casino_bet(player)
        if bet==0:return
        for i,(label,mult) in enumerate(options,1): print(f"{i}. {label} ({mult}x)")
        try:n=int(input("> "))-1
        except ValueError:continue
        if not 0<=n<len(options):continue
        result=random.choice(options); player["coins"]-=bet; net=bet*(result[1] if n==options.index(result) else -1)
        casino_result(player,scoreboard,bet,net,"Big Six Wheel"); print(f"Wheel: {result[0]} | Net {net:+d}")

def keno_game(scoreboard,player_code):
    player=scoreboard[player_code]
    while True:
        bet=casino_bet(player)
        if bet==0:return
        raw=input("Pick 5 unique numbers 1-40: ").split()
        try:picks=set(int(x) for x in raw)
        except ValueError:continue
        if len(picks)!=5 or any(x<1 or x>40 for x in picks):continue
        draw=set(random.sample(range(1,41),10)); matches=len(picks&draw); player["coins"]-=bet
        payout={0:-1,1:-1,2:0,3:2,4:8,5:30}; net=bet*payout[matches]
        casino_result(player,scoreboard,bet,net,"Keno"); print(f"Draw: {sorted(draw)} | Matches: {matches} | Net {net:+d}")

def bingo_game(scoreboard,player_code):
    player=scoreboard[player_code]
    while True:
        bet=casino_bet(player)
        if bet==0:return
        card=random.sample(range(1,51),10); draws=random.sample(range(1,51),20); hits=len(set(card)&set(draws)); player["coins"]-=bet
        net=bet*(20 if hits>=8 else 5 if hits>=6 else 0 if hits>=4 else -1)
        casino_result(player,scoreboard,bet,net,"Bingo"); print(f"Hits: {hits}/10 | Net {net:+d}")

def three_card_poker_game(scoreboard,player_code):
    player=scoreboard[player_code]

    rank_names={0:"High Card",1:"Pair",2:"Flush",3:"Straight",4:"Three of a Kind"}
    while True:
        bet=casino_bet(player)
        if bet==0:return
        cards=random.sample(range(2,15),3); counts={x:cards.count(x) for x in cards}; unique=sorted(set(cards)); flush=random.random()<0.25
        if 3 in counts.values(): rank=4
        elif len(counts)==2: rank=1
        elif len(counts)==3 and (max(unique)-min(unique)==2): rank=3
        elif flush: rank=2
        else: rank=0
        mult={0:0,1:1,2:2,3:3,4:5}[rank]; player["coins"]-=bet; net=bet*mult if mult else -bet
        casino_result(player,scoreboard,bet,net,"Three Card Poker"); print(f"Cards {cards} -> {rank_names[rank]} | Net {net:+d}")

def pai_gow_game(scoreboard,player_code):
    player=scoreboard[player_code]
    while True:
        bet=casino_bet(player)
        if bet==0:return
        player_hand=sum(random.sample(range(1,14),7))%10; dealer_hand=sum(random.sample(range(1,14),7))%10; player["coins"]-=bet
        net=bet if player_hand>dealer_hand else -bet if player_hand<dealer_hand else 0
        casino_result(player,scoreboard,bet,net,"Pai Gow"); print(f"You {player_hand} | Dealer {dealer_hand} | Net {net:+d}")

def casino_menu(scoreboard,player_code):
    games=[("1","Blackjack",blackjack_mode),("2","Five Card Poker",poker_mode),("3","Coin Flip",coin_flip_game),("4","Roulette",roulette_game),("5","Slots",slots_game),("6","Baccarat",baccarat_game),("7","Craps / Dice",dice_sum_game),("8","Sic Bo",dice_sum_game),("9","Casino War",war_game),("10","Red Dog",red_dog_game),("11","High Card",high_card_game),("12","Big Six Wheel",big_six_game),("13","Keno",keno_game),("14","Bingo",bingo_game),("15","Three Card Poker",three_card_poker_game),("16","Pai Gow",pai_gow_game)]
    while True:
        player=scoreboard[player_code]; print("\n========== CASINO =========="); print(f"Pointys: {player['coins']}")
        for n,name,_ in games: print(f"{n}. {name}")
        print("17. Back"); choice=input("> ").strip()
        if choice=="17":return
        game=next((g for g in games if g[0]==choice),None)
        if game: game[2](scoreboard,player_code)
        else: print("Invalid option.")

# Track discovered Verities when a valid word is entered by game modes.
# The existing modes compare against VERITIES directly, so this helper can be
# called from future modes as well without changing their scoring logic.
def discover_chord(player, word, scoreboard=None):
    if word in VERITIES and word not in player.setdefault("discovered_verities",[]):
        player["discovered_verities"].append(word); check_achievements(player,scoreboard)


# ============================================================
# EXPANSION PACK V2: COLLECTION / PET LAB / MARKET / QUESTS / CASINO
# No new worlds, no daily/weekly systems, and no new casino games.
# ============================================================

# --- Extended economy and player progression ---------------------------------
TRADABLE_ITEMS.update({
    "mystery_token": {"name": "Mystery Token", "desc": "Opens special mystery rewards. Tradable."},
    "pet_token": {"name": "Pet Token", "desc": "Used for pet lab upgrades. Tradable."},
    "rainbow_ticket": {"name": "Rainbow Ticket", "desc": "A rare collector ticket. Tradable."},
    "void_shard": {"name": "Void Shard", "desc": "A mysterious high-value shard. Tradable."},
    "secret_coin": {"name": "Secret Coin", "desc": "A very rare collector coin. Tradable."},
    "jackpot_chip": {"name": "Jackpot Chip", "desc": "A special casino collectible. Tradable."},
    "achievement_medal": {"name": "Achievement Medal", "desc": "Proof of an important achievement. Tradable."},
})

# Ability metadata is separate from the numeric pet bonuses so old saves remain compatible.
PET_ABILITIES = {
    "pointy_cat": "Pointy Purr: +5% Pointys",
    "xp_bunny": "Bunny Brain: +5% XP",
    "sleepy_dog": "Lucky Nap: small event boost",
    "tiny_frog": "Lucky Hop: improves event luck",
    "hamster": "Snack Hoard: small Pointy bonus",
    "lucky_fox": "Fortune Tail: +event luck",
    "blue_penguin": "Cool Head: small casino bonus",
    "mushroom_mouse": "Spore Luck: improves mystery rewards",
    "cloud_puppy": "Cloud Nine: small XP boost",
    "ninja_owl": "Silent Insight: improves Chords discovery",
    "golden_slime": "Golden Goo: +Pointys and XP",
    "lava_lizard": "Hot Streak: stronger casino wins",
    "crystal_deer": "Crystal Memory: improves pet XP",
    "storm_crow": "Storm Sense: stronger event luck",
    "rainbow_axolotl": "Rainbow Luck: boosts rare rewards",
    "cosmic_dragon": "Cosmic Fortune: Pointys + XP + event luck",
    "phoenix": "Rebirth Flame: improves pet XP and prestige rewards",
    "celestial_wolf": "Celestial Hunt: improves rare drops",
    "galaxy_whale": "Galaxy Vault: improves trade rewards",
    "void_kitty": "Void Whisper: improves mystery boxes",
    "nebula_serpent": "Nebula Coil: boosts casino luck",
    "time_bunny": "Time Skip: improves timed rewards",
    "reality_glitch": "Reality Glitch: chance for bonus loot",
    "pointy_god": "Pointy Dominion: major Pointy bonus",
    "infinity_dragon": "Infinity: strong XP and Pointy bonus",
    "world_eater": "World Eater: enormous rare-drop bonus",
    "secret_glitch_cat": "Secret Glitch: chance to duplicate rewards",
    "secret_void_dragon": "Secret Void: powerful mystery and casino luck",
    "secret_pointy": "Secret Pointy: ultimate collector bonus",
}

# Mutations are cosmetic/bonus variants stored as separate pet instances.
PET_MUTATIONS = {
    "Shiny": {"mult": 1.25, "chance": 0.035},
    "Golden": {"mult": 1.50, "chance": 0.015},
    "Rainbow": {"mult": 2.00, "chance": 0.006},
    "Corrupted": {"mult": 2.25, "chance": 0.003},
    "Void": {"mult": 3.00, "chance": 0.0015},
}

# Fusion recipes consume duplicate copies and create a higher-rarity pet.
PET_FUSIONS = {
    "pointy_cat": "lucky_fox",
    "xp_bunny": "cloud_puppy",
    "sleepy_dog": "ninja_owl",
    "tiny_frog": "mushroom_mouse",
    "hamster": "blue_penguin",
    "lucky_fox": "golden_slime",
    "blue_penguin": "crystal_deer",
    "mushroom_mouse": "storm_crow",
    "cloud_puppy": "rainbow_axolotl",
    "ninja_owl": "lava_lizard",
    "golden_slime": "cosmic_dragon",
    "lava_lizard": "phoenix",
    "crystal_deer": "celestial_wolf",
    "storm_crow": "galaxy_whale",
    "rainbow_axolotl": "void_kitty",
    "cosmic_dragon": "nebula_serpent",
    "phoenix": "time_bunny",
    "celestial_wolf": "reality_glitch",
    "galaxy_whale": "pointy_god",
    "void_kitty": "infinity_dragon",
    "nebula_serpent": "world_eater",
    "time_bunny": "secret_glitch_cat",
    "reality_glitch": "secret_void_dragon",
}

PET_EVOLUTIONS = {
    "lucky_fox": (10, "golden_slime"),
    "golden_slime": (15, "cosmic_dragon"),
    "cosmic_dragon": (20, "nebula_serpent"),
    "void_kitty": (25, "infinity_dragon"),
    "infinity_dragon": (30, "secret_pointy"),
}

# Static story quests: these are not daily/weekly and can be completed once.
STORY_QUESTS = {
    "quest_first_pet": ("A New Friend", "Own your first pet.", "pet_count", 1, "pet_token", 1),
    "quest_collector": ("Collector's Path", "Own 10 unique pets.", "pet_count", 10, "trade_gem", 3),
    "quest_fusion": ("The Pet Lab", "Complete your first pet fusion.", "fusions", 1, "mystery_token", 2),
    "quest_mutation": ("Strange Genetics", "Obtain a mutated pet.", "mutations", 1, "rainbow_ticket", 1),
    "quest_secret": ("Secret Hunter", "Own a Secret pet.", "secret_pets", 1, "secret_coin", 1),
    "quest_chord": ("Word Collector", "Discover 25 Verities.", "verities_discovered", 25, "achievement_medal", 1),
    "quest_market": ("Merchant", "Complete a marketplace purchase.", "market_purchases", 1, "golden_ticket", 1),
    "quest_casino": ("VIP Table", "Reach Casino VIP rank 3.", "casino_vip", 3, "jackpot_chip", 2),
    "quest_prestige": ("Reborn", "Prestige at least once.", "prestige", 1, "void_shard", 1),
}


def _v2_defaults():
    return {
        "pet_xp": {}, "pet_levels": {}, "pet_mutations": {},
        "pet_locked": [], "favorite_pets": [], "pet_bond": {},
        "fusions": 0, "mutations": 0, "evolutions": 0,
        "pet_quests": {}, "market_purchases": 0, "market_sales": 0,
        "market_listings_created": 0, "verities_discovered": 0,
        "discovered_verities": [], "inventory_locked": [],
        "currency_gems": 0, "currency_tokens": 0, "currency_void": 0,
        "casino_vip": 0, "casino_history": [], "casino_biggest_win": 0,
        "casino_biggest_loss": 0, "casino_streak": 0, "casino_best_streak": 0,
        "casino_jackpot": 500, "casino_jackpots_hit": 0,
        "casino_wagered": 0, "casino_sessions": 0,
        "random_events_triggered": 0, "special_events": [],
        "story_flags": {}, "prestige_history": [],
    }


def _v2_migrate(player):
    for k, v in _v2_defaults().items():
        if k not in player:
            player[k] = v.copy() if isinstance(v, (dict, list)) else v
    for k in ("pet_xp", "pet_levels", "pet_mutations", "pet_bond", "story_flags", "inventory_locked"):
        if not isinstance(player.get(k), dict) and k not in ("inventory_locked",):
            player[k] = {}
    for k in ("pet_locked", "favorite_pets", "discovered_verities", "casino_history", "special_events", "prestige_history", "inventory_locked"):
        if not isinstance(player.get(k), list): player[k] = []
    if not isinstance(player.get("pet_quests"), dict): player["pet_quests"] = {}
    return player

_old_migrate_player = migrate_player
def migrate_player(player):
    _old_migrate_player(player)
    return _v2_migrate(player)

_old_default_stats = default_stats
def default_stats():
    d = _old_default_stats()
    d.update(_v2_defaults())
    return d

# Re-run migration helper for currently loaded/newly created records.


def pet_key(pet_id, mutation=""):
    return f"{pet_id}::{mutation}" if mutation else pet_id


def parse_pet_key(key):
    if "::" in key:
        return tuple(key.split("::", 1))
    return key, ""


def pet_display_name(pet_id, mutation=""):
    base = PET_DATA.get(pet_id, {}).get("name", pet_id)
    return f"{mutation} {base}" if mutation else base


def pet_effect_multiplier(player, pet_id=None):
    if pet_id is None: pet_id = player.get("active_pet", "")
    data = PET_DATA.get(pet_id, {})
    return max(1.0, 1.0 + float(data.get("pointy", 0)) + float(data.get("xp", 0)) * 0.25)


def pet_level(player, pet_id):
    return int(player.get("pet_levels", {}).get(pet_id, 1))


def grant_pet_xp(player, amount, scoreboard=None):
    pet_id = player.get("active_pet", "")
    if not pet_id or pet_id not in PET_DATA or amount <= 0:
        return
    levels = player.setdefault("pet_levels", {})
    xp = player.setdefault("pet_xp", {})
    level = int(levels.get(pet_id, 1))
    xp[pet_id] = int(xp.get(pet_id, 0)) + max(1, int(amount))
    while level < 100 and xp[pet_id] >= 100 + level * 25:
        xp[pet_id] -= 100 + level * 25
        level += 1
        print(color(player, f"PET LEVEL UP! {PET_DATA[pet_id]['name']} is now Lv.{level}!", "accent"))
    levels[pet_id] = level
    player.setdefault("pet_bond", {})[pet_id] = int(player["pet_bond"].get(pet_id, 0)) + 1
    if scoreboard is not None: save_scoreboard(scoreboard)


def grant_pet_collection_xp(player, amount, scoreboard=None):
    grant_pet_xp(player, amount, scoreboard)


def mutate_pet(player, pet_id, scoreboard=None):
    roll = random.random()
    running = 0.0
    for mutation, info in PET_MUTATIONS.items():
        running += info["chance"]
        if roll < running:
            player.setdefault("pet_mutations", {}).setdefault(pet_id, {})
            count = player["pet_mutations"][pet_id].get(mutation, 0) + 1
            player["pet_mutations"][pet_id][mutation] = count
            player["mutations"] = int(player.get("mutations", 0)) + 1
            if scoreboard is not None: save_scoreboard(scoreboard)
            return mutation
    return ""


def pet_copy_count(player, pet_id):
    # Base copies are stored in pet_duplicates by the existing expansion.
    return int(player.get("pet_duplicates", {}).get(pet_id, 0))


def _unique_pet_count(player):
    return len(set(p for p in player.get("pets", []) if p in PET_DATA))


def evolve_pet(player, pet_id, scoreboard=None):
    recipe = PET_EVOLUTIONS.get(pet_id)
    if not recipe:
        print("That pet has no evolution yet.")
        return False
    required_level, target = recipe
    if pet_level(player, pet_id) < required_level:
        print(f"This pet needs level {required_level}.")
        return False
    if pet_id not in player.get("pets", []):
        return False
    if target not in player["pets"]:
        player["pets"].append(target)
    player["active_pet"] = target
    player["evolutions"] = int(player.get("evolutions", 0)) + 1
    print(color(player, f"EVOLUTION! {PET_DATA[pet_id]['name']} -> {PET_DATA[target]['name']}!", "accent"))
    check_story_quests(player, scoreboard)
    save_scoreboard(scoreboard)
    return True


def fuse_pets(player, scoreboard=None):
    candidates = [p for p in sorted(set(player.get("pets", []))) if p in PET_FUSIONS and pet_copy_count(player, p) >= 2]
    if not candidates:
        print("You need at least 2 duplicate copies of a fusion recipe pet.")
        return False
    for i, p in enumerate(candidates, 1):
        print(f"{i}. {PET_DATA[p]['name']} x{pet_copy_count(player,p)+1} -> {PET_DATA[PET_FUSIONS[p]]['name']}")
    raw=input("> ").strip()
    if not raw.isdigit() or not 1 <= int(raw) <= len(candidates): return False
    source=candidates[int(raw)-1]; target=PET_FUSIONS[source]
    if not remove_pet_copy(player, source) or not remove_pet_copy(player, source): return False
    if target not in player["pets"]: player["pets"].append(target)
    player["fusions"] = int(player.get("fusions",0))+1
    mutation = mutate_pet(player, target, scoreboard)
    if mutation: print(color(player, f"Fusion mutation: {mutation}!", "accent"))
    print(color(player, f"FUSION COMPLETE: {PET_DATA[source]['name']} -> {PET_DATA[target]['name']}!", "success"))
    check_story_quests(player, scoreboard)
    save_scoreboard(scoreboard)
    return True


def pet_lab_menu(scoreboard, player_code):
    player=scoreboard[player_code]
    while True:
        print("\n========== PET LAB ==========")
        print("1. Level / bond info")
        print("2. Fuse duplicate pets")
        print("3. Evolve a pet")
        print("4. Mutation collection")
        print("5. Back")
        choice=input("> ").strip()
        if choice=="1":
            for p in sorted(set(player.get("pets", []))):
                print(f"- {PET_DATA.get(p,{}).get('name',p)} | Lv.{pet_level(player,p)} | XP {player.get('pet_xp',{}).get(p,0)} | Bond {player.get('pet_bond',{}).get(p,0)}")
            input("Press ENTER...")
        elif choice=="2": fuse_pets(player,scoreboard)
        elif choice=="3":
            options=[p for p in player.get("pets",[]) if p in PET_EVOLUTIONS]
            for i,p in enumerate(options,1): print(f"{i}. {PET_DATA[p]['name']} Lv.{pet_level(player,p)} -> {PET_DATA[PET_EVOLUTIONS[p][1]]['name']} at Lv.{PET_EVOLUTIONS[p][0]}")
            raw=input("> ").strip()
            if raw.isdigit() and 1<=int(raw)<=len(options): evolve_pet(player,options[int(raw)-1],scoreboard)
        elif choice=="4":
            for p, muts in player.get("pet_mutations",{}).items():
                for m,c in muts.items(): print(f"- {m} {PET_DATA.get(p,{}).get('name',p)} x{c}")
            input("Press ENTER...")
        elif choice=="5": return


def inventory_menu(scoreboard, player_code):
    player=scoreboard[player_code]
    while True:
        print("\n========== INVENTORY ==========")
        print("1. All items")
        print("2. Tradables")
        print("3. Eggs")
        print("4. Consumables")
        print("5. Lock / unlock an item")
        print("6. Back")
        choice=input("> ").strip()
        if choice=="6": return
        if choice in ("1","2","3","4"):
            for item_id,count in sorted(player.get("inventory",{}).items()):
                if count<=0: continue
                if choice=="2" and item_id not in TRADABLE_ITEMS: continue
                if choice=="3" and item_id not in EGG_DATA: continue
                if choice=="4" and item_id not in SHOP_ITEMS: continue
                name=TRADABLE_ITEMS.get(item_id,EGG_DATA.get(item_id,SHOP_ITEMS.get(item_id,{}))).get("name",item_id)
                lock=" 🔒" if item_id in player.get("inventory_locked",[]) else ""
                print(f"{name}: x{count}{lock}")
            input("Press ENTER...")
        elif choice=="5":
            items=[i for i,c in player.get("inventory",{}).items() if c>0]
            for i,item in enumerate(items,1): print(f"{i}. {item} x{player['inventory'][item]}")
            raw=input("> ").strip()
            if raw.isdigit() and 1<=int(raw)<=len(items):
                item=items[int(raw)-1]
                if item in player["inventory_locked"]: player["inventory_locked"].remove(item)
                else: player["inventory_locked"].append(item)
                save_scoreboard(scoreboard)


def collection_index_menu(scoreboard, player_code):
    player=scoreboard[player_code]
    while True:
        print("\n========== COLLECTION INDEX ==========")
        print(f"Pets: {_unique_pet_count(player)}/{len(PET_DATA)}")
        print(f"Verities: {len(player.get('discovered_verities',[]))}/{len(VERITIES)}")
        print(f"Achievements: {len(player.get('achievements',[]))}/{len(ACHIEVEMENTS)}")
        print("\nPet rarities:")
        counts={}
        for p in player.get("pets",[]):
            r=PET_DATA.get(p,{}).get("rarity","?"); counts[r]=counts.get(r,0)+1
        for rarity in ("Common","Rare","Epic","Legendary","Mythic","Divine","Secret"):
            total=sum(1 for d in PET_DATA.values() if d.get("rarity")==rarity)
            owned=sum(1 for p in set(player.get("pets",[])) if PET_DATA.get(p,{}).get("rarity")==rarity)
            print(f"  {rarity}: {owned}/{total}")
        print("\n1. Pet index  2. Chords index  3. Back")
        c=input("> ").strip()
        if c=="3": return
        if c=="1":
            for p,d in PET_DATA.items(): print(("[X] " if p in player.get("pets",[]) else "[ ] ")+d["name"]+f" [{d['rarity']}]" )
            input("Press ENTER...")
        elif c=="2":
            owned=set(player.get("discovered_verities",[]))
            for v in VERITIES: print(("[X] " if v in owned else "[ ] ???" if v not in owned else "")+ (v if v in owned else ""))
            input("Press ENTER...")


def check_story_quests(player, scoreboard=None):
    stats={
        "pet_count": _unique_pet_count(player), "fusions": player.get("fusions",0),
        "mutations": player.get("mutations",0), "secret_pets": sum(1 for p in set(player.get("pets",[])) if PET_DATA.get(p,{}).get("rarity")=="Secret"),
        "verities_discovered": len(player.get("discovered_verities",[])), "market_purchases": player.get("market_purchases",0),
        "casino_vip": player.get("casino_vip",0), "prestige": player.get("prestige",0)
    }
    for qid,(name,desc,stat,threshold,reward_item,reward_amt) in STORY_QUESTS.items():
        if player.get("story_flags",{}).get(qid): continue
        if stats.get(stat,0)>=threshold:
            player["story_flags"][qid]=True; add_item(player,reward_item,reward_amt)
            print(color(player,f"\n📜 QUEST COMPLETE: {name} — {desc}","accent"))
            print(f"Reward: {TRADABLE_ITEMS.get(reward_item,{}).get('name',reward_item)} x{reward_amt}")
    if scoreboard is not None: save_scoreboard(scoreboard)


def quest_menu(scoreboard, player_code):
    player=scoreboard[player_code]; check_story_quests(player,scoreboard)
    print("\n========== STORY QUESTS ==========")
    for qid,(name,desc,stat,threshold,reward,amount) in STORY_QUESTS.items():
        status="COMPLETE" if player.get("story_flags",{}).get(qid) else f"{player.get(stat,0)}/{threshold}"
        print(f"{'[X]' if status=='COMPLETE' else '[ ]'} {name}: {desc} ({status})")
    input("\nPress ENTER...")


def _market_remove_pet(player, pet_id):
    if pet_id not in player.get("pets",[]): return False
    if pet_id==player.get("active_pet"): return False
    if pet_id in player.get("pet_locked",[]) or pet_id in player.get("favorite_pets",[]): return False
    copies=player.get("pet_duplicates",{}).get(pet_id,0)
    if copies>0: player["pet_duplicates"][pet_id]=copies-1
    else: player["pets"].remove(pet_id)
    return True


def marketplace_menu(scoreboard, player_code):
    listings=scoreboard.setdefault("_marketplace",[]); player=scoreboard[player_code]
    while True:
        print("\n========== PLAYER MARKETPLACE ==========")
        print("1. Browse listings")
        print("2. List an item")
        print("3. List a pet copy")
        print("4. Cancel my listing")
        print("5. Back")
        c=input("> ").strip()
        if c=="5": return
        if c=="1":
            if not listings: print("No listings yet.")
            for i,l in enumerate(listings,1): print(f"{i}. {l['name']} [{l['kind']}] — {l['price']} Pointys — seller {l['seller_name']}")
            if listings:
                raw=input("Buy listing # (ENTER to cancel): ").strip()
                if raw.isdigit() and 1<=int(raw)<=len(listings):
                    l=listings[int(raw)-1]
                    if l["seller"]==player_code: print("You cannot buy your own listing."); continue
                    if player["coins"]<l["price"]: print("Not enough Pointys."); continue
                    seller=scoreboard.get(l["seller"])
                    if not isinstance(seller,dict): continue
                    player["coins"]-=l["price"]; seller["coins"]+=l["price"]
                    if l["kind"]=="item": add_item(player,l["asset"],l["amount"])
                    elif l["kind"]=="pet": player["pets"].append(l["asset"])
                    listings.remove(l); player["market_purchases"]+=1; seller["market_sales"]+=1
                    check_story_quests(player,scoreboard); save_scoreboard(scoreboard); print("Purchase complete!")
        elif c=="2":
            options=[i for i,n in player.get("inventory",{}).items() if n>0 and i not in player.get("inventory_locked",[])]
            for i,item in enumerate(options,1): print(f"{i}. {item} x{player['inventory'][item]}")
            raw=input("Item #: ").strip()
            if not raw.isdigit() or not 1<=int(raw)<=len(options): continue
            item=options[int(raw)-1]
            try: price=int(input("Price: ")); amount=int(input("Amount: "))
            except ValueError: continue
            if price<=0 or amount<=0 or inv_count(player,item)<amount: continue
            remove_count=min(amount,inv_count(player,item)); player["inventory"][item]-=remove_count
            listings.append({"seller":player_code,"seller_name":player["name"],"kind":"item","asset":item,"amount":remove_count,"price":price,"id":secrets.token_hex(6)})
            player["market_listings_created"]+=1; save_scoreboard(scoreboard)
        elif c=="3":
            options=[p for p in sorted(set(player.get("pets",[]))) if p!=player.get("active_pet") and p not in player.get("pet_locked",[]) and p not in player.get("favorite_pets",[])]
            for i,p in enumerate(options,1): print(f"{i}. {PET_DATA[p]['name']} x{pet_copy_count(player,p)+1}")
            raw=input("Pet #: ").strip()
            if not raw.isdigit() or not 1<=int(raw)<=len(options): continue
            pet=options[int(raw)-1]
            try: price=int(input("Price: "))
            except ValueError: continue
            if price<=0 or not _market_remove_pet(player,pet): continue
            listings.append({"seller":player_code,"seller_name":player["name"],"kind":"pet","asset":pet,"amount":1,"price":price,"id":secrets.token_hex(6)})
            player["market_listings_created"]+=1; save_scoreboard(scoreboard)
        elif c=="4":
            own=[l for l in listings if l["seller"]==player_code]
            for i,l in enumerate(own,1): print(f"{i}. {l['name'] if 'name' in l else l['asset']} {l['price']}")
            raw=input("Listing #: ").strip()
            if raw.isdigit() and 1<=int(raw)<=len(own):
                l=own[int(raw)-1]
                if l["kind"]=="item": add_item(player,l["asset"],l["amount"])
                else: player["pets"].append(l["asset"])
                listings.remove(l); save_scoreboard(scoreboard)


def casino_vip_rank(player):
    wager=player.get("casino_wagered",0)
    if wager>=100000: return 5
    if wager>=25000: return 4
    if wager>=5000: return 3
    if wager>=1000: return 2
    if wager>=250: return 1
    return 0


def casino_status_menu(scoreboard,player_code):
    p=scoreboard[player_code]
    p["casino_vip"]=casino_vip_rank(p)
    print("\n========== CASINO VIP & STATS ==========")
    print(f"VIP Rank: {p['casino_vip']}/5")
    print(f"Wagered: {p.get('casino_wagered',0)} | Profit: {p.get('casino_profit',0)}")
    print(f"Best win: {p.get('casino_biggest_win',0)} | Biggest loss: {p.get('casino_biggest_loss',0)}")
    print(f"Win streak: {p.get('casino_streak',0)} | Best streak: {p.get('casino_best_streak',0)}")
    print(f"Jackpots hit: {p.get('casino_jackpots_hit',0)} | Current jackpot: {p.get('casino_jackpot',500)}")
    print("VIP rewards: higher jackpot chance, cosmetic titles, and better casino bonus multipliers.")
    save_scoreboard(scoreboard); input("Press ENTER...")

_old_casino_result=casino_result
def casino_result(player, scoreboard, bet, net, name):
    # Apply pet/VIP bonuses to wins only, while preserving the original accounting.
    vip=casino_vip_rank(player)
    casino_bonus=1.0 + (0.02*vip) + (0.02*pet_bonus(player,"casino"))
    if net>0: net=int(net*casino_bonus)
    player["casino_wagered"]=int(player.get("casino_wagered",0))+int(bet)
    player["casino_vip"]=vip
    player["casino_streak"]=player.get("casino_streak",0)+1 if net>0 else 0
    player["casino_best_streak"]=max(player.get("casino_best_streak",0),player["casino_streak"])
    if net>0: player["casino_biggest_win"]=max(player.get("casino_biggest_win",0),net)
    if net<0: player["casino_biggest_loss"]=max(player.get("casino_biggest_loss",0),abs(net))
    player.setdefault("casino_history",[]).append({"game":name,"bet":bet,"net":net,"time":int(time.time())})
    player["casino_history"]=player["casino_history"][-50:]
    # Progressive jackpot grows with play and has a small chance to trigger on a win.
    player["casino_jackpot"]=int(player.get("casino_jackpot",500)+max(1,bet//20))
    if net>0 and random.random() < min(0.001 + vip*0.0005,0.01):
        jackpot=player["casino_jackpot"]; net+=jackpot; player["casino_jackpot"]=500; player["casino_jackpots_hit"]+=1
        print(color(player,f"🎰 PROGRESSIVE JACKPOT! +{jackpot} Pointys!","accent"))
    result=_old_casino_result(player,scoreboard,bet,net,name)
    player["casino_sessions"]=player.get("casino_sessions",0)+1
    check_story_quests(player,scoreboard)
    return result


def casino_menu(scoreboard,player_code):
    games=[("1","Blackjack",blackjack_mode),("2","Five Card Poker",poker_mode),("3","Coin Flip",coin_flip_game),("4","Roulette",roulette_game),("5","Slots",slots_game),("6","Baccarat",baccarat_game),("7","Craps / Dice",dice_sum_game),("8","Sic Bo",dice_sum_game),("9","Casino War",war_game),("10","Red Dog",red_dog_game),("11","High Card",high_card_game),("12","Big Six Wheel",big_six_game),("13","Keno",keno_game),("14","Bingo",bingo_game),("15","Three Card Poker",three_card_poker_game),("16","Pai Gow",pai_gow_game)]
    while True:
        player=scoreboard[player_code]; print("\n========== CASINO =========="); print(f"Pointys: {player['coins']} | VIP {casino_vip_rank(player)}/5 | Jackpot {player.get('casino_jackpot',500)}")
        for n,name,_ in games: print(f"{n}. {name}")
        print("17. VIP / Casino Stats")
        print("18. Back")
        choice=input("> ").strip()
        if choice=="18": return
        if choice=="17": casino_status_menu(scoreboard,player_code); continue
        game=next((g for g in games if g[0]==choice),None)
        if game: game[2](scoreboard,player_code)
        else: print("Invalid option.")


def toggle_pet_lock(player, pet_id):
    locks=player.setdefault("pet_locked",[])
    if pet_id in locks: locks.remove(pet_id); return False
    locks.append(pet_id); return True


def toggle_pet_favorite(player, pet_id):
    fav=player.setdefault("favorite_pets",[])
    if pet_id in fav: fav.remove(pet_id); return False
    fav.append(pet_id); return True


def pet_menu(scoreboard,player_code):
    player=scoreboard[player_code]
    while True:
        active=player.get("active_pet","")
        print("\n========== PETS ==========")
        print(f"Active: {pet_display_name(*parse_pet_key(active)) if active else '(none)'}")
        print(f"Unique: {_unique_pet_count(player)}/{len(PET_DATA)} | Mutations: {player.get('mutations',0)}")
        print("1. Hatch an egg")
        print("2. Equip a pet")
        print("3. Collection")
        print("4. Pet Lab")
        print("5. Lock / favorite pets")
        print("6. Back")
        c=input("> ").strip()
        if c=="6": return
        if c=="1": hatch_egg(player,scoreboard)
        elif c=="2":
            options=sorted(set(player.get("pets",[])))
            for i,p in enumerate(options,1): print(f"{i}. {PET_DATA[p]['name']} [{PET_DATA[p]['rarity']}] Lv.{pet_level(player,p)}")
            raw=input("> ").strip()
            if raw.isdigit() and 1<=int(raw)<=len(options):
                player["active_pet"]=options[int(raw)-1]; save_scoreboard(scoreboard)
        elif c=="3": collection_index_menu(scoreboard,player_code)
        elif c=="4": pet_lab_menu(scoreboard,player_code)
        elif c=="5":
            options=sorted(set(player.get("pets",[])))
            for i,p in enumerate(options,1): print(f"{i}. {PET_DATA[p]['name']} | {'LOCKED' if p in player.get('pet_locked',[]) else 'unlocked'} | {'FAVORITE' if p in player.get('favorite_pets',[]) else ''}")
            raw=input("Pet #: ").strip()
            if raw.isdigit() and 1<=int(raw)<=len(options):
                p=options[int(raw)-1]; print("1. Toggle lock  2. Toggle favorite"); x=input("> ").strip()
                if x=="1": toggle_pet_lock(player,p)
                elif x=="2": toggle_pet_favorite(player,p)
                save_scoreboard(scoreboard)


def progression_menu(scoreboard,player_code):
    player=scoreboard[player_code]
    while True:
        check_story_quests(player,scoreboard)
        print("\n========== PROGRESSION ==========")
        print(f"Lv.{player['level']} | Prestige {player.get('prestige',0)} | {xp_progress_text(player)}")
        print("1. Story quests")
        print("2. Collection index")
        print("3. Inventory")
        print("4. Pet Lab")
        print("5. Marketplace")
        print("6. Casino VIP / Stats")
        print("7. Chords discoveries")
        print("8. Back")
        c=input("> ").strip()
        if c=="8": return
        if c=="1": quest_menu(scoreboard,player_code)
        elif c=="2": collection_index_menu(scoreboard,player_code)
        elif c=="3": inventory_menu(scoreboard,player_code)
        elif c=="4": pet_lab_menu(scoreboard,player_code)
        elif c=="5": marketplace_menu(scoreboard,player_code)
        elif c=="6": casino_status_menu(scoreboard,player_code)
        elif c=="7":
            owned=set(player.get("discovered_verities",[]))
            print("\nCHORDS DISCOVERIES")
            for v in VERITIES: print(f"[X] {v}" if v in owned else "[ ] ???")
            input("Press ENTER...")

_old_add_xp=add_xp
def add_xp(player,amount,scoreboard=None):
    result=_old_add_xp(player,amount,scoreboard)
    grant_pet_xp(player,max(1,int(amount*0.10)),scoreboard)
    check_story_quests(player,scoreboard)
    return result

_old_prestige_player=prestige_player
def prestige_player(scoreboard,player_code):
    result=_old_prestige_player(scoreboard,player_code)
    if result:
        p=scoreboard[player_code]; p.setdefault("prestige_history",[]).append(int(time.time())); check_story_quests(p,scoreboard); save_scoreboard(scoreboard)
    return result

# Add pet mutation chance to hatching without rewriting the original hatch UI.
_old_hatch_egg=hatch_egg
def hatch_egg(player,scoreboard):
    before=set(player.get("pets",[])); old_active=player.get("active_pet","")
    _old_hatch_egg(player,scoreboard)
    pet=player.get("active_pet","")
    if pet and pet in PET_DATA:
        mutation=mutate_pet(player,pet,scoreboard)
        grant_pet_xp(player,25,scoreboard)
        if mutation: print(color(player,f"✨ MUTATION! Your {PET_DATA[pet]['name']} became {mutation}-touched!","accent"))
        check_story_quests(player,scoreboard)
        save_scoreboard(scoreboard)

# Safer Chords discovery wrapper for achievements and the collection index.
_old_discover_chord=discover_chord
def discover_chord(player,word,scoreboard=None):
    before=len(player.setdefault("discovered_verities",[]))
    _old_discover_chord(player,word,scoreboard)
    after=len(player["discovered_verities"])
    if after>before:
        player["verities_discovered"]=after
        player["random_events_triggered"]=player.get("random_events_triggered",0)
        add_item(player,"achievement_medal",1) if after in (10,25,50,len(VERITIES)) else None
        check_story_quests(player,scoreboard)
        save_scoreboard(scoreboard)

# Replace the lobby with the expanded navigation while retaining every old menu.
def lobby(scoreboard,player_code):
    while True:
        player=scoreboard[player_code]; check_story_quests(player,scoreboard)
        print("\n=================================")
        print("          CHORDS LOBBY")
        print("=================================")
        print(f"Player: {display_name(player)} | Lv.{player['level']} | Prestige {player.get('prestige',0)}")
        print(f"Pointys: {player['coins']} | XP: {xp_progress_text(player)} | Pets: {_unique_pet_count(player)}/{len(PET_DATA)}")
        print(f"Achievements: {len(player['achievements'])}/{len(ACHIEVEMENTS)} | Verities: {len(player.get('discovered_verities',[]))}/{len(VERITIES)}")
        print("\n1. Games")
        print("2. Pets")
        print("3. Pointy Shop")
        print("4. Progression / Collection")
        print("5. Profile")
        print("6. Leaderboard")
        print("7. Gifting / Trading")
        print("8. Settings")
        print("9. Prestige / Rebirth")
        print("10. Change player")
        print("11. Quit")
        c=input("\n> ").strip()
        if c=="1": games_menu(scoreboard,player_code)
        elif c=="2": pet_menu(scoreboard,player_code)
        elif c=="3": shop_menu(scoreboard,player_code)
        elif c=="4": progression_menu(scoreboard,player_code)
        elif c=="5": profile_menu(scoreboard,player_code)
        elif c=="6": show_leaderboard(scoreboard)
        elif c=="7": social_menu(scoreboard,player_code)
        elif c=="8": settings_menu(scoreboard,player_code)
        elif c=="9": prestige_player(scoreboard,player_code)
        elif c=="10":
            new_code=login_player(scoreboard)
            if new_code: player_code=new_code
        elif c=="11": save_scoreboard(scoreboard); print("\nThanks for playing Chords!"); return
        else: print("Invalid option.")



# ============================================================
# V2.1 POLISH: ACHIEVEMENTS / CURRENCIES / BANK / MARKET REPUTATION
# ============================================================

_ACH_V2 = {
    "pet_level_10": ("Growing Friend", "Level an active pet to 10.", "xp", 300),
    "pet_level_50": ("Veteran Pet", "Level an active pet to 50.", "xp", 1500),
    "pet_level_100": ("Max Bond", "Level an active pet to 100.", "item", "achievement_medal"),
    "first_fusion": ("Pet Alchemist", "Complete your first pet fusion.", "item", "mystery_token"),
    "first_evolution": ("Evolution", "Evolve a pet for the first time.", "item", "golden_ticket"),
    "first_mutation": ("Mutant", "Obtain your first pet mutation.", "item", "rainbow_ticket"),
    "mutations_10": ("Genetic Chaos", "Obtain 10 pet mutations.", "item", "void_shard"),
    "market_first": ("Market Day", "Make your first marketplace purchase.", "pointys", 100),
    "market_10": ("Master Merchant", "Complete 10 marketplace purchases.", "xp", 1000),
    "market_sales_10": ("Seller", "Complete 10 marketplace sales.", "item", "trade_gem"),
    "chord_25": ("Chords Hunter", "Discover 25 Verities.", "item", "achievement_medal"),
    "chord_all": ("Chords Encyclopedia", "Discover every Chords.", "item", "secret_coin"),
    "casino_vip_3": ("Casino VIP", "Reach Casino VIP rank 3.", "item", "jackpot_chip"),
    "casino_vip_5": ("Casino Legend", "Reach Casino VIP rank 5.", "item", "secret_coin"),
    "jackpot_hit": ("Jackpot!", "Hit a progressive casino jackpot.", "xp", 2500),
    "casino_streak_10": ("Hot Table", "Win 10 casino games in a row.", "xp", 1500),
    "bank_1000": ("Vault Keeper", "Have 1,000 Pointys safely stored in the vault.", "xp", 500),
    "currency_collector": ("Currency Collector", "Own at least 10 gems, 10 tokens, and 5 void currency.", "item", "achievement_medal"),
    "story_5": ("Story Complete", "Complete 5 story quests.", "xp", 2000),
}
for _k,_v in _ACH_V2.items():
    ACHIEVEMENTS[_k]={"name":_v[0],"description":_v[1],"reward_type":_v[2],"reward":_v[3]}

_V2_ACH_IDS=set(_ACH_V2)
_old_check_achievements=check_achievements
def check_achievements(player,scoreboard=None,perfect_game=False):
    _old_check_achievements(player,scoreboard,perfect_game)
    levels=[pet_level(player,p) for p in set(player.get("pets",[])) if p in PET_DATA]
    extra={
        "pet_level_10": max(levels or [0])>=10,
        "pet_level_50": max(levels or [0])>=50,
        "pet_level_100": max(levels or [0])>=100,
        "first_fusion": player.get("fusions",0)>=1,
        "first_evolution": player.get("evolutions",0)>=1,
        "first_mutation": player.get("mutations",0)>=1,
        "mutations_10": player.get("mutations",0)>=10,
        "market_first": player.get("market_purchases",0)>=1,
        "market_10": player.get("market_purchases",0)>=10,
        "market_sales_10": player.get("market_sales",0)>=10,
        "chord_25": len(player.get("discovered_verities",[]))>=25,
        "chord_all": len(player.get("discovered_verities",[]))>=len(VERITIES),
        "casino_vip_3": casino_vip_rank(player)>=3,
        "casino_vip_5": casino_vip_rank(player)>=5,
        "jackpot_hit": player.get("casino_jackpots_hit",0)>=1,
        "casino_streak_10": player.get("casino_best_streak",0)>=10,
        "bank_1000": player.get("bank_coins",0)>=1000,
        "currency_collector": player.get("currency_gems",0)>=10 and player.get("currency_tokens",0)>=10 and player.get("currency_void",0)>=5,
        "story_5": sum(1 for x in player.get("story_flags",{}).values() if x)>=5,
    }
    for aid,ok in extra.items():
        if ok: unlock_achievement(player,aid,scoreboard)

# Extend defaults with bank/trade reputation and auction data.
def _v2_2_defaults():
    return {"bank_coins":0,"bank_deposited_total":0,"bank_interest_claimed":0,"bank_last_claim":0,
            "trade_reputation":0,"auction_wins":0,"auction_bids":0,"auction_listings":[],
            "limited_items":[]}
_old_default_stats_v21=default_stats
def default_stats():
    d=_old_default_stats_v21(); d.update(_v2_2_defaults()); return d
_old_migrate_v21=migrate_player
def migrate_player(player):
    _old_migrate_v21(player)
    for k,v in _v2_2_defaults().items():
        if k not in player: player[k]=list(v) if isinstance(v,list) else v
    if not isinstance(player.get("auction_listings"),list): player["auction_listings"]=[]
    return player


def currency_exchange_menu(scoreboard,player_code):
    p=scoreboard[player_code]
    rates={"1":("Gems", "currency_gems", 100), "2":("Mystery Tokens","currency_tokens",250), "3":("Void Currency","currency_void",1000)}
    while True:
        print("\n========== CURRENCY EXCHANGE ==========")
        print(f"Pointys: {p['coins']} | Gems: {p.get('currency_gems',0)} | Tokens: {p.get('currency_tokens',0)} | Void: {p.get('currency_void',0)}")
        print("1. Buy 1 Gem — 100 Pointys")
        print("2. Buy 1 Mystery Token — 250 Pointys")
        print("3. Buy 1 Void Currency — 1,000 Pointys")
        print("4. Sell 1 Gem — 50 Pointys")
        print("5. Sell 1 Token — 125 Pointys")
        print("6. Sell 1 Void Currency — 500 Pointys")
        print("7. Back")
        c=input("> ").strip()
        buy={"1":("currency_gems",100),"2":("currency_tokens",250),"3":("currency_void",1000)}
        sell={"4":("currency_gems",50),"5":("currency_tokens",125),"6":("currency_void",500)}
        if c=="7": return
        if c in buy:
            k,cost=buy[c]
            if p["coins"]>=cost: p["coins"]-=cost; p[k]+=1; save_scoreboard(scoreboard)
            else: print("Not enough Pointys.")
        elif c in sell:
            k,value=sell[c]
            if p.get(k,0)>0: p[k]-=1; p["coins"]+=value; save_scoreboard(scoreboard)
            else: print("You don't own that currency.")


def bank_menu(scoreboard,player_code):
    p=scoreboard[player_code]
    while True:
        print("\n========== POINTY VAULT ==========")
        print(f"Wallet: {p['coins']} | Vault: {p.get('bank_coins',0)}")
        print("Vault interest is 1% per completed 10-game session (capped at 10,000 vault interest per claim).")
        print("1. Deposit Pointys")
        print("2. Withdraw Pointys")
        print("3. Claim vault interest")
        print("4. Back")
        c=input("> ").strip()
        if c=="4": return
        if c in ("1","2"):
            try:n=int(input("Amount: "))
            except ValueError: continue
            if n<=0: continue
            if c=="1" and p["coins"]>=n: p["coins"]-=n; p["bank_coins"]+=n; p["bank_deposited_total"]+=n
            elif c=="2" and p.get("bank_coins",0)>=n: p["bank_coins"]-=n; p["coins"]+=n
            else: print("Insufficient balance.")
            save_scoreboard(scoreboard)
        elif c=="3":
            sessions=p.get("casino_sessions",0)+p.get("games",0)
            last=p.get("bank_interest_claimed",0)
            if sessions<=last: print("No new vault interest yet.")
            else:
                periods=max(1,(sessions-last)//10); interest=min(10000,int(p.get("bank_coins",0)*0.01*periods))
                p["bank_coins"]+=interest; p["bank_interest_claimed"]=sessions; print(f"Interest added: {interest} Pointys."); save_scoreboard(scoreboard)


def auction_menu(scoreboard,player_code):
    # Lightweight sealed-auction board built on the same persistent marketplace data.
    listings=scoreboard.setdefault("_marketplace",[]); p=scoreboard[player_code]
    while True:
        print("\n========== AUCTIONS ==========")
        auctions=[x for x in listings if x.get("mode")=="auction"]
        if not auctions: print("No auctions available.")
        for i,a in enumerate(auctions,1): print(f"{i}. {a['name']} | bid {a.get('bid',a['price'])} | seller {a['seller_name']}")
        print("\n1. Bid on auction")
        print("2. Back")
        c=input("> ").strip()
        if c=="2": return
        if c=="1" and auctions:
            raw=input("Auction #: ").strip()
            if not raw.isdigit() or not 1<=int(raw)<=len(auctions): continue
            a=auctions[int(raw)-1]
            try: bid=int(input("Your bid: "))
            except ValueError: continue
            if bid<=a.get("bid",a["price"]) or bid>p["coins"]: continue
            a["bid"]=bid; a["bidder"]=player_code; a["bidder_name"]=p["name"]; p["auction_bids"]+=1; save_scoreboard(scoreboard); print("Bid placed. The current leader is stored on the listing.")


def marketplace_menu(scoreboard,player_code):
    listings=scoreboard.setdefault("_marketplace",[]); player=scoreboard[player_code]
    while True:
        print("\n========== PLAYER MARKETPLACE ==========")
        print("1. Browse / buy")
        print("2. List an item")
        print("3. List a pet copy")
        print("4. Create an auction")
        print("5. Browse auctions")
        print("6. Cancel my listing")
        print("7. Back")
        c=input("> ").strip()
        if c=="7": return
        if c=="5": auction_menu(scoreboard,player_code); continue
        if c=="1":
            normal=[l for l in listings if l.get("mode","sale")=="sale"]
            for i,l in enumerate(normal,1): print(f"{i}. {l.get('name',l['asset'])} — {l['price']} Pointys — {l['seller_name']}")
            raw=input("Listing #: ").strip()
            if raw.isdigit() and 1<=int(raw)<=len(normal):
                l=normal[int(raw)-1]
                if l["seller"]==player_code or player["coins"]<l["price"]: continue
                seller=scoreboard.get(l["seller"])
                if not isinstance(seller,dict): continue
                player["coins"]-=l["price"]; seller["coins"]+=l["price"]
                if l["kind"]=="item": add_item(player,l["asset"],l["amount"])
                else: player["pets"].append(l["asset"])
                listings.remove(l); player["market_purchases"]+=1; player["trade_reputation"]+=1; seller["market_sales"]+=1; seller["trade_reputation"]+=1
                check_story_quests(player,scoreboard); check_achievements(player,scoreboard); save_scoreboard(scoreboard)
        elif c in ("2","3"):
            if c=="2":
                options=[i for i,n in player.get("inventory",{}).items() if n>0 and i not in player.get("inventory_locked",[])]
                for i,x in enumerate(options,1): print(f"{i}. {x} x{player['inventory'][x]}")
                raw=input("Item #: ").strip()
                if not raw.isdigit() or not 1<=int(raw)<=len(options): continue
                asset=options[int(raw)-1]
                try: amount=int(input("Amount: ")); price=int(input("Price: "))
                except ValueError: continue
                if amount<=0 or price<=0 or inv_count(player,asset)<amount: continue
                player["inventory"][asset]-=amount; name=TRADABLE_ITEMS.get(asset,EGG_DATA.get(asset,SHOP_ITEMS.get(asset,{}))).get("name",asset)
                listings.append({"seller":player_code,"seller_name":player["name"],"kind":"item","asset":asset,"amount":amount,"price":price,"name":name,"mode":"sale","id":secrets.token_hex(6)})
            else:
                options=[p for p in sorted(set(player.get("pets",[]))) if p!=player.get("active_pet") and p not in player.get("pet_locked",[]) and p not in player.get("favorite_pets",[])]
                for i,x in enumerate(options,1): print(f"{i}. {PET_DATA[x]['name']}")
                raw=input("Pet #: ").strip()
                if not raw.isdigit() or not 1<=int(raw)<=len(options): continue
                asset=options[int(raw)-1]
                try: price=int(input("Price: "))
                except ValueError: continue
                if price<=0 or not _market_remove_pet(player,asset): continue
                listings.append({"seller":player_code,"seller_name":player["name"],"kind":"pet","asset":asset,"amount":1,"price":price,"name":PET_DATA[asset]["name"],"mode":"sale","id":secrets.token_hex(6)})
            player["market_listings_created"]+=1; save_scoreboard(scoreboard)
        elif c=="4":
            options=[i for i,n in player.get("inventory",{}).items() if n>0 and i not in player.get("inventory_locked",[])]
            for i,x in enumerate(options,1): print(f"{i}. {x} x{player['inventory'][x]}")
            raw=input("Item #: ").strip()
            if not raw.isdigit() or not 1<=int(raw)<=len(options): continue
            asset=options[int(raw)-1]
            try: amount=int(input("Amount: ")); start=int(input("Starting bid: "))
            except ValueError: continue
            if amount<=0 or start<=0 or inv_count(player,asset)<amount: continue
            player["inventory"][asset]-=amount; name=TRADABLE_ITEMS.get(asset,EGG_DATA.get(asset,SHOP_ITEMS.get(asset,{}))).get("name",asset)
            listings.append({"seller":player_code,"seller_name":player["name"],"kind":"item","asset":asset,"amount":amount,"price":start,"bid":start,"name":name,"mode":"auction","id":secrets.token_hex(6)})
            player["auction_listings"].append(listings[-1]["id"]); save_scoreboard(scoreboard)
        elif c=="6":
            own=[l for l in listings if l["seller"]==player_code]
            for i,l in enumerate(own,1): print(f"{i}. {l.get('name',l['asset'])} — {l.get('mode','sale')}")
            raw=input("Listing #: ").strip()
            if raw.isdigit() and 1<=int(raw)<=len(own):
                l=own[int(raw)-1]
                if l.get("mode")=="auction" and l.get("bidder"): print("That auction already has a bidder."); continue
                if l["kind"]=="item": add_item(player,l["asset"],l["amount"])
                else: player["pets"].append(l["asset"])
                listings.remove(l); save_scoreboard(scoreboard)

# Final progression menu adds the bank and exchange without adding any worlds.
def progression_menu(scoreboard,player_code):
    player=scoreboard[player_code]
    while True:
        check_story_quests(player,scoreboard); check_achievements(player,scoreboard)
        print("\n========== PROGRESSION ==========")
        print(f"Lv.{player['level']} | Prestige {player.get('prestige',0)} | {xp_progress_text(player)}")
        print(f"Wallet {player['coins']} | Vault {player.get('bank_coins',0)} | Gems {player.get('currency_gems',0)} | Tokens {player.get('currency_tokens',0)} | Void {player.get('currency_void',0)}")
        print("1. Story quests")
        print("2. Collection index")
        print("3. Inventory")
        print("4. Pet Lab")
        print("5. Marketplace / auctions")
        print("6. Casino VIP / Stats")
        print("7. Currency exchange")
        print("8. Pointy vault")
        print("9. Back")
        c=input("> ").strip()
        if c=="9": return
        if c=="1": quest_menu(scoreboard,player_code)
        elif c=="2": collection_index_menu(scoreboard,player_code)
        elif c=="3": inventory_menu(scoreboard,player_code)
        elif c=="4": pet_lab_menu(scoreboard,player_code)
        elif c=="5": marketplace_menu(scoreboard,player_code)
        elif c=="6": casino_status_menu(scoreboard,player_code)
        elif c=="7": currency_exchange_menu(scoreboard,player_code)
        elif c=="8": bank_menu(scoreboard,player_code)


# ============================================================
# MAIN
# ============================================================

def main():
    scoreboard = load_scoreboard()

    while True:
        print("\n=================================")
        print("          CHORDS GAME")
        print("=================================")

        print("\n1. New player")
        print("2. Existing player")
        print("3. Leaderboard")
        print("4. Quit")

        choice = input("\n> ").strip()

        if choice == "1":
            player_code = create_player(scoreboard)
            input("\nPress ENTER to enter the lobby...")
            lobby(scoreboard, player_code)

        elif choice == "2":
            player_code = login_player(scoreboard)
            lobby(scoreboard, player_code)

        elif choice == "3":
            show_leaderboard(scoreboard)

        elif choice == "4":
            save_scoreboard(scoreboard)
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid choice.")



# ============================================================
# V3 SIMPLIFIED UI / PET EVOLUTION FIX
# ============================================================

# Keep the deeper data fields for save compatibility, but remove the
# systems that made the game unnecessarily long: marketplace/auctions,
# bank, currency exchange, story quests, pet mutations/bonding, and VIP UI.


def _ensure_trade_gems(player):
    player.setdefault("inventory", {})
    player.setdefault("pet_duplicates", {})
    player.setdefault("pet_levels", {})
    player.setdefault("pet_xp", {})
    return player


def trade_gem_count(player):
    return inv_count(player, "trade_gem")


def spend_trade_gems(player, amount):
    if trade_gem_count(player) < amount:
        return False
    player["inventory"]["trade_gem"] -= amount
    if player["inventory"]["trade_gem"] <= 0:
        del player["inventory"]["trade_gem"]
    return True


def pet_duplicate_total(player, pet_id):
    # The main copy lives in pets; pet_duplicates stores additional copies.
    return 1 + pet_copy_count(player, pet_id) if pet_id in player.get("pets", []) else pet_copy_count(player, pet_id)


def _evolution_ready(player, pet_id):
    recipe = PET_EVOLUTIONS.get(pet_id)
    if not recipe or pet_id not in player.get("pets", []):
        return False, "That pet cannot evolve yet."
    level, target = recipe
    current = pet_level(player, pet_id)
    if current < level:
        return False, f"{PET_DATA[pet_id]['name']} needs Lv.{level}. It is Lv.{current}."
    # A small, visible crafting cost gives Trade Gems an actual purpose.
    if trade_gem_count(player) < 3:
        return False, "Evolution needs 3 Trade Gems."
    return True, "Ready"


def evolve_pet(player, pet_id, scoreboard=None):
    _ensure_trade_gems(player)
    ready, message = _evolution_ready(player, pet_id)
    if not ready:
        print(message)
        return False

    required_level, target = PET_EVOLUTIONS[pet_id]
    if not spend_trade_gems(player, 3):
        print("Evolution needs 3 Trade Gems.")
        return False

    # Replace the old form rather than silently keeping both.
    try:
        player["pets"].remove(pet_id)
    except ValueError:
        return False
    player.setdefault("pet_duplicates", {}).pop(pet_id, None)

    if target not in player["pets"]:
        player["pets"].append(target)
    player.setdefault("pet_levels", {})[target] = 1
    player.setdefault("pet_xp", {})[target] = 0
    player["active_pet"] = target
    player["evolutions"] = int(player.get("evolutions", 0)) + 1

    print(color(player, f"\n✨ EVOLVED! {PET_DATA[pet_id]['name']} -> {PET_DATA[target]['name']}!", "accent"))
    print("The new pet is now equipped.")
    print("Cost: 3 Trade Gems")
    save_scoreboard(scoreboard)
    check_achievements(player, scoreboard)
    return True


def fuse_pets(player, scoreboard=None):
    _ensure_trade_gems(player)
    candidates = [
        p for p in sorted(set(player.get("pets", [])))
        if p in PET_FUSIONS and pet_duplicate_total(player, p) >= 2
    ]
    if not candidates:
        print("You need a duplicate copy of a fusion pet.")
        return False
    if trade_gem_count(player) < 2:
        print("Fusion needs 2 Trade Gems.")
        return False

    print("\nFUSION RECIPES")
    for i, p in enumerate(candidates, 1):
        print(f"{i}. {PET_DATA[p]['name']} x2 -> {PET_DATA[PET_FUSIONS[p]]['name']} | 2 Gems")
    raw = input("Choose: ").strip()
    if not raw.isdigit() or not 1 <= int(raw) <= len(candidates):
        return False

    source = candidates[int(raw) - 1]
    target = PET_FUSIONS[source]
    if not spend_trade_gems(player, 2):
        print("Fusion needs 2 Trade Gems.")
        return False
    if not remove_pet_copy(player, source) or not remove_pet_copy(player, source):
        # Safety refund if the duplicate bookkeeping cannot complete.
        add_item(player, "trade_gem", 2)
        print("Fusion failed because the duplicate copies were unavailable.")
        return False
    if target not in player["pets"]:
        player["pets"].append(target)
    player["fusions"] = int(player.get("fusions", 0)) + 1
    player["active_pet"] = target
    print(color(player, f"\n✨ FUSION COMPLETE: {PET_DATA[source]['name']} -> {PET_DATA[target]['name']}!", "success"))
    print("Cost: 2 Trade Gems")
    save_scoreboard(scoreboard)
    check_achievements(player, scoreboard)
    return True


def pet_lab_menu(scoreboard, player_code):
    player = scoreboard[player_code]
    while True:
        print("\n========== PET LAB ==========")
        print("Trade Gems: ", trade_gem_count(player))
        print("1. View pet levels")
        print("2. Fuse duplicate pets (2 Gems)")
        print("3. Evolve a pet (3 Gems)")
        print("4. Back")
        choice = input("> ").strip()
        if choice == "4":
            return
        if choice == "1":
            options = sorted(set(player.get("pets", [])))
            if not options:
                print("You do not own any pets.")
            for p in options:
                print(f"- {PET_DATA[p]['name']} [{PET_DATA[p]['rarity']}] Lv.{pet_level(player,p)} | XP {player.get('pet_xp',{}).get(p,0)}")
            input("Press ENTER...")
        elif choice == "2":
            fuse_pets(player, scoreboard)
        elif choice == "3":
            options = [p for p in sorted(set(player.get("pets", []))) if p in PET_EVOLUTIONS]
            if not options:
                print("You do not have an evolvable pet.")
                continue
            for i, p in enumerate(options, 1):
                lvl, target = PET_EVOLUTIONS[p]
                status = "READY" if pet_level(player,p) >= lvl and trade_gem_count(player) >= 3 else f"needs Lv.{lvl} + 3 Gems"
                print(f"{i}. {PET_DATA[p]['name']} Lv.{pet_level(player,p)} -> {PET_DATA[target]['name']} ({status})")
            raw = input("Choose: ").strip()
            if raw.isdigit() and 1 <= int(raw) <= len(options):
                evolve_pet(player, options[int(raw)-1], scoreboard)


def pet_menu(scoreboard, player_code):
    player = scoreboard[player_code]
    while True:
        active = player.get("active_pet", "")
        print("\n========== PETS ==========")
        print(f"Active: {PET_DATA.get(active, {}).get('name', '(none)')}")
        print(f"Pets: {_unique_pet_count(player)}/{len(PET_DATA)} | Trade Gems: {trade_gem_count(player)}")
        print("1. Hatch an egg")
        print("2. Equip a pet")
        print("3. Pet collection")
        print("4. Fuse / evolve")
        print("5. Lock / favorite")
        print("6. Back")
        c = input("> ").strip()
        if c == "6":
            return
        if c == "1":
            hatch_egg(player, scoreboard)
        elif c == "2":
            options = sorted(set(player.get("pets", [])))
            if not options:
                print("You do not own any pets.")
                continue
            for i, p in enumerate(options, 1):
                print(f"{i}. {PET_DATA[p]['name']} [{PET_DATA[p]['rarity']}] Lv.{pet_level(player,p)}")
            raw = input("Choose: ").strip()
            if raw.isdigit() and 1 <= int(raw) <= len(options):
                player["active_pet"] = options[int(raw)-1]
                save_scoreboard(scoreboard)
                print("Pet equipped!")
        elif c == "3":
            collection_index_menu(scoreboard, player_code)
        elif c == "4":
            pet_lab_menu(scoreboard, player_code)
        elif c == "5":
            options = sorted(set(player.get("pets", [])))
            if not options:
                continue
            for i, p in enumerate(options, 1):
                print(f"{i}. {PET_DATA[p]['name']} | {'LOCKED' if p in player.get('pet_locked',[]) else 'unlocked'} | {'FAVORITE' if p in player.get('favorite_pets',[]) else ''}")
            raw = input("Pet #: ").strip()
            if raw.isdigit() and 1 <= int(raw) <= len(options):
                p = options[int(raw)-1]
                print("1. Toggle lock  2. Toggle favorite")
                x = input("> ").strip()
                if x == "1": toggle_pet_lock(player, p)
                elif x == "2": toggle_pet_favorite(player, p)
                save_scoreboard(scoreboard)


def simple_trade_menu(scoreboard, player_code):
    """Simple player-to-player trading. Marketplace/auctions are intentionally removed."""
    player = scoreboard[player_code]
    while True:
        print("\n========== TRADING ==========")
        print("Trade Gems are useful: 2 = pet fusion, 3 = pet evolution.")
        print("1. Gift Pointys")
        print("2. Trade/Gift an item")
        print("3. Trade/Gift a pet")
        print("4. Back")
        c = input("> ").strip()
        if c == "4":
            return
        target_code = input("Target player code: ").strip().upper()
        if target_code not in scoreboard or target_code == player_code:
            print("Invalid target.")
            continue
        target = scoreboard[target_code]
        if c == "1":
            try: amount = int(input("Pointys: "))
            except ValueError: continue
            if amount > 0 and player["coins"] >= amount:
                player["coins"] -= amount; target["coins"] += amount
                save_scoreboard(scoreboard); print("Pointys sent!")
        elif c == "2":
            options = [i for i,n in player.get("inventory",{}).items() if n > 0]
            if not options:
                print("You have no tradeable items."); continue
            for i,x in enumerate(options,1):
                name = TRADABLE_ITEMS.get(x, EGG_DATA.get(x, SHOP_ITEMS.get(x, {}))).get("name", x)
                print(f"{i}. {name} x{inv_count(player,x)}")
            raw = input("Item #: ").strip()
            if raw.isdigit() and 1 <= int(raw) <= len(options):
                item = options[int(raw)-1]
                try: amount = int(input("Amount: "))
                except ValueError: continue
                if 0 < amount <= inv_count(player,item):
                    remove_n = amount
                    player["inventory"][item] -= remove_n
                    if player["inventory"][item] <= 0: del player["inventory"][item]
                    add_item(target,item,amount); save_scoreboard(scoreboard); print("Item sent!")
        elif c == "3":
            options = [p for p in sorted(set(player.get("pets",[]))) if p != player.get("active_pet") and p not in player.get("pet_locked",[]) and p not in player.get("favorite_pets",[])]
            if not options:
                print("No safe pets available to trade."); continue
            for i,p in enumerate(options,1): print(f"{i}. {PET_DATA[p]['name']} [{PET_DATA[p]['rarity']}]")
            raw = input("Pet #: ").strip()
            if raw.isdigit() and 1 <= int(raw) <= len(options):
                pet = options[int(raw)-1]
                if remove_pet_copy(player, pet):
                    if pet not in target["pets"]: target["pets"].append(pet)
                    else: add_item(target, "trade_gem", 1)  # duplicate compensation
                    save_scoreboard(scoreboard); print("Pet sent!")


def progression_menu(scoreboard, player_code):
    player = scoreboard[player_code]
    while True:
        print("\n========== COLLECTION ==========")
        print(f"Pets: {_unique_pet_count(player)}/{len(PET_DATA)} | Verities: {len(player.get('discovered_verities',[]))}/{len(VERITIES)}")
        print("1. Pet / Chords collection")
        print("2. Inventory")
        print("3. Back")
        c = input("> ").strip()
        if c == "3": return
        if c == "1": collection_index_menu(scoreboard, player_code)
        elif c == "2": inventory_menu(scoreboard, player_code)


def lobby(scoreboard, player_code):
    while True:
        player = scoreboard[player_code]
        check_achievements(player, scoreboard)
        print("\n=================================")
        print("          CHORDS LOBBY")
        print("=================================")
        print(f"Player: {display_name(player)} | Lv.{player['level']} | Prestige {player.get('prestige',0)}")
        print(f"Pointys: {player['coins']} | XP: {xp_progress_text(player)} | Pets: {_unique_pet_count(player)}/{len(PET_DATA)}")
        print(f"Achievements: {len(player['achievements'])}/{len(ACHIEVEMENTS)} | Verities: {len(player.get('discovered_verities',[]))}/{len(VERITIES)}")
        print("\n1. Games")
        print("2. Pets")
        print("3. Pointy Shop")
        print("4. Collection / Inventory")
        print("5. Profile / Prestige")
        print("6. Leaderboard")
        print("7. Trading")
        print("8. Settings")
        print("9. Change player")
        print("10. Quit")
        c = input("\n> ").strip()
        if c == "1": games_menu(scoreboard, player_code)
        elif c == "2": pet_menu(scoreboard, player_code)
        elif c == "3": shop_menu(scoreboard, player_code)
        elif c == "4": progression_menu(scoreboard, player_code)
        elif c == "5":
            profile_menu(scoreboard, player_code)
            print("\n1. Prestige / Rebirth  2. Back")
            if input("> ").strip() == "1": prestige_player(scoreboard, player_code)
        elif c == "6": show_leaderboard(scoreboard)
        elif c == "7": simple_trade_menu(scoreboard, player_code)
        elif c == "8": settings_menu(scoreboard, player_code)
        elif c == "9":
            new_code = login_player(scoreboard)
            if new_code: player_code = new_code
        elif c == "10":
            save_scoreboard(scoreboard)
            print("\nThanks for playing Chords!")
            return
        else:
            print("Invalid option.")


# ============================================================
# DEVELOPER ACCOUNT OVERRIDE
# ============================================================

def ensure_dev_account(scoreboard):
    """Create or refresh the DEV account with a complete testing loadout.

    The developer account is intentionally excluded from the public leaderboard,
    but has every gameplay unlock so the game can be tested without grinding.
    """
    if DEV_PLAYER_CODE not in scoreboard or not isinstance(scoreboard.get(DEV_PLAYER_CODE), dict):
        salt, password_hash = hash_password(secrets.token_urlsafe(24))
        scoreboard[DEV_PLAYER_CODE] = create_default_player_data("Developer", salt, password_hash)

    player = scoreboard[DEV_PLAYER_CODE]
    migrate_player(player)
    player["is_dev"] = True
    player["name"] = "Developer"
    player["title"] = "Developer"

    # Currencies / progression.
    player["coins"] = 999_999_999
    player["total_pointys_earned"] = 999_999_999
    player["xp"] = 999_999_999
    player["level"] = 100
    player["prestige"] = 99
    player["prestige_multiplier"] = 1.0 + (99 * PRESTIGE_BONUS)
    player["currency_gems"] = 999_999_999
    player["currency_tokens"] = 999_999_999
    player["currency_void"] = 999_999_999

    # Every permanent upgrade, theme and title.
    player["upgrades"] = sorted(set(
        list(player.get("upgrades", [])) + [
            item_id for item_id, item in SHOP_ITEMS.items()
            if item.get("type") == "upgrade" and item.get("value")
        ]
    ))
    player["owned_themes"] = sorted(set(list(FREE_THEMES) + list(THEMES.keys())))
    player["owned_titles"] = sorted(set(
        [item.get("value") for item in SHOP_ITEMS.values()
         if item.get("type") == "title" and item.get("value")] + ["Developer"]
    ))

    # Every pet, with extra copies available for testing fusion/trading.
    player["pets"] = list(PET_DATA.keys())
    player["pet_duplicates"] = {pet_id: 99 for pet_id in PET_DATA}
    player["pet_levels"] = {pet_id: 100 for pet_id in PET_DATA}
    player["pet_xp"] = {pet_id: 0 for pet_id in PET_DATA}
    player["pet_bond"] = {pet_id: 999 for pet_id in PET_DATA}
    player["pet_locked"] = []
    player["favorite_pets"] = []
    player["active_pet"] = "secret_pointy"

    # Every shop item, egg and tradable, with a generous testing quantity.
    player.setdefault("inventory", {})
    for item_id in SHOP_ITEMS:
        player["inventory"][item_id] = 999
    for egg_id in EGG_DATA:
        player["inventory"][egg_id] = 999
    for item_id in TRADABLE_ITEMS:
        player["inventory"][item_id] = 999

    # Unlock all discoveries and achievements.
    player["achievements"] = list(ACHIEVEMENTS.keys())
    player["discovered_verities"] = list(VERITIES)
    player["verities_discovered"] = len(VERITIES)
    player["fusions"] = 999
    player["evolutions"] = 999
    player["mutations"] = 999
    player["pet_quests"] = {key: True for key in STORY_QUESTS}
    player["story_flags"] = {key: True for key in STORY_QUESTS}

    # Give the dev profile maximum useful casino/testing values too.
    player["casino_vip"] = 99
    player["casino_jackpot"] = 999_999_999
    player["casino_biggest_win"] = 999_999_999
    player["casino_best_streak"] = 999
    player["casino_streak"] = 0
    player["discovered_chords"] = list(CHORDS)

    save_scoreboard(scoreboard)


# ============================================================
# V4 REAL TRADING + NOTIFICATIONS
# ============================================================

# The old "gift" behavior is intentionally replaced by a real two-sided
# trade offer system. Nothing changes hands until the receiver accepts.


def _ensure_social_data(player):
    player.setdefault("notifications", [])
    player.setdefault("trade_offers", [])
    player.setdefault("sent_trade_offers", [])
    return player


def add_notification(player, title, message, kind="info"):
    _ensure_social_data(player)
    player["notifications"].append({
        "title": str(title),
        "message": str(message),
        "kind": str(kind),
        "read": False,
    })
    # Keep saves compact.
    player["notifications"] = player["notifications"][-50:]


def unread_notifications(player):
    _ensure_social_data(player)
    return sum(1 for n in player["notifications"] if not n.get("read", False))


_old_unlock_achievement_v4 = unlock_achievement

def unlock_achievement(player, achievement_id, scoreboard=None):
    already = achievement_id in player.get("achievements", [])
    result = _old_unlock_achievement_v4(player, achievement_id, scoreboard)
    if not already and achievement_id in ACHIEVEMENTS:
        ach = ACHIEVEMENTS[achievement_id]
        add_notification(player, "Achievement unlocked", f"{ach['name']}: {ach['description']}", "achievement")
        if scoreboard is not None:
            save_scoreboard(scoreboard)
    return result


def notifications_menu(scoreboard, player_code):
    refresh_social_state(scoreboard, player_code)
    player = scoreboard[player_code]
    _ensure_social_data(player)
    while True:
        unread = unread_notifications(player)
        print("\n========== NOTIFICATIONS ==========")
        print(f"Unread: {unread}")
        if not player["notifications"]:
            print("You have no notifications.")
        else:
            for i, n in enumerate(reversed(player["notifications"]), 1):
                status = "NEW" if not n.get("read") else "read"
                print(f"{i}. [{status}] {n.get('title','Notification')}")
                print(f"   {n.get('message','')}")
        print("\n1. Mark all as read")
        print("2. Clear notifications")
        print("3. Back")
        c = input("> ").strip()
        if c == "1":
            for n in player["notifications"]:
                n["read"] = True
            save_scoreboard(scoreboard)
            print("All notifications marked as read.")
        elif c == "2":
            player["notifications"] = []
            save_scoreboard(scoreboard)
            print("Notifications cleared.")
        elif c == "3":
            return


def _tradeable_item_ids():
    # Eggs and explicitly tradable collectibles are tradeable. Ordinary
    # consumables/upgrades stay personal so trading cannot bypass progression.
    return set(TRADABLE_ITEMS) | set(EGG_DATA)


def _trade_asset_label(asset):
    kind = asset.get("kind")
    if kind == "pointys":
        return f"{asset.get('amount', 0):,} Pointys"
    if kind == "pet":
        return PET_DATA.get(asset.get("id"), {}).get("name", asset.get("id", "Pet"))
    item_id = asset.get("id", "")
    data = TRADABLE_ITEMS.get(item_id) or EGG_DATA.get(item_id) or SHOP_ITEMS.get(item_id, {})
    return f"{data.get('name', item_id)} x{asset.get('amount', 1)}"


def _parse_trade_assets(player, raw):
    """Parse: pointys:100,item:trade_gem:2,pet:lucky_fox"""
    assets = []
    if not raw.strip():
        return assets, "No assets entered."
    for part in raw.split(","):
        bits = [x.strip() for x in part.split(":")]
        if not bits or not bits[0]:
            continue
        kind = bits[0].lower()
        if kind == "pointys":
            if len(bits) != 2 or not bits[1].isdigit() or int(bits[1]) <= 0:
                return [], "Pointys format: pointys:100"
            amount = int(bits[1])
            if player.get("coins", 0) < amount:
                return [], "You do not have enough Pointys."
            assets.append({"kind": "pointys", "amount": amount})
        elif kind == "item":
            if len(bits) != 3 or not bits[2].isdigit() or int(bits[2]) <= 0:
                return [], "Item format: item:trade_gem:2"
            item_id, amount = bits[1], int(bits[2])
            if item_id not in _tradeable_item_ids():
                return [], f"{item_id} is not tradeable."
            if inv_count(player, item_id) < amount:
                return [], f"You do not have enough {item_id}."
            assets.append({"kind": "item", "id": item_id, "amount": amount})
        elif kind == "pet":
            if len(bits) != 2:
                return [], "Pet format: pet:lucky_fox"
            pet_id = bits[1]
            if pet_id not in player.get("pets", []):
                return [], "You do not own that pet."
            if pet_id == player.get("active_pet"):
                return [], "You cannot trade your active pet."
            if pet_id in player.get("pet_locked", []) or pet_id in player.get("favorite_pets", []):
                return [], "Unlock/unfavorite that pet before trading it."
            assets.append({"kind": "pet", "id": pet_id, "amount": 1})
        else:
            return [], "Use pointys, item, or pet."
    if not assets:
        return [], "No valid assets entered."
    return assets, ""


def _validate_trade_assets(player, assets):
    for asset in assets:
        if asset["kind"] == "pointys":
            if player.get("coins", 0) < asset["amount"]:
                return False, "You no longer have enough Pointys."
        elif asset["kind"] == "item":
            if inv_count(player, asset["id"]) < asset["amount"]:
                return False, f"You no longer have enough {asset['id']}."
        elif asset["kind"] == "pet":
            pet_id = asset["id"]
            if pet_id not in player.get("pets", []):
                return False, "One of the offered pets is no longer owned."
            if pet_id == player.get("active_pet"):
                return False, "An offered pet became your active pet."
            if pet_id in player.get("pet_locked", []) or pet_id in player.get("favorite_pets", []):
                return False, "An offered pet is locked/favorited."
    return True, ""


def _remove_trade_assets(player, assets):
    ok, reason = _validate_trade_assets(player, assets)
    if not ok:
        return False, reason
    for asset in assets:
        if asset["kind"] == "pointys":
            player["coins"] -= asset["amount"]
        elif asset["kind"] == "item":
            player["inventory"][asset["id"]] -= asset["amount"]
            if player["inventory"][asset["id"]] <= 0:
                del player["inventory"][asset["id"]]
        elif asset["kind"] == "pet":
            if not remove_pet_copy(player, asset["id"]):
                return False, "A pet could not be removed safely."
    return True, ""


def _add_trade_assets(player, assets):
    for asset in assets:
        if asset["kind"] == "pointys":
            player["coins"] += asset["amount"]
        elif asset["kind"] == "item":
            add_item(player, asset["id"], asset["amount"])
        elif asset["kind"] == "pet":
            pet_id = asset["id"]
            if pet_id not in player["pets"]:
                player["pets"].append(pet_id)
                player.setdefault("pet_levels", {})[pet_id] = 1
                player.setdefault("pet_xp", {})[pet_id] = 0
            else:
                # A duplicate pet is represented by the duplicate counter.
                player.setdefault("pet_duplicates", {})[pet_id] = pet_copy_count(player, pet_id) + 1


def _trade_summary(assets):
    return ", ".join(_trade_asset_label(a) for a in assets) if assets else "Nothing"


def _next_trade_id(scoreboard):
    scoreboard["__trade_counter__"] = int(scoreboard.get("__trade_counter__", 0)) + 1
    return f"T{scoreboard['__trade_counter__']:06d}"


def create_trade_offer(scoreboard, player_code):
    player = scoreboard[player_code]
    _ensure_social_data(player)
    print("\n========== NEW TRADE ==========")
    target_code = input("Player code to trade with: ").strip().upper()
    if target_code not in scoreboard or target_code.startswith("__") or target_code == player_code:
        print("Invalid target player.")
        return
    target = scoreboard[target_code]
    _ensure_social_data(target)

    print("\nYour side")
    print("Format examples:")
    print("  pointys:500")
    print("  item:trade_gem:3")
    print("  pet:lucky_fox")
    print("  Multiple assets: pointys:500,item:trade_gem:3")
    give_raw = input("You offer: ").strip()
    give, error = _parse_trade_assets(player, give_raw)
    if error:
        print(error)
        return

    print("\nTheir side")
    receive_raw = input("You want: ").strip()
    receive, error = _parse_trade_assets(target, receive_raw)
    if error:
        print("That request cannot be made:", error)
        return

    trade_id = _next_trade_id(scoreboard)
    offer = {
        "id": trade_id,
        "from": player_code,
        "to": target_code,
        "give": give,
        "receive": receive,
        "status": "pending",
    }
    player["sent_trade_offers"].append(offer)
    target["trade_offers"].append(offer)
    add_notification(
        target,
        "New trade offer",
        f"{player.get('name', player_code)} offered {_trade_summary(give)} for {_trade_summary(receive)}. Trade #{trade_id}.",
        "trade",
    )
    save_scoreboard(scoreboard)
    print(f"Trade #{trade_id} sent. Nothing changes until they accept it.")


def _find_trade(scoreboard, player_code, trade_id):
    player = scoreboard[player_code]
    for offer in player.get("trade_offers", []):
        if offer.get("id") == trade_id and offer.get("status") == "pending":
            return offer
    return None


def accept_trade(scoreboard, player_code, trade_id):
    receiver = scoreboard[player_code]
    offer = _find_trade(scoreboard, player_code, trade_id)
    if not offer or offer.get("to") != player_code:
        print("Trade offer not found or already handled.")
        return
    sender_code = offer["from"]
    if sender_code not in scoreboard:
        print("The sender no longer exists.")
        return
    sender = scoreboard[sender_code]
    _ensure_social_data(sender)

    ok, reason = _validate_trade_assets(sender, offer["give"])
    if not ok:
        offer["status"] = "failed"
        add_notification(receiver, "Trade failed", reason, "trade")
        add_notification(sender, "Trade failed", f"Trade #{offer['id']} could not be completed.", "trade")
        save_scoreboard(scoreboard)
        print(reason)
        return
    ok, reason = _validate_trade_assets(receiver, offer["receive"])
    if not ok:
        offer["status"] = "failed"
        add_notification(sender, "Trade failed", f"{receiver.get('name', player_code)} no longer has the requested assets.", "trade")
        add_notification(receiver, "Trade failed", reason, "trade")
        save_scoreboard(scoreboard)
        print(reason)
        return

    # Validate both sides before removing anything, then perform the swap.
    ok, reason = _remove_trade_assets(sender, offer["give"])
    if not ok:
        print("Trade could not be completed safely:", reason)
        return
    ok, reason = _remove_trade_assets(receiver, offer["receive"])
    if not ok:
        # The sender's assets have already moved; restore them before aborting.
        _add_trade_assets(sender, offer["give"])
        print("Trade could not be completed safely. Nothing was changed.")
        return

    _add_trade_assets(receiver, offer["give"])
    _add_trade_assets(sender, offer["receive"])
    offer["status"] = "accepted"

    add_notification(receiver, "Trade completed", f"Trade #{offer['id']} completed successfully.", "trade")
    add_notification(sender, "Trade accepted", f"{receiver.get('name', player_code)} accepted trade #{offer['id']}.", "trade")
    save_scoreboard(scoreboard)
    print(f"Trade #{offer['id']} accepted!")


def reject_trade(scoreboard, player_code, trade_id):
    receiver = scoreboard[player_code]
    offer = _find_trade(scoreboard, player_code, trade_id)
    if not offer or offer.get("to") != player_code:
        print("Trade offer not found or already handled.")
        return
    offer["status"] = "rejected"
    sender_code = offer.get("from")
    if sender_code in scoreboard:
        sender = scoreboard[sender_code]
        _ensure_social_data(sender)
        add_notification(sender, "Trade rejected", f"{receiver.get('name', player_code)} rejected trade #{offer['id']}.", "trade")
    add_notification(receiver, "Trade rejected", f"You rejected trade #{offer['id']}.", "trade")
    save_scoreboard(scoreboard)
    print("Trade rejected.")


def cancel_trade(scoreboard, player_code, trade_id):
    player = scoreboard[player_code]
    for offer in player.get("sent_trade_offers", []):
        if offer.get("id") == trade_id and offer.get("status") == "pending":
            offer["status"] = "cancelled"
            target_code = offer.get("to")
            if target_code in scoreboard:
                target = scoreboard[target_code]
                _ensure_social_data(target)
                add_notification(target, "Trade cancelled", f"{player.get('name', player_code)} cancelled trade #{trade_id}.", "trade")
            save_scoreboard(scoreboard)
            print("Trade cancelled.")
            return
    print("Pending trade not found.")


def incoming_trades_menu(scoreboard, player_code):
    refresh_social_state(scoreboard, player_code)
    player = scoreboard[player_code]
    _ensure_social_data(player)
    pending = [x for x in player["trade_offers"] if x.get("status") == "pending" and x.get("to") == player_code]
    if not pending:
        print("\nYou have no pending trade offers.")
        input("Press ENTER...")
        return
    while True:
        pending = [x for x in player["trade_offers"] if x.get("status") == "pending" and x.get("to") == player_code]
        print("\n========== TRADE OFFERS ==========")
        for i, offer in enumerate(pending, 1):
            sender = scoreboard.get(offer["from"], {}).get("name", offer["from"])
            print(f"{i}. #{offer['id']} from {sender}")
            print(f"   They give: {_trade_summary(offer['give'])}")
            print(f"   They want: {_trade_summary(offer['receive'])}")
        print("0. Back")
        raw = input("Choose offer: ").strip()
        if raw == "0":
            return
        if not raw.isdigit() or not 1 <= int(raw) <= len(pending):
            print("Invalid choice.")
            continue
        offer = pending[int(raw) - 1]
        print(f"\nTrade #{offer['id']}")
        print(f"You give: {_trade_summary(offer['receive'])}")
        print(f"You get:  {_trade_summary(offer['give'])}")
        print("1. Accept")
        print("2. Reject")
        print("3. Back")
        action = input("> ").strip()
        if action == "1":
            accept_trade(scoreboard, player_code, offer["id"])
        elif action == "2":
            reject_trade(scoreboard, player_code, offer["id"])


def sent_trades_menu(scoreboard, player_code):
    refresh_social_state(scoreboard, player_code)
    player = scoreboard[player_code]
    _ensure_social_data(player)
    pending = [x for x in player["sent_trade_offers"] if x.get("status") == "pending"]
    print("\n========== SENT TRADES ==========")
    if not pending:
        print("No pending sent trades.")
    for offer in pending:
        target = scoreboard.get(offer["to"], {}).get("name", offer["to"])
        print(f"#{offer['id']} -> {target}: {_trade_summary(offer['give'])} for {_trade_summary(offer['receive'])}")
    if pending:
        raw = input("Trade ID to cancel (or ENTER to go back): ").strip().upper()
        if raw:
            cancel_trade(scoreboard, player_code, raw)
    else:
        input("Press ENTER...")


def simple_trade_menu(scoreboard, player_code):
    player = scoreboard[player_code]
    _ensure_social_data(player)
    while True:
        incoming = sum(1 for x in player["trade_offers"] if x.get("status") == "pending" and x.get("to") == player_code)
        print("\n========== TRADING ==========")
        print("Trading is now two-sided: send an offer, choose what you want, then the other player accepts or rejects it.")
        print(f"Pending offers: {incoming}")
        print("1. Create trade offer")
        print("2. View / accept / reject offers")
        print("3. View / cancel sent trades")
        print("4. Notifications")
        print("5. Back")
        c = input("> ").strip()
        if c == "1":
            create_trade_offer(scoreboard, player_code)
        elif c == "2":
            incoming_trades_menu(scoreboard, player_code)
        elif c == "3":
            sent_trades_menu(scoreboard, player_code)
        elif c == "4":
            notifications_menu(scoreboard, player_code)
        elif c == "5":
            return


def lobby(scoreboard, player_code):
    while True:
        player = scoreboard[player_code]
        _ensure_social_data(player)
        check_achievements(player, scoreboard)
        unread = unread_notifications(player)
        incoming = sum(1 for x in player["trade_offers"] if x.get("status") == "pending" and x.get("to") == player_code)
        print("\n=================================")
        print("          CHORDS LOBBY")
        print("=================================")
        print(f"Player: {display_name(player)} | Lv.{player['level']} | Prestige {player.get('prestige',0)}")
        print(f"Pointys: {player['coins']} | XP: {xp_progress_text(player)} | Pets: {_unique_pet_count(player)}/{len(PET_DATA)}")
        print(f"Achievements: {len(player['achievements'])}/{len(ACHIEVEMENTS)} | Verities: {len(player.get('discovered_verities',[]))}/{len(VERITIES)}")
        print(f"Notifications: {unread} unread | Trade offers: {incoming} pending")
        print("\n1. Games")
        print("2. Pets")
        print("3. Pointy Shop")
        print("4. Collection / Inventory")
        print("5. Profile / Prestige")
        print("6. Leaderboard")
        print("7. Trading")
        print("8. Notifications")
        print("9. Settings")
        print("10. Change player")
        print("11. Quit")
        c = input("\n> ").strip()
        if c == "1": games_menu(scoreboard, player_code)
        elif c == "2": pet_menu(scoreboard, player_code)
        elif c == "3": shop_menu(scoreboard, player_code)
        elif c == "4": progression_menu(scoreboard, player_code)
        elif c == "5":
            profile_menu(scoreboard, player_code)
            print("\n1. Prestige / Rebirth  2. Back")
            if input("> ").strip() == "1": prestige_player(scoreboard, player_code)
        elif c == "6": show_leaderboard(scoreboard)
        elif c == "7": simple_trade_menu(scoreboard, player_code)
        elif c == "8": notifications_menu(scoreboard, player_code)
        elif c == "9": settings_menu(scoreboard, player_code)
        elif c == "10":
            new_code = login_player(scoreboard)
            if new_code: player_code = new_code
        elif c == "11":
            save_scoreboard(scoreboard)
            print("\nThanks for playing Chords!")
            return
        else:
            print("Invalid option.")


# ============================================================
# V5 PICKER-BASED TRADING + GIFTING
# ============================================================

def _player_choices(scoreboard, player_code):
    return [(code, data) for code, data in scoreboard.items()
            if not str(code).startswith("__") and code != player_code and isinstance(data, dict)]


def _choose_player(scoreboard, player_code, prompt="Choose a player"):
    choices = _player_choices(scoreboard, player_code)
    if not choices:
        print("No other players are available.")
        return None
    print(f"\n========== {prompt.upper()} ==========")
    for i, (code, data) in enumerate(choices, 1):
        print(f"{i}. {display_name(data)} ({code})")
    print("0. Back")
    while True:
        raw = input("> ").strip()
        if raw == "0":
            return None
        if raw.isdigit() and 1 <= int(raw) <= len(choices):
            return choices[int(raw) - 1][0]
        print("Pick a player from the list.")


def _asset_options(player):
    options = []
    coins = int(player.get("coins", 0))
    if coins > 0:
        options.append({"kind": "pointys", "amount": coins})
    for item_id in sorted(_tradeable_item_ids()):
        count = inv_count(player, item_id)
        if count > 0:
            options.append({"kind": "item", "id": item_id, "amount": count})
    for pet_id in sorted(set(player.get("pets", []))):
        if (pet_id == player.get("active_pet") or pet_id in player.get("pet_locked", [])
                or pet_id in player.get("favorite_pets", [])):
            continue
        count = pet_copy_count(player, pet_id)
        if count > 0:
            options.append({"kind": "pet", "id": pet_id, "amount": count})
    return options


def _asset_option_label(asset):
    if asset["kind"] == "pointys":
        return f"💰 Pointys (up to {asset['amount']:,})"
    if asset["kind"] == "item":
        data = TRADABLE_ITEMS.get(asset["id"]) or EGG_DATA.get(asset["id"]) or SHOP_ITEMS.get(asset["id"], {})
        return f"🎁 {data.get('name', asset['id'])} (x{asset['amount']})"
    data = PET_DATA.get(asset["id"], {})
    return f"🐾 {data.get('name', asset['id'])} [{data.get('rarity', 'Unknown')}] (x{asset['amount']})"


def _quantity_choices(max_amount):
    max_amount = max(1, int(max_amount))
    vals = []
    for value in (1, 2, 3, 5, 10, 25, 50, 100, 250, 500, 1000):
        if value <= max_amount and value not in vals:
            vals.append(value)
    if max_amount not in vals:
        vals.append(max_amount)
    return vals


def _choose_quantity(max_amount):
    vals = _quantity_choices(max_amount)
    print("\nChoose quantity:")
    for i, value in enumerate(vals, 1):
        suffix = " (ALL)" if value == max_amount else ""
        print(f"{i}. {value:,}{suffix}")
    print("0. Back")
    while True:
        raw = input("> ").strip()
        if raw == "0":
            return None
        if raw.isdigit() and 1 <= int(raw) <= len(vals):
            return vals[int(raw) - 1]
        print("Pick a quantity from the list.")


def _pick_assets(player, heading, max_assets=8):
    """Choose assets entirely from menus; no asset IDs or amounts need to be typed."""
    chosen = []
    while len(chosen) < max_assets:
        options = _asset_options(player)
        if not options:
            if not chosen:
                print("You have nothing tradeable/giftable.")
            return chosen
        print(f"\n========== {heading.upper()} ==========")
        if chosen:
            print("Selected:")
            for asset in chosen:
                print(f"  • {_trade_asset_label(asset)}")
        for i, asset in enumerate(options, 1):
            print(f"{i}. {_asset_option_label(asset)}")
        print("D. Done")
        print("0. Cancel")
        raw = input("> ").strip().lower()
        if raw == "0":
            return None
        if raw == "d":
            return chosen if chosen else None
        if not raw.isdigit() or not 1 <= int(raw) <= len(options):
            print("Pick an item from the list.")
            continue
        selected = dict(options[int(raw) - 1])
        quantity = _choose_quantity(selected["amount"])
        if quantity is None:
            continue
        selected["amount"] = quantity
        # Pets are individual copies, so selecting one pet at a time is clearer.
        if selected["kind"] == "pet" and quantity > 1:
            print("Pet trades select one pet copy at a time. Choose 1.")
            continue
        chosen.append(selected)
    return chosen


def create_trade_offer(scoreboard, player_code):
    player = scoreboard[player_code]
    _ensure_social_data(player)
    target_code = _choose_player(scoreboard, player_code, "Trade with")
    if not target_code:
        return
    target = scoreboard[target_code]
    _ensure_social_data(target)

    give = _pick_assets(player, "Choose what you will give")
    if give is None:
        return
    receive = _pick_assets(target, "Choose what you want from them")
    if receive is None:
        return

    trade_id = _next_trade_id(scoreboard)
    offer = {
        "id": trade_id, "from": player_code, "to": target_code,
        "give": give, "receive": receive, "status": "pending",
    }
    player["sent_trade_offers"].append(offer)
    target["trade_offers"].append(offer)
    add_notification(target, "New trade offer",
                     f"{player.get('name', player_code)} offered {_trade_summary(give)} for {_trade_summary(receive)}. Trade #{trade_id}.", "trade")
    save_scoreboard(scoreboard)
    print(f"\nTrade #{trade_id} sent! Nothing changes until they accept it.")
    input("Press ENTER...")


def gift_assets(scoreboard, player_code):
    player = scoreboard[player_code]
    _ensure_social_data(player)
    target_code = _choose_player(scoreboard, player_code, "Gift to")
    if not target_code:
        return
    target = scoreboard[target_code]
    _ensure_social_data(target)
    assets = _pick_assets(player, "Choose what to gift", max_assets=1)
    if not assets:
        return
    asset = assets[0]
    print(f"\nGift: {_trade_asset_label(asset)}")
    print("1. Send gift")
    print("2. Cancel")
    if input("> ").strip() != "1":
        return
    ok, reason = _validate_trade_assets(player, [asset])
    if not ok:
        print(reason)
        return
    ok, reason = _remove_trade_assets(player, [asset])
    if not ok:
        print(reason)
        return
    _add_trade_assets(target, [asset])
    add_notification(target, "Gift received",
                     f"{player.get('name', player_code)} gifted you {_trade_summary([asset])}.", "gift")
    add_notification(player, "Gift sent",
                     f"You gifted {target.get('name', target_code)} {_trade_summary([asset])}.", "gift")
    save_scoreboard(scoreboard)
    print("Gift sent!")
    input("Press ENTER...")


def simple_trade_menu(scoreboard, player_code):
    refresh_social_state(scoreboard, player_code)
    player = scoreboard[player_code]
    _ensure_social_data(player)
    while True:
        refresh_social_state(scoreboard, player_code)
        player = scoreboard[player_code]
        pending = sum(1 for x in player.get("trade_offers", []) if x.get("status") == "pending" and x.get("to") == player_code)
        print("\n========== TRADING & GIFTING ==========")
        print("Trade Gems are useful: 2 = fusion, 3 = evolution.")
        print(f"Pending trade offers: {pending}")
        print("1. Create Trade Offer")
        print("2. View Incoming Trades")
        print("3. View My Sent Trades")
        print("4. Gift Something")
        print("5. Back")
        c = input("> ").strip()
        if c == "1":
            create_trade_offer(scoreboard, player_code)
        elif c == "2":
            incoming_trades_menu(scoreboard, player_code)
        elif c == "3":
            sent_trades_menu(scoreboard, player_code)
        elif c == "4":
            gift_assets(scoreboard, player_code)
        elif c == "5":
            return
        else:
            print("Pick an option from the list.")

# ============================================================
# START
# ============================================================



# ============================================================
# CHORDS GAMEPLAY CORE
# Built directly on this version's progression/economy framework.
# The old word/Verity puzzle mechanic is intentionally replaced.
# ============================================================

CHORDS = [
    "C","D","E","F","G","A","B",
    "Cm","Dm","Em","Fm","Gm","Am","Bm",
    "Cdim","Ddim","Edim","Fdim","Gdim","Adim","Bdim",
    "Caug","Daug","Eaug","Faug","Gaug","Aaug","Baug",
    "C7","D7","E7","F7","G7","A7","B7",
    "Cmaj7","Dmaj7","Emaj7","Fmaj7","Gmaj7","Amaj7","Bmaj7",
    "Cm7","Dm7","Em7","Fm7","Gm7","Am7","Bm7",
    "Csus2","Dsus2","Esus2","Fsus2","Gsus2","Asus2","Bsus2",
    "Csus4","Dsus4","Esus4","Fsus4","Gsus4","Asus4","Bsus4",
    "C6","D6","E6","F6","G6","A6","B6",
    "C9","D9","E9","F9","G9","A9","B9",
    "C5","D5","E5","F5","G5","A5","B5",
    "C#","D#","F#","G#","A#","C#m","D#m","F#m","G#m","A#m",
    "Ab","Bb","Db","Eb","Gb","Abm","Bbm","Dbm","Ebm","Gbm",
]

NOTE_INDEX = {
    "C":0, "C#":1, "Db":1, "D":2, "D#":3, "Eb":3,
    "E":4, "F":5, "F#":6, "Gb":6, "G":7, "G#":8,
    "Ab":8, "A":9, "A#":10, "Bb":10, "B":11
}
NOTE_NAMES = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
CHORD_INTERVALS = {
    "": [0,4,7], "m": [0,3,7], "dim": [0,3,6], "aug": [0,4,8],
    "7": [0,4,7,10], "maj7": [0,4,7,11], "m7": [0,3,7,10],
    "sus2": [0,2,7], "sus4": [0,5,7], "6": [0,4,7,9],
    "9": [0,4,7,10,14], "5": [0,7]
}

def _parse_chord(chord):
    root = chord[:2] if len(chord) >= 2 and chord[1] in "#b" else chord[:1]
    suffix = chord[len(root):]
    return root, suffix

def chord_notes(chord):
    root, suffix = _parse_chord(chord)
    root_pc = NOTE_INDEX[root]
    intervals = CHORD_INTERVALS.get(suffix, CHORD_INTERVALS[""])
    return [NOTE_NAMES[(root_pc + i) % 12] for i in intervals]

def _pitch(note):
    note = note.strip().upper()
    aliases = {"DB":"C#","EB":"D#","GB":"F#","AB":"G#","BB":"A#"}
    note = aliases.get(note, note)
    return NOTE_INDEX.get(note)

def _display_chord_notes(chord, visible_count):
    notes = chord_notes(chord)
    visible_count = max(1, min(len(notes), visible_count))
    visible = random.sample(notes, visible_count)
    shown = visible + ["X"] * (len(notes) - visible_count)
    random.shuffle(shown)
    return shown, visible

def _compatible(candidate, visible):
    candidate_pitches = {_pitch(n) for n in chord_notes(candidate)}
    visible_pitches = {_pitch(n) for n in visible}
    return visible_pitches.issubset(candidate_pitches)

def _chord_choices(target, visible):
    # Exactly one valid answer: distractors must be incompatible with
    # the displayed tones.
    candidates = [c for c in CHORDS if c != target and not _compatible(c, visible)]
    target_root = _parse_chord(target)[0]
    different_root = [c for c in candidates if _parse_chord(c)[0] != target_root]
    if len(different_root) >= 3:
        candidates = different_root
    random.shuffle(candidates)
    choices = [target] + candidates[:3]
    if len(choices) < 4:
        # This should not happen with the supplied pool, but keeps the mode safe.
        extras = [c for c in CHORDS if c not in choices]
        choices += extras[:4-len(choices)]
    random.shuffle(choices)
    return choices

def _ask_chord_question(player, target, visible_count, prefix=""):
    shown, visible = _display_chord_notes(target, visible_count)
    choices = _chord_choices(target, visible)

    print(f"\n{prefix}Notes: " + "  ".join(shown))
    print("Which chord is it?")
    for i, choice in enumerate(choices, 1):
        print(f"{i}. {choice}")

    while True:
        answer = input("Answer (1-4, H=hint, L=leaderboard, Q=quit): ").strip().lower()
        if answer == "q" or answer == "quit":
            return None, False, True
        if answer == "l":
            print("\nLeaderboard is available from the lobby.")
            continue
        if answer == "h":
            print(color(player, f"Hint: the root is {_parse_chord(target)[0]}.", "info"))
            continue
        if answer in ("1","2","3","4"):
            selected = choices[int(answer)-1]
            return selected, selected == target, False
        print("Please choose 1, 2, 3, or 4.")

def _chord_visible_count(player):
    return {
        "Easy": 4,
        "Normal": 3,
        "Hard": 2,
        "Extreme": 1,
    }.get(player.get("difficulty", "Normal"), 3)

def choose_difficulty(player):
    options = [
        ("Easy", 0.80, "4 notes shown"),
        ("Normal", 1.00, "3 notes shown"),
        ("Hard", 1.25, "2 notes shown"),
        ("Extreme", 1.60, "1 note shown"),
    ]
    while True:
        print("\n========== DIFFICULTY ==========")
        for i, (name, reward, desc) in enumerate(options, 1):
            print(f"{i}. {name} - {desc} - reward x{reward:.2f}")
        print("5. Back")
        choice = input("> ").strip()
        if choice in ("1","2","3","4"):
            player["difficulty"] = options[int(choice)-1][0]
            return player["difficulty"]
        if choice == "5":
            return None
        print("Invalid option.")

def _finish_chord_game(player, scoreboard, mode, correct, wrong, best_combo,
                       running_pointys=0, xp_base=0, perfect=False):
    if best_combo > player["best_combo"]:
        player["best_combo"] = best_combo
    player["games"] += 1
    bonus = magnet_bonus(player)
    if bonus:
        give_pointys(player, bonus, scoreboard)
        running_pointys += bonus
    xp_earned = max(1, int(xp_base * (1.25 if "xp_booster" in player.get("upgrades", []) else 1)))
    add_xp(player, xp_earned, scoreboard)
    record_history(player, mode, "Perfect" if perfect else "Completed", correct)
    check_achievements(player, scoreboard, perfect)
    save_scoreboard(scoreboard)
    return running_pointys, xp_earned

def play_game(scoreboard, player_code):
    player = scoreboard[player_code]
    banner(player, "CHORDS MODE")
    data = DIFFICULTIES.get(player.get("difficulty", "Normal"), {})
    low, high = data.get("normal_len", (6, 10))
    length = random.randint(low, high)
    visible_count = _chord_visible_count(player)

    print(f"\nQuestions: {length} | Notes shown: {visible_count}")
    print("Pick the correct chord with 1-4. You never type a chord name.")
    print("Type Q at any question to leave the game.")

    boosts = start_boosts(player, scoreboard)
    combo = best_combo = correct = wrong = 0
    running_pointys = 0
    event_xp = 0

    for number in range(1, length + 1):
        target = random.choice(CHORDS)
        event = roll_event(player, boosts)
        attempts = 3 if event and event.get("guesses") else 1
        solved = False

        while attempts:
            selected, ok, quit_game = _ask_chord_question(
                player, target, visible_count, f"Question {number}/{length}"
            )
            if quit_game:
                print("\nGame cancelled.")
                return
            attempts -= 1
            if ok:
                solved = True
                break
            wrong += 1
            player["wrong_answers"] += 1
            player["total_questions"] += 1
            if attempts:
                print(color(player, "Wrong — try again! Combo is safe for this event.", "error"))
            else:
                print(color(player, f"Wrong! The answer was {target}.", "error"))

        if solved:
            correct += 1
            combo += 1
            player["correct_answers"] += 1
            player["total_questions"] += 1
            best_combo = max(best_combo, combo)
            base = combo if combo > 1 else 1
            earned = pointy_reward(base, event, boosts, player)
            give_pointys(player, earned, scoreboard)
            running_pointys += earned
            if event and event.get("xp"):
                event_xp += event["xp"]
            print(color(player, f"Correct! {target}  +{earned} pointys", "success"))
        else:
            combo = handle_miss(player, scoreboard, combo)

    running_pointys, xp_earned = _finish_chord_game(
        player, scoreboard, "chords", correct, wrong, best_combo,
        running_pointys, correct * 5 + event_xp, wrong == 0
    )
    banner(player, "CHORDS COMPLETE!", "success")
    print(f"\nCorrect: {correct}/{length}")
    print(f"Wrong: {wrong}")
    print(f"Best combo: {best_combo}x")
    print(f"+{running_pointys} pointys")
    print(f"+{xp_earned} XP")
    input("\nPress ENTER to return to the lobby...")

def timed_mode(scoreboard, player_code):
    player = scoreboard[player_code]
    banner(player, "TIMED CHORDS")
    total_seconds = difficulty_data(player)["timed"]
    boosts = start_boosts(player, scoreboard, timed=True)
    total_seconds += boosts["extra_seconds"]
    print(f"\nYou have {total_seconds} seconds.")
    print("Identify as many chords as possible using 1-4.")
    input("\nPress ENTER to start...")
    start = time.monotonic()
    correct = wrong = combo = best_combo = 0
    running_pointys = 0
    event_xp = 0

    while time.monotonic() - start < total_seconds:
        target = random.choice(CHORDS)
        event = roll_event(player, boosts)
        attempts = 3 if event and event.get("guesses") else 1
        solved = False
        while attempts and time.monotonic() - start < total_seconds:
            remaining = max(0, total_seconds - (time.monotonic() - start))
            print(f"\n[{remaining:.1f}s] {combo}x combo")
            selected, ok, quit_game = _ask_chord_question(player, target, _chord_visible_count(player))
            if quit_game:
                return
            attempts -= 1
            if ok:
                solved = True
                break
            wrong += 1
            player["wrong_answers"] += 1
            player["total_questions"] += 1
        if solved:
            correct += 1
            combo += 1
            best_combo = max(best_combo, combo)
            player["correct_answers"] += 1
            player["total_questions"] += 1
            earned = pointy_reward(combo, event, boosts, player)
            give_pointys(player, earned, scoreboard)
            running_pointys += earned
            if event and event.get("xp"):
                event_xp += event["xp"]
            print(color(player, f"Correct! +{earned} pointys", "success"))
        else:
            combo = handle_miss(player, scoreboard, combo)

    player["timed_games"] += 1
    player["timed_correct"] += correct
    player["timed_best"] = max(player["timed_best"], correct)
    if best_combo > player["best_combo"]:
        player["best_combo"] = best_combo
    end_bonus = correct * boosts["pointy_mult"] + magnet_bonus(player)
    give_pointys(player, end_bonus, scoreboard)
    xp_earned = correct * 2 * boosts["xp_mult"] + event_xp
    add_xp(player, xp_earned, scoreboard)
    record_history(player, "timed", "Completed", correct)
    check_achievements(player, scoreboard)
    save_scoreboard(scoreboard)
    banner(player, "TIME'S UP!", "accent")
    print(f"\nCorrect: {correct}")
    print(f"Wrong: {wrong}")
    print(f"Best combo: {best_combo}x")
    print(f"+{running_pointys + end_bonus} pointys")
    print(f"+{xp_earned} XP")
    input("\nPress ENTER to return to the lobby...")

def memory_mode(scoreboard, player_code):
    player = scoreboard[player_code]
    length = random.randint(*difficulty_data(player)["memory_len"])
    sequence = [random.choice(CHORDS) for _ in range(length)]
    banner(player, "CHORD MEMORY")
    print(f"\nRemember this chord sequence ({length} chords).")
    print("You will then identify each chord from four choices.")
    input("\nPress ENTER to reveal...")
    print("\n  " + "  ".join(sequence))
    input("\nPress ENTER when ready...")
    print("\n" * 30)

    boosts = start_boosts(player, scoreboard)
    correct = 0
    position = 0
    mistakes_left = 1
    if player.get("difficulty") == "Easy":
        mistakes_left = 2
    elif player.get("difficulty") == "Hard":
        mistakes_left = 1
    elif player.get("difficulty") == "Extreme":
        mistakes_left = 0

    while position < length:
        target = sequence[position]
        selected, ok, quit_game = _ask_chord_question(
            player, target, _chord_visible_count(player), f"Memory {position+1}/{length}"
        )
        if quit_game:
            return
        if ok:
            correct += 1
            player["correct_answers"] += 1
            player["total_questions"] += 1
            position += 1
            print(color(player, "Correct!", "success"))
        else:
            player["wrong_answers"] += 1
            player["total_questions"] += 1
            mistakes_left -= 1
            print(color(player, f"Wrong! It was {target}.", "error"))
            if mistakes_left < 0:
                break
            if position < length:
                position += 1

    player["memory_games"] += 1
    player["memory_best"] = max(player["memory_best"], correct)
    perfect = correct == length
    if perfect:
        player["memory_perfect_best"] = max(player["memory_perfect_best"], length)
    pointys_earned = pointy_reward(correct * 2 + (length if perfect else 0), None, boosts, player) + magnet_bonus(player)
    give_pointys(player, pointys_earned, scoreboard)
    xp_earned = max(1, correct * 3 * boosts["xp_mult"])
    add_xp(player, xp_earned, scoreboard)
    record_history(player, "memory", "Perfect" if perfect else "Completed", correct)
    check_achievements(player, scoreboard)
    save_scoreboard(scoreboard)
    banner(player, "MEMORY COMPLETE!", "success")
    print(f"\nCorrect: {correct}/{length}")
    print(f"+{pointys_earned} pointys")
    print(f"+{xp_earned} XP")
    print("The sequence was:")
    print("  " + "  ".join(sequence))
    input("\nPress ENTER to return to the lobby...")

def endless_mode(scoreboard, player_code):
    player = scoreboard[player_code]
    banner(player, "ENDLESS CHORDS")
    print("\nKeep identifying chords until you get one wrong.")
    print("Type Q to leave.")
    boosts = start_boosts(player, scoreboard)
    streak = best = 0
    running_pointys = 0
    while True:
        target = random.choice(CHORDS)
        selected, ok, quit_game = _ask_chord_question(
            player, target, _chord_visible_count(player), f"Streak {streak}"
        )
        if quit_game:
            return
        if ok:
            streak += 1
            best = max(best, streak)
            player["correct_answers"] += 1
            player["total_questions"] += 1
            earned = pointy_reward(max(1, streak), None, boosts, player)
            give_pointys(player, earned, scoreboard)
            running_pointys += earned
            print(color(player, f"Correct! +{earned} pointys", "success"))
        else:
            player["wrong_answers"] += 1
            player["total_questions"] += 1
            print(color(player, f"Wrong! It was {target}.", "error"))
            break
    player["endless_games"] += 1
    player["endless_total_correct"] += streak
    player["endless_best"] = max(player["endless_best"], streak)
    player["best_combo"] = max(player["best_combo"], best)
    add_xp(player, max(1, streak * 4), scoreboard)
    record_history(player, "endless", "Completed", streak)
    check_achievements(player, scoreboard)
    save_scoreboard(scoreboard)
    banner(player, "ENDLESS RUN OVER", "accent")
    print(f"\nStreak: {streak}")
    print(f"Best endless: {player['endless_best']}")
    print(f"+{running_pointys} pointys")
    input("\nPress ENTER to return to the lobby...")

def custom_mode(scoreboard, player_code):
    player = scoreboard[player_code]
    cfg = player.get("custom_mode", {"length": 10, "lives": 1, "reward": 1.0})
    length = max(1, int(cfg.get("length", 10)))
    lives = max(0, int(cfg.get("lives", 1)))
    reward_mult = float(cfg.get("reward", 1.0))
    banner(player, "CUSTOM CHORDS")
    print(f"\nQuestions: {length} | Mistakes allowed: {lives}")
    print("Every question is four-choice chord identification.")
    boosts = start_boosts(player, scoreboard)
    correct = wrong = combo = best = 0
    position = 0
    while position < length:
        target = random.choice(CHORDS)
        selected, ok, quit_game = _ask_chord_question(
            player, target, _chord_visible_count(player), f"Question {position+1}/{length}"
        )
        if quit_game:
            return
        if ok:
            correct += 1
            combo += 1
            best = max(best, combo)
            player["correct_answers"] += 1
            player["total_questions"] += 1
            earned = int(max(1, combo) * boosts["pointy_mult"] * reward_mult)
            give_pointys(player, earned, scoreboard)
            print(color(player, f"Correct! +{earned} pointys", "success"))
            position += 1
        else:
            wrong += 1
            player["wrong_answers"] += 1
            player["total_questions"] += 1
            combo = handle_miss(player, scoreboard, combo)
            lives -= 1
            if lives < 0:
                break
            position += 1
    success = position >= length
    if success:
        bonus = int(10 * reward_mult)
        give_pointys(player, bonus, scoreboard)
        xp = int(15 * reward_mult)
        add_xp(player, xp, scoreboard)
    else:
        xp = max(1, correct * 2)
        add_xp(player, xp, scoreboard)
    player["best_combo"] = max(player["best_combo"], best)
    record_history(player, "custom", "Completed" if success else "Failed", correct)
    check_achievements(player, scoreboard, success and wrong == 0)
    save_scoreboard(scoreboard)
    print(color(player, f"\nCustom result: {correct}/{length}", "success" if success else "error"))
    print(f"+{xp} XP")
    input("\nPress ENTER to return to the lobby...")

def custom_mode_setup(scoreboard, player_code):
    player = scoreboard[player_code]
    print("\n========== CUSTOM CHORDS ==========")
    try:
        length = int(input("Questions (3-40): ").strip())
        lives = int(input("Mistakes allowed (0-5): ").strip())
    except ValueError:
        print("Invalid number.")
        return False
    if not 3 <= length <= 40 or not 0 <= lives <= 5:
        print("Questions must be 3-40 and mistakes must be 0-5.")
        return False
    reward = min(2.5, 0.75 + length / 20 + lives * 0.10)
    player["custom_mode"] = {"length": length, "lives": lives, "reward": reward}
    save_scoreboard(scoreboard)
    print(f"Custom mode saved: {length} questions, {lives} mistakes, reward x{reward:.2f}.")
    input("Press ENTER to continue...")
    return True

def _normalize_note_set(raw):
    """Turn user-entered note text into a pitch-class set.
    Accepts commas, spaces, slashes, and hyphens; order does not matter.
    """
    import re
    tokens = [t for t in re.split(r"[\s,;/|+-]+", raw.strip()) if t]
    pitches = []
    for token in tokens:
        pitch = _pitch(token)
        if pitch is None:
            return None
        pitches.append(pitch)
    return set(pitches)


def _note_entry_display(notes):
    return " ".join(notes)


def name_chord_notes_mode(scoreboard, player_code):
    """Show a chord name and require the player to type all of its notes."""
    player = scoreboard[player_code]
    banner(player, "NAME THE CHORD NOTES")
    data = DIFFICULTIES.get(player.get("difficulty", "Normal"), {})
    low, high = data.get("normal_len", (6, 10))
    length = random.randint(low, high)
    boosts = start_boosts(player, scoreboard)
    correct = wrong = combo = best_combo = 0
    running_pointys = 0
    event_xp = 0

    print("\nA chord name will appear. Type every note in that chord.")
    print("Order does not matter. Examples: C E G  |  G,C,E")
    print("Sharps/flats are accepted as enharmonic equivalents (C# = Db).")
    print("Type H for a hint or Q to quit.")

    for number in range(1, length + 1):
        target = random.choice(CHORDS)
        target_notes = chord_notes(target)
        target_pitches = {_pitch(n) for n in target_notes}
        event = roll_event(player, boosts)

        print(f"\nQuestion {number}/{length}")
        print(f"CHORD: {target}")
        print(f"Number of notes: {len(target_notes)}")
        hint_used = False

        while True:
            raw = input("Notes: ").strip()
            if raw.lower() in ("q", "quit"):
                print("\nGame cancelled.")
                return
            if raw.lower() == "h":
                if hint_used:
                    print("Hint already used for this chord.")
                else:
                    hint_used = True
                    print(f"Hint: the chord contains {len(target_notes)} notes.")
                    print(f"One note is: {random.choice(target_notes)}")
                continue

            submitted = _normalize_note_set(raw)
            if submitted is None or not submitted:
                print("Enter notes such as: C E G or C,E,G")
                continue

            ok = submitted == target_pitches
            break

        player["total_questions"] += 1
        if ok:
            correct += 1
            combo += 1
            best_combo = max(best_combo, combo)
            player["correct_answers"] += 1
            earned = pointy_reward(max(1, combo), event, boosts, player)
            give_pointys(player, earned, scoreboard)
            running_pointys += earned
            if event and event.get("xp"):
                event_xp += event["xp"]
            print(color(player, f"Correct! {target}: {_note_entry_display(target_notes)}  +{earned} pointys", "success"))
        else:
            wrong += 1
            combo = handle_miss(player, scoreboard, combo)
            player["wrong_answers"] += 1
            print(color(player, f"Wrong! {target} = {_note_entry_display(target_notes)}", "error"))

    running_pointys, xp_earned = _finish_chord_game(
        player, scoreboard, "note_names", correct, wrong, best_combo,
        running_pointys, correct * 6 + event_xp, wrong == 0
    )
    banner(player, "NOTE MODE COMPLETE!", "success")
    print(f"\nCorrect: {correct}/{length}")
    print(f"Wrong: {wrong}")
    print(f"Best combo: {best_combo}x")
    print(f"+{running_pointys} pointys")
    print(f"+{xp_earned} XP")
    input("\nPress ENTER to return to the lobby...")


def games_menu(scoreboard, player_code):
    while True:
        player = scoreboard[player_code]
        menu_header(player, "GAMES")
        print("\n1. Chords")
        print("2. Timed Chords")
        print("3. Chord Memory")
        print("4. Endless Chords")
        print("5. Custom Chords")
        print("6. Name the Chord Notes")
        print("7. Casino")
        print("8. Back")
        choice = input("\n> ").strip()
        if choice in ("1","2","3","4","5","6"):
            if choose_difficulty(player) is None:
                continue
            save_scoreboard(scoreboard)
            if choice == "1":
                play_game(scoreboard, player_code)
            elif choice == "2":
                timed_mode(scoreboard, player_code)
            elif choice == "3":
                memory_mode(scoreboard, player_code)
            elif choice == "4":
                endless_mode(scoreboard, player_code)
            elif choice == "5":
                if custom_mode_setup(scoreboard, player_code):
                    custom_mode(scoreboard, player_code)
            else:
                name_chord_notes_mode(scoreboard, player_code)
        elif choice == "7":
            casino_menu(scoreboard, player_code)
        elif choice == "8":
            return
        else:
            print("Invalid option.")

# Keep old save fields compatible, but make the discovery screen chord-based.
def discover_verity(player, word, scoreboard=None):
    if word in CHORDS:
        discovered = player.setdefault("discovered_chords", [])
        if word not in discovered:
            discovered.append(word)
            if scoreboard is not None:
                save_scoreboard(scoreboard)

# Make the progression discovery screen show chords instead of the legacy word list.
_old_progression_menu = globals().get("progression_menu")
def progression_menu(scoreboard, player_code):
    player = scoreboard[player_code]
    while True:
        print("\n========== PROGRESSION ==========")
        print(f"Lv.{player['level']} | Prestige {player.get('prestige',0)} | {xp_progress_text(player)}")
        print("1. Story quests")
        print("2. Collection index")
        print("3. Inventory")
        print("4. Pet Lab")
        print("5. Marketplace")
        print("6. Casino VIP / Stats")
        print("7. Chord discoveries")
        print("8. Back")
        c = input("> ").strip()
        if c == "8":
            return
        if c == "1":
            quest_menu(scoreboard, player_code)
        elif c == "2":
            collection_index_menu(scoreboard, player_code)
        elif c == "3":
            inventory_menu(scoreboard, player_code)
        elif c == "4":
            pet_lab_menu(scoreboard, player_code)
        elif c == "5":
            marketplace_menu(scoreboard, player_code)
        elif c == "6":
            casino_status_menu(scoreboard, player_code)
        elif c == "7":
            owned = set(player.get("discovered_chords", []))
            print("\nCHORD DISCOVERIES")
            for chord in CHORDS:
                print(f"[X] {chord}" if chord in owned else "[ ] ???")
            input("\nPress ENTER...")
        else:
            print("Invalid option.")


# ============================================================
# FULL DEVELOPER CONSOLE
# ============================================================

def _dev_max_player(player):
    """Apply the complete developer/god-mode loadout to a player."""
    player["is_dev"] = True
    player["coins"] = 999_999_999
    player["total_pointys_earned"] = max(player.get("total_pointys_earned", 0), 999_999_999)
    player["xp"] = 999_999_999
    player["level"] = 100
    player["prestige"] = 99
    player["prestige_multiplier"] = 1.0 + (99 * PRESTIGE_BONUS)
    player["currency_gems"] = 999_999_999
    player["currency_tokens"] = 999_999_999
    player["currency_void"] = 999_999_999
    player["casino_vip"] = 99
    player["casino_jackpot"] = 999_999_999
    player["casino_biggest_win"] = 999_999_999
    player["casino_best_streak"] = 999
    player["achievements"] = list(ACHIEVEMENTS.keys())
    player["discovered_chords"] = list(CHORDS)
    player["discovered_verities"] = list(CHORDS)
    player["verities_discovered"] = len(CHORDS)
    player["pets"] = list(PET_DATA.keys())
    player["pet_duplicates"] = {k: 99 for k in PET_DATA}
    player["pet_levels"] = {k: 100 for k in PET_DATA}
    player["pet_xp"] = {k: 0 for k in PET_DATA}
    player["pet_bond"] = {k: 999 for k in PET_DATA}
    player["active_pet"] = next(iter(PET_DATA), "")
    player["fusions"] = 999
    player["evolutions"] = 999
    player["mutations"] = 999
    player["upgrades"] = sorted(set(
        player.get("upgrades", []) + [k for k, v in SHOP_ITEMS.items() if v.get("type") == "upgrade"]
    ))
    player["owned_themes"] = sorted(set(list(FREE_THEMES) + list(THEMES.keys())))
    player["owned_titles"] = sorted(set(
        [v.get("value") for v in SHOP_ITEMS.values() if v.get("type") == "title" and v.get("value")] + ["Developer"]
    ))
    player["title"] = "Developer"
    player.setdefault("inventory", {})
    for item_id in SHOP_ITEMS:
        player["inventory"][item_id] = 999
    for item_id in EGG_DATA:
        player["inventory"][item_id] = 999
    for item_id in TRADABLE_ITEMS:
        player["inventory"][item_id] = 999
    return player


def _dev_choose_player(scoreboard, current_code):
    choices = [(code, p) for code, p in scoreboard.items()
               if not str(code).startswith("__") and isinstance(p, dict)]
    if not choices:
        print("No player accounts found.")
        return None
    print("\n========== PLAYER ACCOUNTS ==========")
    for i, (code, p) in enumerate(choices, 1):
        print(f"{i}. {code} — {p.get('name', 'Unknown')} (Lv.{p.get('level', 1)}, {p.get('coins', 0):,} Pointys)")
    raw = input("Select player (ENTER = cancel): ").strip()
    if not raw:
        return None
    try:
        idx = int(raw) - 1
        return choices[idx][0] if 0 <= idx < len(choices) else None
    except ValueError:
        return None


def developer_console(scoreboard, player_code):
    if player_code != DEV_PLAYER_CODE or not scoreboard.get(player_code, {}).get("is_dev"):
        print("Developer access denied.")
        return

    while True:
        dev = scoreboard[player_code]
        print("\n=================================")
        print("        CHORDS DEVELOPER")
        print("=================================")
        print("GOD MODE: ON")
        print(f"Pointys: {dev.get('coins', 0):,} | XP: {dev.get('xp', 0):,} | Lv.{dev.get('level', 1)} | Prestige {dev.get('prestige', 0)}")
        print("\n1. Max / refresh DEV account")
        print("2. Give resources to a player")
        print("3. Max another player's account")
        print("4. Unlock everything for a player")
        print("5. Grant a specific inventory item")
        print("6. Unlock all chords")
        print("7. Set player level / XP / Prestige")
        print("8. Inspect accounts")
        print("9. Reset a player's stats")
        print("10. DEV diagnostics")
        print("11. Back")
        choice = input("> ").strip()

        if choice == "11":
            save_scoreboard(scoreboard)
            return

        if choice == "1":
            _dev_max_player(dev)
            save_scoreboard(scoreboard)
            print("DEV account refreshed to maximum testing state.")

        elif choice == "2":
            target = _dev_choose_player(scoreboard, player_code)
            if target:
                p = scoreboard[target]
                try:
                    amount = int(input("Pointys to give: ").strip())
                    p["coins"] = max(0, p.get("coins", 0) + amount)
                    p["total_pointys_earned"] = max(0, p.get("total_pointys_earned", 0) + max(0, amount))
                    p["currency_gems"] = p.get("currency_gems", 0) + int(input("Gems to give (0 = none): ").strip() or 0)
                    p["currency_tokens"] = p.get("currency_tokens", 0) + int(input("Tokens to give (0 = none): ").strip() or 0)
                    p["currency_void"] = p.get("currency_void", 0) + int(input("Void to give (0 = none): ").strip() or 0)
                    save_scoreboard(scoreboard)
                    print("Resources granted.")
                except ValueError:
                    print("Invalid number.")

        elif choice == "3":
            target = _dev_choose_player(scoreboard, player_code)
            if target:
                _dev_max_player(scoreboard[target])
                save_scoreboard(scoreboard)
                print(f"{target} is now fully unlocked and maxed.")

        elif choice == "4":
            target = _dev_choose_player(scoreboard, player_code)
            if target:
                p = scoreboard[target]
                p["achievements"] = list(ACHIEVEMENTS.keys())
                p["discovered_chords"] = list(CHORDS)
                p["discovered_verities"] = list(CHORDS)
                p["verities_discovered"] = len(CHORDS)
                p["owned_themes"] = sorted(set(list(FREE_THEMES) + list(THEMES.keys())))
                p["owned_titles"] = sorted(set([v.get("value") for v in SHOP_ITEMS.values() if v.get("type") == "title" and v.get("value")]))
                p["upgrades"] = sorted(set(p.get("upgrades", []) + [k for k,v in SHOP_ITEMS.items() if v.get("type") == "upgrade"]))
                save_scoreboard(scoreboard)
                print("All unlocks granted.")

        elif choice == "5":
            target = _dev_choose_player(scoreboard, player_code)
            if target:
                p = scoreboard[target]
                item_id = input("Item / egg / tradable ID: ").strip()
                amount_raw = input("Amount: ").strip()
                try:
                    amount = int(amount_raw)
                    if amount < 1:
                        raise ValueError
                    p.setdefault("inventory", {})[item_id] = p["inventory"].get(item_id, 0) + amount
                    save_scoreboard(scoreboard)
                    print(f"Granted {amount} x {item_id}.")
                except ValueError:
                    print("Invalid amount.")

        elif choice == "6":
            dev["discovered_chords"] = list(CHORDS)
            dev["discovered_verities"] = list(CHORDS)
            dev["verities_discovered"] = len(CHORDS)
            save_scoreboard(scoreboard)
            print(f"All {len(CHORDS)} chords unlocked.")

        elif choice == "7":
            target = _dev_choose_player(scoreboard, player_code)
            if target:
                p = scoreboard[target]
                try:
                    p["level"] = max(1, int(input("Level: ").strip()))
                    p["xp"] = max(0, int(input("XP: ").strip()))
                    p["prestige"] = max(0, int(input("Prestige: ").strip()))
                    p["prestige_multiplier"] = 1.0 + p["prestige"] * PRESTIGE_BONUS
                    save_scoreboard(scoreboard)
                    print("Progression updated.")
                except ValueError:
                    print("Invalid number.")

        elif choice == "8":
            print("\n========== ACCOUNTS ==========")
            for code, p in scoreboard.items():
                if isinstance(p, dict) and not str(code).startswith("__"):
                    print(f"{code}: {p.get('name','?')} | Lv.{p.get('level',1)} | {p.get('coins',0):,} Pointys | Dev={p.get('is_dev', False)}")
            input("Press ENTER...")

        elif choice == "9":
            target = _dev_choose_player(scoreboard, player_code)
            if target and target != DEV_PLAYER_CODE:
                fresh = create_default_player_data(
                    scoreboard[target].get("name", "Player"),
                    scoreboard[target].get("password_salt", ""),
                    scoreboard[target].get("password_hash", ""),
                )
                scoreboard[target] = fresh
                save_scoreboard(scoreboard)
                print("Player stats reset. Login credentials were preserved.")

        elif choice == "10":
            print("\n========== DEV DIAGNOSTICS ==========")
            print(f"Chord pool: {len(CHORDS)}")
            print(f"Pets: {len(PET_DATA)}")
            print(f"Shop items: {len(SHOP_ITEMS)}")
            print(f"Achievements: {len(ACHIEVEMENTS)}")
            print(f"Accounts: {sum(1 for k,v in scoreboard.items() if isinstance(v,dict) and not str(k).startswith('__'))}")
            print("Developer account: ONLINE")
            input("Press ENTER...")
        else:
            print("Invalid option.")


# Add the DEV console to the existing lobby without replacing the normal game flow.
_original_lobby_for_dev = lobby

def lobby(scoreboard, player_code):
    if player_code == DEV_PLAYER_CODE and scoreboard.get(player_code, {}).get("is_dev"):
        while True:
            # Keep the regular lobby available, but make the developer console obvious.
            print("\n[DEV ACCOUNT] Developer console available from option D.")
            # Run the original lobby until it returns. The original lobby is still
            # the authoritative normal gameplay UI.
            return _dev_lobby(scoreboard, player_code)
    return _original_lobby_for_dev(scoreboard, player_code)


def _dev_lobby(scoreboard, player_code):
    while True:
        player = scoreboard[player_code]
        print("\n=================================")
        print("        CHORDS DEV LOBBY")
        print("=================================")
        print(f"Developer | Lv.{player.get('level',100)} | {player.get('coins',0):,} Pointys")
        print("\n1. Normal Chords Lobby")
        print("2. Developer Console")
        print("3. Games")
        print("4. Pets")
        print("5. Shop")
        print("6. Progression")
        print("7. Casino")
        print("8. Save")
        print("9. Quit")
        c = input("\n> ").strip().lower()
        if c == "1":
            return _original_lobby_for_dev(scoreboard, player_code)
        elif c == "2":
            developer_console(scoreboard, player_code)
        elif c == "3":
            games_menu(scoreboard, player_code)
        elif c == "4":
            pet_menu(scoreboard, player_code)
        elif c == "5":
            shop_menu(scoreboard, player_code)
        elif c == "6":
            progression_menu(scoreboard, player_code)
        elif c == "7":
            casino_menu(scoreboard, player_code)
        elif c == "8":
            save_scoreboard(scoreboard)
            print("Saved.")
        elif c == "9":
            save_scoreboard(scoreboard)
            return
        else:
            print("Invalid option.")


# Ensure the developer account exists even on a brand-new installation.
_original_load_scoreboard_for_dev = load_scoreboard
def load_scoreboard():
    scoreboard = _original_load_scoreboard_for_dev()
    ensure_dev_account(scoreboard)
    return scoreboard

if __name__ == "__main__":
    main()

# ============================================================
# V6 SIMPLIFIED CASINO + BUYABLE VIP
# ============================================================

CASINO_VIP_PRICES = {
    1: 500,
    2: 2500,
    3: 10000,
    4: 25000,
    5: 100000,
}

_old_casino_vip_rank = casino_vip_rank

def casino_vip_rank(player):
    # VIP can be earned by wagering OR purchased directly.
    earned = _old_casino_vip_rank(player)
    purchased = int(player.get("casino_vip_purchased", 0))
    return min(5, max(earned, purchased))


def casino_vip_shop(scoreboard, player_code):
    player = scoreboard[player_code]
    while True:
        current = casino_vip_rank(player)
        print("\n========== CASINO VIP SHOP ==========")
        print(f"Pointys: {player['coins']} | VIP: {current}/5")
        if current >= 5:
            print("You already have the highest VIP level!")
            input("Press ENTER...")
            return

        next_level = current + 1
        price = CASINO_VIP_PRICES[next_level]
        print(f"1. Buy VIP {next_level} — {price:,} Pointys")
        print("2. Back")
        choice = input("> ").strip()
        if choice == "2":
            return
        if choice != "1":
            print("Invalid option.")
            continue
        if player["coins"] < price:
            print(f"You need {price-player['coins']:,} more Pointys.")
            continue
        player["coins"] -= price
        player["casino_vip_purchased"] = next_level
        player["casino_vip"] = casino_vip_rank(player)
        save_scoreboard(scoreboard)
        print(f"VIP {next_level} purchased! 🎰")
        input("Press ENTER...")


def casino_more_games_menu(scoreboard, player_code):
    games = [
        ("1", "Five Card Poker", poker_mode),
        ("2", "Craps / Dice", dice_sum_game),
        ("3", "Sic Bo", dice_sum_game),
        ("4", "Casino War", war_game),
        ("5", "Red Dog", red_dog_game),
        ("6", "High Card", high_card_game),
        ("7", "Big Six Wheel", big_six_game),
        ("8", "Keno", keno_game),
        ("9", "Bingo", bingo_game),
        ("10", "Three Card Poker", three_card_poker_game),
        ("11", "Pai Gow", pai_gow_game),
    ]
    while True:
        print("\n========== MORE CASINO GAMES ==========")
        for n, name, _ in games:
            print(f"{n}. {name}")
        print("12. Back")
        choice = input("> ").strip()
        if choice == "12":
            return
        game = next((g for g in games if g[0] == choice), None)
        if game:
            game[2](scoreboard, player_code)
        else:
            print("Invalid option.")


def casino_menu(scoreboard, player_code):
    # Keep the casino compact: popular games on the main screen, everything
    # else behind More Games, and VIP purchasing in its own short menu.
    games = [
        ("1", "Blackjack", blackjack_mode),
        ("2", "Coin Flip", coin_flip_game),
        ("3", "Roulette", roulette_game),
        ("4", "Slots", slots_game),
        ("5", "Baccarat", baccarat_game),
    ]
    while True:
        player = scoreboard[player_code]
        print("\n========== CASINO ==========")
        print(f"Pointys: {player['coins']:,} | VIP {casino_vip_rank(player)}/5")
        for n, name, _ in games:
            print(f"{n}. {name}")
        print("6. More Games")
        print("7. VIP Shop")
        print("8. Back")
        choice = input("> ").strip()
        if choice == "8":
            return
        if choice == "6":
            casino_more_games_menu(scoreboard, player_code)
            continue
        if choice == "7":
            casino_vip_shop(scoreboard, player_code)
            continue
        game = next((g for g in games if g[0] == choice), None)
        if game:
            game[2](scoreboard, player_code)
        else:
            print("Invalid option.")
