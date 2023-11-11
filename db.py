import sqlite3, time
from models import User


def get_db() -> sqlite3.Connection:
    return sqlite3.connect("users.db")


def init():
    CREATE_USER_TABLE = """ CREATE TABLE users (
        timestamp INTEGER NOT NULL,
        chat_id TEXT NOT NULL,
        name TEXT,
        username TEXT
    )
    """
    con = get_db()
    c = con.cursor()
    c.execute(CREATE_USER_TABLE)
    con.commit()
    con.close()


def get_user(chat_id) -> User:
    con = get_db()
    c = con.cursor()
    try:
        c.execute(
            "SELECT timestamp, name, username FROM users WHERE chat_id = ?",
            (str(chat_id),),
        )
        user = c.fetchone()
        if user is not None:
            return User(user[0], str(chat_id), user[1], user[2])
        return None
    except:
        return None
    finally:
        con.commit()
        con.close()


def get_all_user():
    con = get_db()
    c = con.cursor()
    try:
        c.execute("SELECT timestamp, chat_id, name, username FROM users")
        users = c.fetchall()
        if users is None or users == []:
            return []
        array = []
        for user in users:
            array.append(User(user[0], user[1], user[2], user[3]))
        return array

    except:
        return []
    finally:
        con.commit()
        con.close()


def add_user(user: User) -> bool:
    con = get_db()
    c = con.cursor()
    try:
        t = int(time.time()) if user.timestamp is None else user.timestamp
        c.execute(
            "INSERT INTO users VALUES(?,?,?,?)",
            (t, user.chat_id, user.name, user.username),
        )
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        con.commit()
        con.close()


if __name__ == "__main__":
    init() # Run this only once