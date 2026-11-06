from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.user import User, UserRole
from app.schemas.auth import UserCreate, UserLogin, UserResponse, Token
from app.api.v1.deps import get_current_user

router = APIRouter()

@router.post("/register", response_model=Token)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    hashed_pw = get_password_hash(user_in.password)
    user = User(
        email=user_in.email,
        hashed_password=hashed_pw,
        full_name=user_in.full_name,
        role=user_in.role,
        phone=user_in.phone,
        institution_id=user_in.institution_id,
        kitchen_id=user_in.kitchen_id,
        processing_unit_id=user_in.processing_unit_id,
        ngo_id=user_in.ngo_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(subject=user.email, role=user.role.value)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }

@router.post("/login", response_model=Token)
def login(login_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_in.email).first()
    if not user or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="User account is deactivated")

    token = create_access_token(subject=user.email, role=user.role.value)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/demo-users")
def get_demo_users():
    """Provides instant 1-click test credentials for the 4 core roles."""
    return [
        {
            "role": "ADMIN",
            "name": "Dr. Rajesh Sharma (MoFPI Oversight)",
            "email": "admin@foodwise.gov.in",
            "password": "Password123!",
            "description": "National platform administrator, policy monitor & ESG reporting"
        },
        {
            "role": "KITCHEN_MANAGER",
            "name": "Ananya Desai (Executive Chef & Kitchen Lead)",
            "email": "kitchen@delhitechnical.edu",
            "password": "Password123!",
            "description": "Campus cafeteria manager: demand forecasting, food quality & surplus"
        },
        {
            "role": "PROCESSING_MANAGER",
            "name": "Vikram Malhotra (Plant Operations Lead)",
            "email": "processing@agrofresh.in",
            "password": "Password123!",
            "description": "Industrial processing manager: raw material yield, machine downtime & energy"
        },
        {
            "role": "NGO",
            "name": "Meera Sen (Aahaar Foundation Director)",
            "email": "contact@aahaarngo.org",
            "password": "Password123!",
            "description": "Food bank coordinator: nearby surplus matching, pickup logistics & distribution"
        }
    ]
