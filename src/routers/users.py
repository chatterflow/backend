from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from src.core.errors.errors import DatabaseError, DuplicateEntryError, NotFoundError
from src.core.schemas.schemas import User
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database.database import get_session
from src.core.repositories.user_repository import UserRepository

router = APIRouter()


@router.get("/user")  # Endpoint to get a single user based on the id
async def get(userId: str, db: AsyncSession = Depends(get_session)):
    try:
        user = await UserRepository(db).get(userId)
        return user
    except NotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.get("/user/email")  # Endpoint to get a single user based on the email
async def get(userEmail: str, db: AsyncSession = Depends(get_session)):
    try:
        user = await UserRepository(db).getViaEmail(userEmail)
        return user
    except NotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.get("/users")  # Endpoint to get all users
async def get(db: AsyncSession = Depends(get_session)):
    try:
        user = await UserRepository(db).select_everything()
        return user
    except NotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.post("/users")  # Endpoint to register a user
async def create(user: User, db: AsyncSession = Depends(get_session)):
    try:
        newUser = await UserRepository(db).create(user)
        return newUser
    except DuplicateEntryError as error:
        raise HTTPException(status_code=406, detail=str(error))
    except DatabaseError as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.post("/user/login")  # Endpoint for login call
async def get(request_form_user: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    try:
        user = await UserRepository(db).user_login(request_form_user.username, request_form_user.password)
        return JSONResponse(
            content=user,
            status_code=status.HTTP_200_OK
        )
    except NotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.get("/user/authenticate")  # Endpoint to authenticate the user
async def getData(token: str, db: AsyncSession = Depends(get_session)):
    try:
        user = await UserRepository(db).verify_token(token)
        return user
    except NotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))
