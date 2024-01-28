"""Util Functions and classes around Redis"""

from dotenv import load_dotenv
import json
import os
import aioredis
from fastapi import HTTPException
from .utils import generate_uuid

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")

Redis = aioredis.from_url(REDIS_URL)

async def create_user() -> str:
    """Create a new user"""
    user_id = generate_uuid()
    await Redis.set(f"user {user_id}", "", 2000)
    return user_id

async def get_user_session(user_id: str) -> str:
    """Get the current session_id for a user (user_id)"""
    try:
        session_id = await Redis.get("user "+user_id)
        return str(session_id)[2:-1]
    except:
        raise HTTPException(status_code=401, detail=f"Unkown error ocurred while fetching from Cache")
    
async def get_session_by_id(session_id: str) -> dict:
    """Get session information from session_id"""
    try:
        session_data = await Redis.get(f"session {session_id}")
        return json.loads(session_data)
    except Exception as error:
        raise Exception("cannot retrieve session with the session_id"+ str(error))

async def drop_session(session_id) -> None:
    """Drop an existing user session for rate limiting purposes"""
    try:
        session = f"session {session_id}"
        # first check if the key was present or not
        session_data = await Redis.get(session)
        print(session, session_data)
        # then delete the session if it is not present
        await Redis.delete(session)
    except:
        pass

async def write_session(new_session_id: str, new_session: dict) -> None:
    """Write a new user session"""
    try:
        await Redis.set(f"session {new_session_id}", json.dumps(new_session))
    except Exception as error:
        raise Exception("unable to set new user session in redis "+ str(error))

async def write_user_session(user_id: str, new_session_id: str) -> None:
    """Function to write a new session to the user"""
    try:
        await Redis.set(f"user {user_id}", new_session_id)
    except Exception as error:
        raise Exception("unable to assign session to a user in redis "+str(error))