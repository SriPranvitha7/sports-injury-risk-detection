import os
import uuid
from fastapi import UploadFile, File
from video_processor import check_video_quality, process_video
from risk_analyzer import analyze_risk
from biomechanics_report import generate_full_report

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from auth import hash_password, verify_password, create_access_token

app = FastAPI(title="Sports Injury Risk Detection API")

# This allows your React frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary storage (real database comes in next milestone)
fake_users_db = {}

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    role: str  # athlete, coach, physiotherapist, sports_scientist, admin

class LoginRequest(BaseModel):
    email: str
    password: str

@app.get("/")
def home():
    return {"message": "Sports Injury Risk Detection Backend is Running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "project": "Sports Injury Risk Detection"}

@app.post("/register")
def register(user: RegisterRequest):
    if user.email in fake_users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    fake_users_db[user.email] = {
        "username": user.username,
        "email": user.email,
        "password": hash_password(user.password),
        "role": user.role
    }
    return {"message": "User registered successfully", "role": user.role}

@app.post("/login")
def login(user: LoginRequest):
    db_user = fake_users_db.get(user.email)
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token({"sub": user.email, "role": db_user["role"]})
    return {"access_token": token, "token_type": "bearer", "role": db_user["role"]}

class AthleteProfile(BaseModel):
    username: str
    sport_type: str
    position: str
    age: int
    height_cm: float
    weight_kg: float
    injury_history: str
    training_load: str

athlete_profiles_db = {}

@app.post("/athlete/profile")
def create_athlete_profile(profile: AthleteProfile):
    athlete_profiles_db[profile.username] = profile.dict()
    return {"message": "Athlete profile created successfully", "data": profile}

@app.get("/athlete/profile/{username}")
def get_athlete_profile(username: str):
    profile = athlete_profiles_db.get(username)
    if not profile:
        raise HTTPException(status_code=404, detail="Athlete not found")
    return profile

# Folder to save uploaded videos
UPLOAD_FOLDER = "uploaded_videos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Temporary storage for analysis results
analysis_results_db = {}

@app.post("/video/upload")
async def upload_video(file: UploadFile = File(...)):
    """
    Receives a video file from the frontend.
    Validates the format.
    Saves it to the server.
    Returns a video ID for tracking.
    """
    # Check file format
    allowed_formats = ["video/mp4", "video/quicktime", "video/x-msvideo"]
    if file.content_type not in allowed_formats:
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Please upload MP4, MOV, or AVI."
        )

    # Generate unique ID for this video
    video_id = str(uuid.uuid4())[:8]
    filename = f"{video_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    # Save the file
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    return {
        "message": "Video uploaded successfully",
        "video_id": video_id,
        "filename": filename
    }


@app.post("/video/analyze/{video_id}")
def analyze_video(video_id: str):
    """
    Finds the uploaded video.
    Checks quality.
    Runs pose estimation and risk analysis.
    Stores results.
    """
    # Find the video file
    video_file = None
    for f in os.listdir(UPLOAD_FOLDER):
        if f.startswith(video_id):
            video_file = f
            break

    if not video_file:
        raise HTTPException(status_code=404, detail="Video not found")

    video_path  = os.path.join(UPLOAD_FOLDER, video_file)
    output_path = os.path.join(UPLOAD_FOLDER, f"processed_{video_file}")

    # Step 1 — Check video quality
    quality_ok, quality_message = check_video_quality(video_path)
    if not quality_ok:
        raise HTTPException(status_code=400, detail=quality_message)

    # Step 2 — Process video (OpenCV + MediaPipe + NumPy)
    df = process_video(video_path, output_path)

    # Step 3 — Analyze risk (Scikit-learn + XGBoost logic)
    risk_report = analyze_risk(df)

    # Step 4 — Generate full report with charts
    full_report = generate_full_report(df, risk_report)

    # Store results
    analysis_results_db[video_id] = full_report

    return {
        "message": "Analysis complete",
        "video_id": video_id,
        "risk_category": full_report["summary"]["risk_category"],
        "overall_risk_score": full_report["summary"]["overall_risk_score"]
    }


@app.get("/video/results/{video_id}")
def get_results(video_id: str):
    """
    Returns the full analysis report for a video.
    """
    if video_id not in analysis_results_db:
        raise HTTPException(status_code=404, detail="Results not found. Please analyze the video first.")

    return analysis_results_db[video_id]