"""Util Functions and classes around Redis"""

from dtoenv import load_dotenv
import os

from fastapi import HTTPException

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")

Redis = aioredis.from_url(REDIS_URL)

async def get_user_session(user_id: str) -> str:
    """Get the current session_id for a user (user_id)"""
    try:
        session_id = await Redis.get(user_id)
        return session_id
    except:
        raise HTTPException(status_code=401, detail=f"Unkown error ocurred while fetching from Cache")
    
async def get_session_by_id(session_id: str) -> dict:
    """Get session information from session_id"""
    try:
        session_data = await Redis.get(session_id)
        return json.loads(session_data)
    except:
        raise Exception("cannot retrieve session with the session_id")

async def drop_session(session_id) -> None:
    """Drop an existing user session for rate limiting purposes"""
    try:
        # first check if the key was present or not
        session_data = await Redis.get(session_id)
        # then delete the session if it is not present
        await Redis.delete(session_id)
    except:
        pass

async def write_session(new_session_id: str, new_session: dict) -> None:
    """Write a new user session"""
    try:
        await Redis.set(new_session_id, json.dumps(new_session))
    except:
        raise Exception("unable to set new user session in redis")

async def write_user_session(user_id: str, new_session_id: str) -> none:
    """Function to write a new session to the user"""
    try:
        await Redis.set(user_id, new_session_id)
    except:
        raise Exception("unable to assign session to a user in redis")