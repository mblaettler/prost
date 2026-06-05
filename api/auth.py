from datetime import timezone, datetime, timedelta
import os

import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session


from api.config.schemas import Token
from api.database import get_db
from models.config.User import User as UserModel

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM  = "HS256"
TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()
router = APIRouter(prefix="/login")

def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

async def verify_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("role") != "admin":
            raise HTTPException(
                status_code=403,
                detail="Admin role required"
            )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

def create_access_token(data: dict) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    payload["exp"] = expire
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/", response_model=Token)
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Look up user
    user = db.query(UserModel).filter(UserModel.name == data.username).first()

    # 2. Validate credentials
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Build and return JWT
    token = create_access_token({"sub": user.name, "role": user.role.value})
    return Token(access_token=token, token_type="bearer")

