from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.security import create_access_token, hash_password, verify_password
from app.db.session import get_db
from app.models.student import Student
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserCreate, UserRead


router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    if user.role == "student":
        student_number = f"S{user.id:06d}"
        db.add(Student(user_id=user.id, student_number=student_number))
        db.commit()
    return user


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(str(user.id))
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserRead)
def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/me/profile")
def my_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = {"id": current_user.id, "email": current_user.email, "role": current_user.role}
    if current_user.role == "student":
        student = db.execute(
            select(Student).where(Student.user_id == current_user.id)
        ).scalar_one_or_none()
        if student:
            result["student"] = {
                "id": student.id,
                "student_number": student.student_number,
                "status": student.status,
                "level": student.level,
                "major": student.major,
                "gpa": student.gpa,
                "holds": student.holds,
            }
    return result
