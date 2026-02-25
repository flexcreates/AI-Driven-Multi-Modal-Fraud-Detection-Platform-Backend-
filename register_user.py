
import asyncio
import sys
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from getpass import getpass

from SRC.config.settings import settings
from SRC.models.user import User
from SRC.core.security import get_password_hash

async def register_user():
    print(f"Connecting to {settings.DATABASE_URL}...")
    engine = create_async_engine(settings.DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    email = input("Enter email for new user: ").strip()
    if not email:
        print("Email cannot be empty.")
        return

    password = getpass("Enter password: ").strip()
    if not password:
        print("Password cannot be empty.")
        return
    
    confirm_password = getpass("Confirm password: ").strip()
    if password != confirm_password:
        print("Passwords do not match.")
        return

    role_input = input("Enter role (ADMIN, ANALYST, USER) [default: ADMIN]: ").strip().upper()
    role = role_input if role_input in ["ADMIN", "ANALYST", "USER"] else "ADMIN"
    
    # Map friendly roles to DB roles if needed (based on seed data: BANK_ADMIN, SOC_ANALYST, USER)
    # Seed data uses: BANK_ADMIN, SOC_ANALYST, USER
    db_role_map = {
        "ADMIN": "BANK_ADMIN",
        "ANALYST": "SOC_ANALYST",
        "USER": "USER"
    }
    db_role = db_role_map.get(role, "BANK_ADMIN")

    name = input("Enter full name [default: New User]: ").strip() or "New User"

    async with async_session() as session:
        try:
            # Check if user exists
            result = await session.execute(select(User).where(User.email == email))
            existing_user = result.scalars().first()
            if existing_user:
                print(f"Error: User with email '{email}' already exists.")
                return

            # Create user
            hashed_password = get_password_hash(password)
            new_user = User(
                email=email,
                hashed_password=hashed_password,
                role=db_role,
                name=name,
                is_active=True
            )
            session.add(new_user)
            await session.commit()
            print(f"\nSuccessfully created user:")
            print(f"Email: {email}")
            print(f"Role: {db_role}")
            print(f"Name: {name}")

        except Exception as e:
            print(f"Error creating user: {e}")
            await session.rollback()

    await engine.dispose()

if __name__ == "__main__":
    try:
        asyncio.run(register_user())
    except KeyboardInterrupt:
        print("\nCancelled.")
