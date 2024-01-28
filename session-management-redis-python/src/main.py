from datetime import datetime
from fastapi import FastAPI, HTTPException

from .utils import generate_uuid, CreateSession
from .redis_utils import get_user_session, write_session, write_user_session, drop_session, create_user, get_session_by_id

app = FastAPI()

@app.get("/user/create")
async def create_user_id():
    """Create and return a new user_id"""
    user_id = await create_user()
    return {"status": "success", "detail": user_id}

@app.get("/session/create/{user_id}")
async def create_session_api(user_id):
    """
    Create a user session for a user_id

    This first checks if tehre isn't any existing session for the user, and 
    if there is then we expire it and create a new one to replace it.
    """
    try:
        # get the existing user sessions from redis
        existing_session = await get_user_session(user_id)
        await drop_session(existing_session)
        # we will store only those details which are required
        # and maintain a single source of truth, because most of 
        # the user details shall be directed to a different cache/db
        # entirely -> seperation of concerns
        new_session = {
            "created_at": datetime.now().isoformat(),
            "refreshed_at": datetime.now().isoformat(),
            "user_id": user_id,
        }

        # get a random session_id for the new session
        new_session_id = generate_uuid()

        # write back the new session into cache
        await write_session(new_session_id, new_session)
        # when session hasbeen written, write user_id too
        await write_user_session(user_id, new_session_id)

        return {"status": "success", "detail": "successfully created a user session"}
    except Exception as error:
        raise HTTPException(status_code=403, detail=f"Error: {str(error)}")
    
@app.get("/session/validate/{session_id}")
async def validate_user_session_api(session_id) -> dict:
    """validate a user session if its expired or not"""
    try:
        session_data = await get_session_by_id(session_id)
        return {"status": "success", "detail": "user session is valid"}
    except:
        raise HTTPException(status_code=403, detail="user session does not exist")