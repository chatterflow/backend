import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.database.database import check_database_connection
from src.routers import users, auth, threads, messages, websockets

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
app.include_router(users.router, tags=(["Users"]))
app.include_router(threads.router, tags=(["Threads"]))
app.include_router(messages.router, tags=(["Messages"]))
app.include_router(websockets.router, tags=(["Websockets"]))
app.include_router(auth.router, tags=(['Authorize Router']))


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
