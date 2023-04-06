import dbcontroller as db
import random
import config
from dbcontroller import DBController

db = DBController()


def on_user_login(username):
    user = db.get_user(username)
    db.add_credits(
        user['id'],
        random.randrange(config.RANDOM_RANGE_START, config.RANDOM_RANGE_END))


# TODO think about transactions for buy, sell
def buy(username, item_name):
    if item_name not in config.ALL_ITEMS.keys():
        return False

    dbuser = db.get_user(username)

    try:
        db.subtract_credits(dbuser['id'], config.ALL_ITEMS[item_name])
    except:
        return False

    db.create_item(dbuser['id'], item_name, config.ALL_ITEMS[item_name])
    return True


# TODO need transactions - pure race condition to sell twice one thing
def sell(username, item_name):
    if item_name not in config.ALL_ITEMS.keys():
        return False

    dbuser = db.get_user(username)
    user_items = db.get_item_with_name(dbuser['id'], item_name)

    if len(user_items) == 0:
        return False

    try:
        db.add_credits(dbuser['id'], config.ALL_ITEMS[item_name])
        db.delete_item(user_items[0]['id'])
    except:
        return False

    return True


def get_items():
    return config.ALL_ITEMS
