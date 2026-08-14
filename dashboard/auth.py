"""
Minimal username + PIN authentication.

This is intentionally simple: it's built for a small internal team (a
handful of coordinators), not for public internet exposure. PINs are stored
as SHA-256 hashes in dashboard/users.yaml, never in plain text. If YALL ever
needs stronger security (e.g. the dashboard becomes internet-public with
sensitive data), swap this for a proper auth library such as
streamlit-authenticator or an OAuth login.
"""

import hashlib
import os

import yaml

USERS_PATH = os.path.join(os.path.dirname(__file__), "users.yaml")


def hash_pin(pin: str) -> str:
    return hashlib.sha256(pin.encode("utf-8")).hexdigest()


def load_users():
    with open(USERS_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("users", {})


def save_users(users: dict):
    with open(USERS_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump({"users": users}, f, sort_keys=False, allow_unicode=True)


def verify(username: str, pin: str):
    """Returns the user dict (with username attached) if the PIN matches, else None."""
    users = load_users()
    user = users.get(username)
    if not user:
        return None
    if user.get("pin_hash") != hash_pin(pin):
        return None
    result = dict(user)
    result["username"] = username
    return result


def set_pin(username: str, new_pin: str):
    users = load_users()
    if username not in users:
        raise KeyError(f"No such user: {username}")
    users[username]["pin_hash"] = hash_pin(new_pin)
    save_users(users)


def rename_user(username: str, new_name: str):
    users = load_users()
    if username not in users:
        raise KeyError(f"No such user: {username}")
    users[username]["name"] = new_name
    save_users(users)
