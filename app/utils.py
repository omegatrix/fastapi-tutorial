from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_hash(password: str):
    return password_context.hash(password)


def verify_password(password: str, hashed_password):
    return password_context.verify(password, hashed_password)
