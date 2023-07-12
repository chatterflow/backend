from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from src.core.errors.errors import DatabaseError, DuplicateEntryError, NotFoundError
from src.core.schemas.schemas import User
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database.database import get_session
from src.core.repositories.user_repository import UserRepository

router = APIRouter()

 # Endpoint to get a single user based on the id
@router.get("/user/id/{userId}") 
async def get(userId: str, db: AsyncSession = Depends(get_session)):
    try:
        user = await UserRepository(db).get(userId)
        return user
    except NotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))

 # Endpoint to get a single user based on the email
@router.get("/user/email/{userEmail}") 
async def get(userEmail: str, db: AsyncSession = Depends(get_session)):
    try:
        user = await UserRepository(db).get_by_email(userEmail)
        return user
    except NotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))

# Endpoint to get all users
@router.get("/users")  
async def get(db: AsyncSession = Depends(get_session)):
    try:
        user = await UserRepository(db).select_everything()
        return user
    except NotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))

# Endpoint to register a user
@router.post("/user")  
async def create(user: User, db: AsyncSession = Depends(get_session)):
    try:
        newUser = await UserRepository(db).create(user)
        return newUser
    except DuplicateEntryError as error:
        raise HTTPException(status_code=406, detail=str(error))
    except DatabaseError as error:
        raise HTTPException(status_code=500, detail=str(error))

# Endpoint for login call
@router.post("/user/login")  
async def get(request_form_user: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    try:
        user = await UserRepository(db).user_login(request_form_user.username, request_form_user.password)
        return JSONResponse(
            content=user,
            status_code=status.HTTP_200_OK
        )
    except NotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))

# Endpoint to authenticate the user
@router.get("/user/authenticate")  
async def get_data(token: str, db: AsyncSession = Depends(get_session)):
    try:
        user = await UserRepository(db).verify_token(token)
        return user
    except NotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))
