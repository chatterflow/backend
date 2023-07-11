from core.schemas import schemas
from core.models.models import User
from core.dto.dto import CreateUserOutput
from core.utils.utils import value_exists, selectValue, selectEverything
from core.errors.errors import DuplicateEntryError, DatabaseError, NotFoundError
from core.database.hash_passwords import hash_password
from datetime import datetime
import uuid
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, userSchema: schemas.User): #Create an user
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
                f"Errir when inserting user data into the database: {str(error)}")

    async def get(self, userId: str): # Function to get the user
        user = await selectValue(self.db, User, User.id, userId)
        if not user:
            raise NotFoundError('User not found')
        return user

    async def getViaEmail(self, userEmail: str): # Function to get the user by inserting the email
        user = await selectValue(self.db, User, User.email, userEmail)
        if not user:
            raise NotFoundError('User not found')
        return user

    async def select_everything(self): # SELECT * from users
        user = await selectEverything(self.db, User)
        if not user:
            raise NotFoundError('Something went wrong')
        return user
