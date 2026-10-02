from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from app.routes import router

app = FastAPI(title="ComicCraft - AI Comic Story Creator")

# Ensure required static directories exist
os.makedirs("static/panels", exist_ok=True)
os.makedirs("static/exports", exist_ok=True)
os.makedirs("static/fonts", exist_ok=True)

# Mount static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)