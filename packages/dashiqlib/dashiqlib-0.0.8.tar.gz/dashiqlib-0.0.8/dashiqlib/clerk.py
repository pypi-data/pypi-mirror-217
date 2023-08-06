"""DashIQ methods for auth with Clerk"""
import os
from typing import NamedTuple
import requests
from dotenv import load_dotenv
from . import MissingEnvVarException


load_dotenv()



CLERK_BASE = 'https://api.clerk.com/v1'
SECRET_KEY = os.environ.get('CLERK_SECRET_KEY')


class ClerkAPIException(Exception):
    """Class to catch Clerk API errors"""

class ClerkAPIParseException(Exception):
    """Class to catch errors while parsing Clerk responses"""

class ClerkAPI404Exception(Exception):
    """Class to catch Clerk 404 errors"""


class User(NamedTuple):
    """Class that represents the key attributes of a user"""
    user_id: str
    profile_photo: str | None
    first_name: str | None



def validate_session(session_id: str) -> bool:
    """Method to check if a session is valid"""
    payload = {}
    try:
        payload = get_session(session_id)
    except ClerkAPI404Exception:
        # occurs when session Id is invalid
        return False

    if payload['status'] == 'active':
        return True
    return False

def get_session(session_id: str) -> dict:
    """Method to return a session payload from Clerk's API"""
    if not SECRET_KEY:
        raise MissingEnvVarException("CLERK_SECRET_KEY not set!")
    headers = {"Authorization": "Bearer " + SECRET_KEY}
    r = requests.get(CLERK_BASE + '/sessions/' + session_id, headers=headers, timeout=1000)
    if r.status_code == 404:
        raise ClerkAPI404Exception("Session not found!")
    if r.status_code != 200:
        raise ClerkAPIException(
                "Error getting session from Clerk API. API returned status code:"
                , r.status_code)
    return r.json()

def get_user(user_id: str) -> dict:
    """Method to return the user payload from Clerk's API"""
    if not SECRET_KEY:
        raise MissingEnvVarException("CLERK_SECRET_KEY not set!")
    headers = {"Authorization": "Bearer " + SECRET_KEY}
    r = requests.get(CLERK_BASE + '/users/' + user_id, headers=headers, timeout=1000)
    if r.status_code == 404:
        raise ClerkAPI404Exception("Session not found!")
    if r.status_code != 200:
        raise ClerkAPIException(
                "Error getting session from Clerk API. API returned status code:",
                r.status_code)
    return r.json()

def get_filtered_user(user_id: str) -> User:
    """Method that returns queries Clerk API for a user and returns only key attributes"""
    json = get_user(user_id)
    return filter_user(json)

def filter_user(u: dict) -> User:
    """Method to filter the """
    user = User(
            user_id=u['id'],
            profile_photo=u.get('image_url'),
            first_name=u.get('first_name')
            )
    return user
