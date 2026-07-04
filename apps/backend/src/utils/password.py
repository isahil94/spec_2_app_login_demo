"""Password hashing utilities."""

from passlib.context import CryptContext

# Use a portable hashing scheme to avoid bcrypt native-build issues in CI/
# developer environments. sha256_crypt is slower but widely available and
# interoperable for test and dev purposes. For production, prefer bcrypt or
# argon2 with proper native dependencies.
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)
