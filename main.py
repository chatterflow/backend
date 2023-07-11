import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.database.database import check_database_connection
from src.routers import users
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    if not await check_database_connection():
        raise RuntimeError("Failed to connect to the database")

@app.get("/")
async def hello():
    return {"Hello world"}


# Routes
app.include_router(users.router, tags=(["Usuários"]))

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
