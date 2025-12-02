from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from config import get_settings
from routes import auth as auth_routes
from routes import wishlists as wishlist_routes
from routes import gifts as gift_routes
from db import Base, engine
from sqlalchemy import text


app = FastAPI(title="Wishlist API", version="0.1.0")

# CORS will be finalized in config, keep permissive for scaffold
app.add_middleware(
	CORSMiddleware,
	allow_origins=settings.backend_cors_origins.split(","),
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

settings = get_settings()
app.add_middleware(SessionMiddleware, secret_key=settings.session_secret_key, same_site="lax")

app.include_router(auth_routes.router)
app.include_router(wishlist_routes.router)
app.include_router(gift_routes.router)


@app.get("/health")
async def health_check():
	return {"status": "ok"}


def get_app() -> FastAPI:
	return app


@app.on_event("startup")
def on_startup():
    # Create tables only in development environment
    if settings.environment == "development":
        Base.metadata.create_all(bind=engine)
    # Best-effort schema patching to avoid manual alembic when container has no CLI
    with engine.begin() as conn:
        try:
            conn.execute(text("ALTER TABLE wishlists ADD COLUMN IF NOT EXISTS share_token VARCHAR(5)"))
            conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS uq_wishlists_share_token ON wishlists(share_token)"))
        except Exception:
            pass


