from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from SRC.database.session import get_db
from SRC.models.user import User
from SRC.schemas.user import UserCreate, UserResponse, Token
from SRC.core.security import verify_password, get_password_hash, create_access_token, settings
from SRC.logs.logger import get_logger

logger = get_logger("api.auth")

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user account."""
    logger.info(f"Registration attempt for email={user.email}")

    # Check if user exists
    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalars().first()
    if existing_user:
        logger.warning(f"Registration failed: email already registered ({user.email})")
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password,
        role=user.role,
        is_active=user.is_active,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    logger.info(f"User registered successfully: id={db_user.id}, email={db_user.email}")
    return db_user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Authenticate and receive a JWT access token."""
    logger.info(f"Login attempt for username={form_data.username}")

    # Authenticate user
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        logger.warning(f"Login failed: invalid credentials for {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.email, expires_delta=access_token_expires
    )

    logger.info(f"Login successful for user={user.email}")
    return {"access_token": access_token, "token_type": "bearer"}
