from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os

from company_data import companies
from roadmap_generator import generate_roadmap
from models import UserInput, ProgressInput
from database import create_database, save_progress
from resume_parser import analyze_resume
from gemini_service import generate_ai_roadmap

app = FastAPI()


# Create database
create_database()


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ai-career-prep-assistant.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Home API
@app.get("/")
def home():

    return {
        "message": "Welcome to AI Placement Preparation Assistant!"
    }


# Get Companies
@app.get("/companies")
def get_companies():

    return companies


# Generate Normal Roadmap
@app.post("/generate-roadmap")
def generate_user_roadmap(user: UserInput):

    result = generate_roadmap(
        user.company,
        user.skills
    )

    return result


# Generate AI Roadmap (Gemini)
@app.post("/generate-ai-roadmap")
def generate_ai(user: UserInput):

    ai_result = generate_ai_roadmap(
        user.company,
        user.skills
    )

    return {
        "ai_roadmap": ai_result
    }


# Save Progress
@app.post("/save-progress")
def save_user_progress(progress: ProgressInput):

    save_progress(
        progress.company,
        progress.skill,
        progress.completed
    )

    return {
        "message": "Progress saved successfully!"
    }


# Upload Resume + ATS Analysis
@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    file_path = file.filename

    with open(file_path, "wb") as f:

        f.write(await file.read())

    resume_result = analyze_resume(file_path)

    os.remove(file_path)

    return {
        "skills": resume_result["skills"],
        "score": resume_result["score"],
        "suggestions": resume_result["suggestions"]
    }