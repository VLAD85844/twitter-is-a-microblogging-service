import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import SessionLocal
from .routes import tweets, users, media
from . import models

logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    app = FastAPI(
        title="Corporate Microblog Service",
        description="Twitter-клон для корпоративной сети",
        version="1.0.0",
    )

    app.include_router(tweets.router, prefix="/api/tweets", tags=["Tweets"])
    app.include_router(users.router, prefix="/api/users", tags=["Users"])
    app.include_router(media.router, prefix="/api/medias", tags=["Media"])

    origins = [
        "http://localhost",
        "http://localhost:8000",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    def on_startup():
        db = SessionLocal()
        try:
            if db.query(models.User).count() == 0:
                test_user = models.User(name="TestUser", api_key="test")
                db.add(test_user)
                db.commit()
                logger.info("Создан пользователь TestUser (api_key='test')")
        except Exception as e:
            logger.error(f"Seeding error: {e}")
        finally:
            db.close()
    @app.get("/")
    def root():
        return {"message": "Corporate microblog API is running!"}

    return app
app = create_app()
