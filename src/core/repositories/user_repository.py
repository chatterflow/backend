from fastapi import HTTPException, status
from src.core.schemas import schemas
from src.core.models.models import User
from src.core.dto.dto import CreateUserOutput
from src.core.utils.utils import value_exists, select_value, select_everything
from src.core.errors.errors import DuplicateEntryError, DatabaseError, NotFoundError
from src.core.database.hash_passwords import hash_password, password_verify
from datetime import datetime, timedelta
from jose import jwt, JWTError
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
import os

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    # Create an user
    async def create(self, userSchema: schemas.User):
        async with self.db as session:
            userExists = await value_exists(self.db, User, User.email, userSchema.email)
            if userExists:
                raise DuplicateEntryError(
                    'There already exists an user with this CPF registered.')

            newUser = User(
                id=str(uuid.uuid4()),
                nome_completo=userSchema.nome_completo,
                genero=userSchema.genero,
                cpf=userSchema.cpf,
                email=userSchema.email,
                data_nascimento=userSchema.data_nascimento,
                senha=hash_password(userSchema.senha),
                preferencia_comunicacao=userSchema.preferencia_comunicacao,
                cep=userSchema.cep,
                telefone=userSchema.telefone,
                endereco=userSchema.endereco,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            userOutput = CreateUserOutput(
                id=newUser.id,
                nome_completo=newUser.nome_completo,
                genero=newUser.nome_completo,
                cpf=newUser.cpf,
                email=newUser.email,
                data_nascimento=newUser.data_nascimento,
                preferencia_comunicacao=newUser.preferencia_comunicacao,
                cep=newUser.cep,
                telefone=newUser.telefone,
                endereco=newUser.endereco,
                created_at=newUser.created_at,
                updated_at=newUser.updated_at
            )

        try:
            session.add(newUser)
            await session.commit()
            return userOutput
        except Exception as error:
            await session.rollback()
            print(f"Error when inserting data into the database: {str(error)}")
            raise DatabaseError(
                f"Error when inserting user data into the database: {str(error)}")

    # Function to get the user
    async def get(self, userId: str):
        user = await select_value(self.db, User, User.id, userId)
        if not user:
            raise NotFoundError('User not found')
        return user

    # Function to get the user by the email
    async def get_by_email(self, userEmail: str):
        user = await select_value(self.db, User, User.email, userEmail)
        if not user:
            raise NotFoundError('User not found')
        return user

    # SELECT * from users
    async def select_everything(self):
        user = await select_everything(self.db, User)
        if not user:
            raise NotFoundError('Something went wrong')
        return user

    # Function that generates the jwt token
    async def user_login(self, userEmail: str, passwordU: str, expires_in: int = (24 * 60 * 7)):
        user = await select_value(self.db, User, User.email, userEmail)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='User or password are wrong')
        else:
            if password_verify(password=passwordU, hash_password=user.senha):
                exp = datetime.utcnow() + timedelta(minutes=expires_in)
                payload = {
                    'sub': userEmail,
                    'exp': exp
                }
                access_token = jwt.encode(
                    payload, key=SECRET_KEY, algorithm=ALGORITHM)
                return {
                    'access_token': access_token,
                    'exp': exp.isoformat()
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail='User or password are wrong')

    # Function to see if the token is valid
    async def verify_token(self, access_token):
        try:
            data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid access token'
            )

        user_on_db = await select_value(self.db, User, User.email, data['sub'])

        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid access token'
            )
        return user_on_db
