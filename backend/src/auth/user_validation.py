import bcrypt
import secrets
from playhouse.shortcuts import model_to_dict
from functools import reduce
import time
import datetime
import sys
sys.path.extend("../database")
from database.models import Users
from typing import Optional
from constants import Uid



async def register_user(username: str, email: str, password: str, phone: str) -> bool:
    """
    Adds a user to our database.
    Returns a boolean corresponding to the status code
    of the operation (True for success, False for failure)
    """
    password = password.encode("utf-8")
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    return Users.insert(
        email_address=email, username=username, password=hashed, phone=phone
    ).execute()


async def validate_user(email: str, password: str) -> Optional[Uid]:
    """
    Returns True if the user with the provided email
    and password exist in the database. False if either
    user credentials are wrong or another db error occurs
    """
    password = password.encode("utf-8")

    q_handler = (
        Users.select(Users.password, Users.uid).where(Users.email_address == email).execute()
    )

    q_handler = list(q_handler)

    if not q_handler:
        return False

    hashed_pw = q_handler[0].password.encode("utf-8")

    if bcrypt.checkpw(password, hashed_pw):
        return q_handler[0].uid

    return None


async def generate_session_id() -> str:
    """
    Generates a cryptographically secure session_id
    to be used as the session_id cookie
    """
    return str(secrets.randbits(32))


async def get_user_from_session_id(session_id: str) -> Optional[Users]:
    """
    Returns the user object corresponding to the session_id
    """
    q = Users.select().where(Users.session_id == session_id).execute()

    if q.count == 0:
        return None
    return list(q)[0]


async def clear_session_cookie(uid: Uid) -> None:
    """
    Deletes the session ID associated with a given user
    For security we unset this on each user login
    """
    return Users.update(session_id=None).where(Users.uid == uid).execute()


async def set_user_token(uid: Uid, session_id: str) -> None:
    """
    Updates the database with current user token
    """
    return Users.update(session_id=session_id).where(Users.uid == uid).execute()


async def set_user_image(uid: Uid, img_url: str) -> None:
    """
    Overwrites the image url associated with an email address
    """
    return Users.update(profile_image=img_url).where(Users.uid == uid).execute()
