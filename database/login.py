from typing import List
import database
from connections.connection_pool import pool, get_connection

class Poll:
    def __init__(self, user: str, password: str, _id: int = None):
        self.id = _id
        self.user = user
        self.password = owner

    def __repr__(self):
        return f"Login({self.user!r}: password hidden, ID hidden)"

    # def save(self):
    #     connection = pool.getconn() #pool is an instance of a psycopg2.SimpleConnectionPool-Class
    #     new_poll_id = database.create_poll(connection, self.title, self.owner)
    #     pool.putconn(connection) #add connection that is not used anymore back to pool
    #     self.id = new_poll_id

    # def add_option(self, option_text: str):
    #     Option(option_text, self.id).save()

    # @classmethod
    # def get_info_for_plt(cls, poll_id: int):
    #     with get_connection() as connection:
    #         polls = database.get_poll_options_for_plt(connection, poll_id)
    #         for poll in polls:
    #             print(f'{poll[0]}: {poll[1]}') 
    #         options = [poll[0] for poll in polls]
    #         vote_count = [poll[1] for poll in polls]
    #         return options, vote_count

    # @property #allows to do "pollname.options" instead of "pollname.options()"
    # def options(self) -> List[Option]:
    #     with get_connection() as connection: #better option to the above: use context manager that was created in connection_pool.py
    #         options = database.get_poll_options(connection, self.id)
    #         return [Option(option[1], option[2], option[0]) for option in options]

    # @classmethod
    # def get(cls, poll_id: int) -> "Poll":
    #     with get_connection() as connection:
    #         poll = database.get_poll(connection, poll_id)
    #         return cls(poll[1], poll[2], poll[0])

    # @classmethod
    # def all(cls) -> List["Poll"]:
    #     with get_connection() as connection:
    #         polls = database.get_polls(connection)
    #         return [cls(poll[1], poll[2], poll[0]) for poll in polls]

    # @classmethod
    # def latest(cls):
    #     with get_connection() as connection:
    #         poll = database.get_latest_poll(connection)
    #         return cls(poll[1], poll[2], poll[0])