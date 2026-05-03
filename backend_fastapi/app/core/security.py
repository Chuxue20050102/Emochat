from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str) -> str:
    return pwd_context.hash(str(password or ''))


def is_hashed_password(password_hash: str) -> bool:
    value = str(password_hash or '')
    return value.startswith('$2a$') or value.startswith('$2b$') or value.startswith('$2y$')


def verify_password(plain_password: str, password_hash: str) -> bool:
    hashed = str(password_hash or '')
    plain = str(plain_password or '')

    if is_hashed_password(hashed):
        return pwd_context.verify(plain, hashed)

    # Legacy plaintext fallback for old users before hash migration.
    return plain == hashed
