# app/dependencies.py
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from app.config import JWT_SECRET, JWT_ALGORITHM

bearer_scheme = HTTPBearer()  # This tells FastAPI it is a "Bearer" security scheme

async def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials  # This is your JWT
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload  # contains admin_id, org
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
