from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from config import UPLOADS_TEMP_PATH

load_dotenv()

# Initialize Firebase Admin SDK if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(os.getenv("FIREBASE_CRED_FILE"))
    firebase_admin.initialize_app(cred, {
    'storageBucket': f"{os.getenv('FIREBASE_STORAGE_DEFAULT_BUCKET')}"
})

from routes.classroom_route import classroom_router
from routes.lecture_route import lecture_router
from routes.questions_route import questions_router


app = FastAPI(title="ListenBack - RAG Chatbot for Lectures")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Frontend development server
        "http://127.0.0.1:3000",  # Alternative localhost
        "http://localhost:3001",  # Alternative frontend port
        "https://yourdomain.com",  # Add your production domain here when deployed
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(classroom_router)
app.include_router(lecture_router)
app.include_router(questions_router)

if not os.path.exists("static"):
    os.makedirs("static")
    os.makedirs(f"{UPLOADS_TEMP_PATH}", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("home.html", {
        "request": request
    })

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "ListenBack backend is running"}

@app.get("/api/test")
async def test_cors():
    return {"message": "CORS is working correctly!", "timestamp": "2025-08-17"}

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))

    uvicorn.run("app:app", host=host, port=port, reload=True)
