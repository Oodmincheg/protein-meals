from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.database import get_db  # your existing session dependency
from app.schemas.user import UserCreate, UserOut
from app.crud import user as user_crud

router = APIRouter(tags=["Userbase"])

@router.post("/registration", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing = user_crud.get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists.",
        )
    user = user_crud.create_user(db, payload)
    return user

@router.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return user_crud.get_users(db)

@router.get("/users/{id}", response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user

@router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_user(id: int, db: Session = Depends(get_db)) -> Response:
    user = user_crud.get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    user_crud.delete_user(db, user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
