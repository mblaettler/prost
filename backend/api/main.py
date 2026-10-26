import argparse
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text

from api import auth
from api.config import product_categories, products, user
from api.bar import bar
from api.deliverer import deliverer
from api.schemas import UserCreate
from api.database import engine, SessionLocal
from models.config.User import UserRole
from models.database import Base

Base.metadata.create_all(bind=engine)


def migrate_schema():
    # create_all does not add columns to existing tables, so add new ones here
    with engine.begin() as conn:
        product_columns = {c["name"] for c in inspect(conn).get_columns("products")}
        if "favourite" not in product_columns:
            conn.execute(text("ALTER TABLE products ADD COLUMN favourite BOOLEAN NOT NULL DEFAULT FALSE"))


migrate_schema()

app = FastAPI(title="Prost Config API")

# CORS is handled by the ingress (Traefik) in k8s; enabled here only for local
# dev, where the Vite dev server (5173) and the API (8000) are different origins.
if os.getenv("ENABLE_CORS_MIDDLEWARE", "false").lower() == "true":
    origins = [
        "*"
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
app.include_router(deliverer.router)

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
        try:
            user.create_user(new_admin_user, db)
        except HTTPException as e:
            if e.status_code == 400:
                print(f"Admin user '{args.username}' already exists, skipping.")
            else:
                raise


if __name__ == "__main__":
    main()
