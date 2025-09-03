from fastapi import FastAPI
from app.connection_db.database_connnection import Base, engine
from app.controllers.user_controller import router as user_router
from app.entities.user import UserEntity

Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Service")
app.include_router(user_router)

@app.get("/", tags=["health"])
def health():
    return {"status": "ok"}
