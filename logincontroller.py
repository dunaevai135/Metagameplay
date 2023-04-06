import metagameplay_pb2
import uuid
import config

from dbcontroller import DBController


class LoginController:

    def __init__(self):
        self.db = DBController()

    def __del__(self):
        del self.db

    # session storage, can be smf redis`ish
    session_storage = {}

    # TODO add expire time
    # TODO del session on new login to dont deal with race cond
    def new_session(self, username):
        session_id = str(uuid.uuid4())
        user = self.db.get_user(username)

        if user is None:
            self.db.create_user(username, credits=config.START_CREDITS_AMMOUNT)

        self.session_storage[session_id] = username

        return (session_id, True)

    def get_username_session(self, session_id):

        if session_id in self.session_storage:
            return self.session_storage[session_id]

        return None

    def validate_session(self, username, session_id):

        if session_id in self.session_storage:
            name = self.session_storage[session_id]
            return name == username

        return False

    def logout(self, session_id):

        if session_id in self.session_storage:
            del self.session_storage[session_id]

        return
