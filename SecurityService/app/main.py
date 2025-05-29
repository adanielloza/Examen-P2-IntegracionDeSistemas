# SecurityService/app/main.py

from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel
import jwt  # PyJWT

app = FastAPI(title="SecurityService")

# In a real system you’d load this from env / vault
SECRET_KEY = "your-super-secret-key"
ALGORITHM = "HS256"

class TokenData(BaseModel):
    sub: str
    roles: list[str] = []

@app.get("/verify")
async def verify_token(authorization: str = Header(..., description="Bearer <JWT>")):
    """
    Validate the incoming JWT in the Authorization header.
    Returns the token's 'sub' (username) and any 'roles' claim.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header must start with Bearer",
        )
    token = authorization.removeprefix("Bearer ").strip()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        data = TokenData(**payload)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )
    except (jwt.InvalidTokenError, Exception):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    return {"username": data.sub, "roles": data.roles}
