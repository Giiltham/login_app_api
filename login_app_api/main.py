from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

def run():
    uvicorn.run("login_app_api.main:app", host="127.0.0.1", port=8000, reload=True)

# Création de l'app
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Users
users_db = {
    "jean@example.com": {
        "id": 1,
        "first_name": "Jean",
        "last_name": "Dupont",
        "email": "jean@example.com",
        "hashed_password": pwd_context.hash("ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f"),
        "role": "user",
    },
    "admin@example.com": {
        "id": 2,
        "first_name": "Admin",
        "last_name": "Admin",
        "email": "admin@example.com",
        "hashed_password": pwd_context.hash("240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9"),
        "role": "admin",
    }
}

# Requests
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Routes
@app.post("/login")
async def login(request: LoginRequest):
    user = users_db.get(request.email)

    # check user exist and password is good
    if not user or not pwd_context.verify(request.password, user["hashed_password"]):
        raise HTTPException(
            status_code=400,
            detail={
                "status": 400,
                "message": "Error",
            }
        )

    return {
        "status": 200,
        "message": "Success",
        "id": user["id"],
        "firstName": user["first_name"],
        "lastName": user["last_name"],
        "email": user["email"],
        "role": user["role"],
    }
