from passlib.context import CryptContext


CRIPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')


def password_verify(password: str, hash_password: str) -> bool:
    """
    Function for determining whether the password is correct by comparing the password in plain text 
    as informed by the user, and the hash of the password that will be saved in the database after account creation.
    """
    return CRIPTO.verify(password, hash_password)


def hash_password(password: str) -> str:
    """
    Function that generates and returns the hash of the password
    """
    return CRIPTO.hash(password)
