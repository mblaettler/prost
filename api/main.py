import argparse

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import auth
from api.config import product_categories, products, user
from api.bar import bar
from api.schemas import UserCreate
from api.database import engine, SessionLocal
from models.config.User import UserRole
from models.database import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Prost Config API")

# Configure CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(product_categories.router)
app.include_router(products.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(bar.router)

@app.get("/")
def root():
    return {"message": "Welcome to the PaRty Ordering SysTem (PROST) API"}

def main():
    parser = argparse.ArgumentParser(description="PROST administrator CLI")
    parser.add_argument("username", help="Username of the administrator to create")
    parser.add_argument("password", help="Password of the administrator to create")
    args = parser.parse_args()

    new_admin_user = UserCreate(name=args.username, password=args.password, role=UserRole.ADMIN)
    with SessionLocal() as db:
        user.create_user(new_admin_user, db)


if __name__ == "__main__":
    main()
