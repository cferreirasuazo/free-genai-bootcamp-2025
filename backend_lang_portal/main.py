from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routes.word_routes import router as WordEndpoints
from routes.groups_routes import router as GrounpEndpoints
from routes.study_session_routes import router as StudySessionRoutes
from database import engine
from models import Base  # Import Base from models
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables stored in this metadata on startup
    Base.metadata.create_all(bind=engine)
    print("Starting up... Database tables created")
    yield
    # Shutdown
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


app.include_router(WordEndpoints, tags=["words"])
app.include_router(GrounpEndpoints, tags=["groups"])
app.include_router(StudySessionRoutes, tags=["study_sessions"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 