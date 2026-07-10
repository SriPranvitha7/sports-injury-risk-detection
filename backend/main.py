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