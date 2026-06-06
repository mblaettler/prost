from datetime import timezone, datetime, timedelta
import os
from uuid import UUID

import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session


from api.schemas import Token
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

def extract_role(credential: HTTPAuthorizationCredentials = Depends(security)):
    token = credential.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return payload.get("role", None)

def extract_user(credential: HTTPAuthorizationCredentials = Depends(security)) -> UUID:
    token = credential.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return UUID(payload.get("sub", None))

def verify_admin(credential: HTTPAuthorizationCredentials = Depends(security)):
    role = extract_role(credential)
    if role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin role required"
        )

def verify_bar(credential: HTTPAuthorizationCredentials = Depends(security)) -> UUID:
    role = extract_role(credential)
    if role != "bar":
        raise HTTPException(
            status_code=403,
            detail="Bar role required"
        )
    return extract_user(credential)

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
    token = create_access_token({"sub": user.id.hex, "role": user.role.value})
    return Token(access_token=token, token_type="bearer")

