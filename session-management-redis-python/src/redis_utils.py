"""Util Functions and classes around Redis"""

from fastapi import HTTPException

async def get_user_session(user_id: str) -> str:
    """Get the current session_id for a user (user_id)"""
    if error_in_retrieval:
        raise HTTPException(status_code=401, detail=f"Unkown error ocurred while fetching from Cache")
    pass