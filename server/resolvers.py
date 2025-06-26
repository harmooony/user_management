from ariadne import convert_kwargs_to_snake_case
from .models import User
from .auth import get_password_hash, verify_password, create_access_token
from sqlalchemy.orm import Session
from .database import SessionLocal
from datetime import datetime


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@convert_kwargs_to_snake_case
def resolve_list_users(obj, info, filter=None, limit=None, offset=None):
    db = SessionLocal()
    try:
        query = db.query(User)

        if filter:
            if filter.get("name"):
                query = query.filter(User.name.ilike(f"%{filter['name']}%"))
            if filter.get("email"):
                query = query.filter(User.email.ilike(f"%{filter['email']}%"))
            if filter.get("role"):
                query = query.filter(User.role == filter["role"])

        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)

        return query.all()
    finally:
        db.close()


@convert_kwargs_to_snake_case
def resolve_get_user(obj, info, id):
    db = SessionLocal()
    try:
        return db.query(User).filter(User.id == id).first()
    finally:
        db.close()


@convert_kwargs_to_snake_case
def resolve_me(obj, info, token=None):
    db = SessionLocal()
    try:
        if not token:
            raise Exception("Authentication required")

        from .auth import decode_token
        payload = decode_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise Exception("Invalid token")

        return db.query(User).filter(User.id == user_id).first()
    finally:
        db.close()


@convert_kwargs_to_snake_case
def resolve_create_user(obj, info, input):
    db = SessionLocal()
    try:
        hashed_password = get_password_hash(input["password"])
        user = User(
            name=input["name"],
            email=input["email"],
            password_hash=hashed_password,
            role=input["role"]
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


@convert_kwargs_to_snake_case
def resolve_update_user(obj, info, id, input):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == id).first()
        if not user:
            raise Exception("User not found")

        if "name" in input:
            user.name = input["name"]
        if "email" in input:
            user.email = input["email"]
        if "password" in input:
            user.password_hash = get_password_hash(input["password"])
        if "role" in input:
            user.role = input["role"]

        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


@convert_kwargs_to_snake_case
def resolve_delete_user(obj, info, id):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == id).first()
        if not user:
            return False

        db.delete(user)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


@convert_kwargs_to_snake_case
def resolve_login(obj, info, email, password):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.password_hash):
            raise Exception("Invalid email or password")

        access_token = create_access_token(data={"sub": str(user.id)})
        return {"token": access_token, "user": user}
    finally:
        db.close()